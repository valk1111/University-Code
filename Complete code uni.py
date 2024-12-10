# importing libraries required for the code
from datetime import datetime
import socket
from netmiko import ConnectHandler
import requests

# Function to display the menu
def show_menu():
    print("--- Menu ---")
    print("1 - Show date and time (local computer)")
    print("2 - Show IP address (local computer)")
    print("3 - Show Remote home directory listing")
    print("4 - Backup remote file")
    print("5 - Save web page")
    print("Q - Quit")

# Function for the Date and Time
def show_date_time():
    print(f"Local Date and Time: {datetime.now()}")

# Function for getting the IP address
def show_ip_address():
    try:
        print(f"Local IP Address: {socket.gethostbyname(socket.gethostname())}")
    except Exception as e:
        print(f"Error: {e}")

# Function to connect to the linux system
def connect_to_device():
    return ConnectHandler(
        device_type="linux",
        host="10.8.15.118",
        hort="22",  
        username="valentinas",       
        password="valentinask1",
        secret="valentinask1")

# Function to list the home directory and the path to it on the linux machine
def list_remote_home_directory():
    try:
        with connect_to_device() as connection:
            print("Contents of /home:")
            print(connection.send_command("ls $HOME"))
            print("\nHome Directory Path:")
            print(connection.send_command("echo ~"))
    except Exception as e:
        print(f"Error: {e}")

# Function to backupo a remote file that the user chooses on the linux device
def backup_remote_file():
    remote_file = input("Enter the full path to the remote file: ").strip()
    try:
        with connect_to_device() as connection:
            if connection.send_command(f"test -f {remote_file} && echo exists || echo not_found").strip() != "exists":
                print(f"Error: File '{remote_file}' not found.")
                return

            file_content = connection.send_command(f"cat {remote_file}")
            if not file_content:
                print(f"Error: Failed to read '{remote_file}'.")
                return
            backup_file = f"{remote_file}.old"
            connection.send_command(f"echo '{file_content}' > {backup_file}")
            print(f"Backup created at {backup_file}.")
    except Exception as e:
        print(f"Error: {e}")

# Function to save a specified webpage to the system
def save_web_page():
    url = input("Enter the URL of the web page: ").strip()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open("webpage_backup.html", 'w', encoding='utf-8') as file:
                file.write(response.text)
            print("Web page saved to webpage_backup.html")
        else:
            print(f"Failed to fetch page: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


# Main function
def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip().upper()
        if choice == "1":
            show_date_time()
        elif choice == "2":
            show_ip_address()
        elif choice == "3":
            list_remote_home_directory()
        elif choice == "4":
            backup_remote_file()
        elif choice == "5":
            save_web_page()
        elif choice == "Q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()