import os
import sys
import time
import curses
import docker
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import Prompt
from rich.table import Table

class DockerManager:
    def __init__(self):
        self.console = Console()
        self.client = None
        self.services = {
            'redis': {'name': 'Redis', 'image': 'redis:latest', 'port': 6379},
            'mysql': {'name': 'MySQL', 'image': 'mysql:latest', 'port': 3306},
            'postgres': {'name': 'PostgreSQL', 'image': 'postgres:latest', 'port': 5432},
            'nginx': {'name': 'Nginx', 'image': 'nginx:latest', 'port': 80},
            'mongodb': {'name': 'MongoDB', 'image': 'mongo:latest', 'port': 27017},
            'elasticsearch': {'name': 'Elasticsearch', 'image': 'elasticsearch:latest', 'port': 9200}
        }
        
    def connect_docker(self):
        try:
            self.client = docker.from_env()
            return True
        except docker.errors.DockerException:
            self.console.print("[yellow]Docker not found. Installing Docker...")
            
            if sys.platform == "linux":
                os.system('''
                    curl -fsSL https://get.docker.com -o get-docker.sh && \
                    sudo sh get-docker.sh && \
                    sudo usermod -aG docker $USER && \
                    sudo systemctl start docker
                ''')
            elif sys.platform == "darwin":
                os.system('brew install --cask docker')
            elif sys.platform == "win32":
                os.system('winget install Docker.DockerDesktop')
                
            self.console.print("[green]Docker installed! Please restart your system and run this script again.")
            return False
        except Exception as e:
            self.console.print(f"[red]Error connecting to Docker: {str(e)}")
            return False
    def show_welcome(self):
        self.console.print(Panel.fit(
            "[bold blue]Docker Service Manager[/bold blue]\n"
            "Welcome to the interactive Docker management system",
            border_style="green"
        ))

    def show_menu(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="dim")
        table.add_column("Description")
        
        table.add_row("1", "List Available Services")
        table.add_row("2", "Install/Start Service")
        table.add_row("3", "Stop Service")
        table.add_row("4", "View Running Services")
        table.add_row("5", "Service Logs")
        table.add_row("6", "Interactive Shell")  # New option
        table.add_row("7", "Exit")
        
        self.console.print(table)

    def list_services(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Service")
        table.add_column("Image")
        table.add_column("Default Port")
        
        for key, service in self.services.items():
            table.add_row(
                service['name'],
                service['image'],
                str(service['port'])
            )
        
        self.console.print(table)

    def install_service(self):
        service_name = Prompt.ask("Enter service name", choices=list(self.services.keys()))
        service = self.services[service_name]
        
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Installing {service['name']}...", total=100)
            
            try:
                # Pull image
                self.client.images.pull(service['image'])
                progress.update(task, advance=50)
                
                # Run container
                container = self.client.containers.run(
                    service['image'],
                    name=f"{service_name}-container",
                    ports={f"{service['port']}/tcp": service['port']},
                    detach=True
                )
                progress.update(task, advance=50)
                
                self.console.print(f"[green]Successfully installed {service['name']}!")
                
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}")

    def stop_service(self):
        containers = self.client.containers.list()
        if not containers:
            self.console.print("[yellow]No running containers found")
            return
            
        choices = [container.name for container in containers]
        container_name = Prompt.ask("Select container to stop", choices=choices)
        
        try:
            container = self.client.containers.get(container_name)
            container.stop()
            self.console.print(f"[green]Successfully stopped {container_name}")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}")

    def view_running(self):
        containers = self.client.containers.list()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Container ID")
        table.add_column("Name")
        table.add_column("Status")
        table.add_column("Ports")
        
        for container in containers:
            table.add_row(
                container.short_id,
                container.name,
                container.status,
                str(container.ports)
            )
        
        self.console.print(table)

    def view_logs(self):
        container_name = Prompt.ask("Enter container name")
        try:
            container = self.client.containers.get(container_name)
            logs = container.logs().decode()
            self.console.print(Panel(logs, title="Container Logs", border_style="blue"))
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}")

    def interactive_shell(self):
        containers = self.client.containers.list()
        if not containers:
            self.console.print("[yellow]No running containers found")
            return
            
        choices = [container.name for container in containers]
        container_name = Prompt.ask("Select container for interactive shell", choices=choices)
        
        try:
            container = self.client.containers.get(container_name)
            self.console.print(f"[green]Entering interactive shell for {container_name}")
            self.console.print("[yellow]Type 'exit' to leave the shell")
            
            # Execute interactive shell
            os.system(f"docker exec -it {container_name} /bin/bash || docker exec -it {container_name} /bin/sh")
            
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}")

    def run(self):
        self.show_welcome()
        
        if not self.connect_docker():
            self.console.print("[red]Error: Could not connect to Docker. Is it installed and running?")
            return

        while True:
            self.show_menu()
            choice = Prompt.ask("Select an option", choices=['1', '2', '3', '4', '5', '6', '7'])
            
            if choice == '1':
                self.list_services()
            elif choice == '2':
                self.install_service()
            elif choice == '3':
                self.stop_service()
            elif choice == '4':
                self.view_running()
            elif choice == '5':
                self.view_logs()
            elif choice == '6':
                self.interactive_shell()
            elif choice == '7':
                self.console.print("[yellow]Goodbye!")
                break
def main():
    manager = DockerManager()
    manager.run()
if __name__ == "__main__":
    main()
