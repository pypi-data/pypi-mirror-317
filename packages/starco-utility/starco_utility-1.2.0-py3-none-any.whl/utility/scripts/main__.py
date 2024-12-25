#!/usr/bin/env python3
import os
import sys
from . import linux_service
from . import nginx_config

def main():
    if os.geteuid() != 0:
        print("This script must be run as root!")
        sys.exit(1)

    while True:
        print("\nUtility Scripts Menu")
        print("1. Linux Service Manager")
        print("2. Nginx Configuration Manager")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            linux_service.main()
        elif choice == "2":
            nginx_config.main()
        elif choice == "3":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
