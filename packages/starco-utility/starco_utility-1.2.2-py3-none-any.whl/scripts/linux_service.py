#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from typing import Optional
import time
from colorama import init, Fore, Style
import tqdm

# Initialize colorama for colored output
init()

class ServiceManager:
    def __init__(self):
        self.services_dir = "/etc/systemd/system"
    
    def create_service_file(self, service_name: str, exec_path: str, 
                          working_directory: str, description: str = "",
                          user: str = "root", group: str = "root",
                          environment: dict = None, dependencies: list = None) -> bool:
        
        env_vars = "\n".join([f"Environment={k}={v}" for k,v in (environment or {}).items()])
        deps = "\n".join([f"Requires={dep}" for dep in (dependencies or [])])
        
        service_content = f"""[Unit]
Description={description if description else service_name}
After=network.target
{deps}

[Service]
Type=simple
ExecStart={exec_path}
Restart=always
RestartSec=3
User={user}
Group={group}
WorkingDirectory={working_directory}
{env_vars}
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier={service_name}

[Install]
WantedBy=multi-user.target
"""
        service_file_path = f"{self.services_dir}/{service_name}.service"
        
        try:
            with open(service_file_path, 'w') as f:
                f.write(service_content)
            print(f"{Fore.GREEN}✓ Service file created at {service_file_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Error creating service file: {str(e)}{Style.RESET_ALL}")
            return False

    def _run_systemctl_command(self, command: str, service_name: str) -> bool:
        try:
            result = subprocess.run(
                ['systemctl', command, f'{service_name}.service'],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"{Fore.GREEN}✓ Service {service_name} {command} successfully{Style.RESET_ALL}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}✗ Error during {command}: {e.stderr}{Style.RESET_ALL}")
            return False

    def enable_service(self, service_name: str) -> bool:
        return self._run_systemctl_command('enable', service_name)

    def start_service(self, service_name: str) -> bool:
        return self._run_systemctl_command('start', service_name)
    
    def stop_service(self, service_name: str) -> bool:
        return self._run_systemctl_command('stop', service_name)
    
    def restart_service(self, service_name: str) -> bool:
        return self._run_systemctl_command('restart', service_name)
    
    def get_status(self, service_name: str) -> str:
        try:
            result = subprocess.run(
                ['systemctl', 'status', f'{service_name}.service'],
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stdout if e.stdout else e.stderr

    def list_services(self) -> list:
        services = []
        for file in os.listdir(self.services_dir):
            if file.endswith('.service'):
                services.append(file[:-8])  # Remove .service extension
        return services

    def show_logs(self, service_name: str, lines: int = 50) -> str:
        try:
            result = subprocess.run(
                ['journalctl', '-u', f'{service_name}.service', '-n', str(lines)],
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error getting logs: {e.stderr}"

def progress_bar(description: str, duration: int = 3):
    for i in tqdm.tqdm(range(duration), desc=description):
        time.sleep(1)

def main():
    if os.geteuid() != 0:
        print(f"{Fore.RED}This script must be run as root!{Style.RESET_ALL}")
        sys.exit(1)

    service_manager = ServiceManager()

    while True:
        print(f"\n{Fore.CYAN}Linux Service Manager{Style.RESET_ALL}")
        print("1. Create Service")
        print("2. Enable Service")
        print("3. Start Service")
        print("4. Stop Service")
        print("5. Restart Service")
        print("6. Show Service Status")
        print("7. Show Service Logs")
        print("8. List All Services")
        print("9. Exit")

        choice = input(f"\n{Fore.YELLOW}Enter your choice (1-9): {Style.RESET_ALL}")

        if choice == "1":
            service_name = input("Enter service name: ")
            exec_path = input("Enter full path to executable: ")
            working_directory = input("Enter Working Directory: ")
            description = input("Enter service description (optional): ")
            user = input("Enter service user (default: root): ") or "root"
            group = input("Enter service group (default: root): ") or "root"
            
            progress_bar("Creating service")
            service_manager.create_service_file(
                service_name, exec_path, working_directory, 
                description, user, group
            )

        elif choice == "2":
            service_name = input("Enter service name: ")
            progress_bar("Enabling service")
            service_manager.enable_service(service_name)

        elif choice == "3":
            service_name = input("Enter service name: ")
            progress_bar("Starting service")
            service_manager.start_service(service_name)

        elif choice == "4":
            service_name = input("Enter service name: ")
            progress_bar("Stopping service")
            service_manager.stop_service(service_name)

        elif choice == "5":
            service_name = input("Enter service name: ")
            progress_bar("Restarting service")
            service_manager.restart_service(service_name)

        elif choice == "6":
            service_name = input("Enter service name: ")
            status = service_manager.get_status(service_name)
            print(f"\n{Fore.CYAN}Service Status:{Style.RESET_ALL}\n{status}")

        elif choice == "7":
            service_name = input("Enter service name: ")
            lines = input("Enter number of log lines (default: 50): ") or "50"
            logs = service_manager.show_logs(service_name, int(lines))
            print(f"\n{Fore.CYAN}Service Logs:{Style.RESET_ALL}\n{logs}")

        elif choice == "8":
            services = service_manager.list_services()
            print(f"\n{Fore.CYAN}Installed Services:{Style.RESET_ALL}")
            for service in services:
                print(f"- {service}")

        elif choice == "9":
            print(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
