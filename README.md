![ViewCount](https://hits.sh/github.com/war100ck/BnS-Server-Manager.svg?style=flat-square)

# BNS Server Manager

![BnS Server Manager](https://raw.githubusercontent.com/war100ck/BnS-Server-Manager/main/screen/BNS-Server-Manager.png)

## Description

**BNS Server Manager** is a tool for managing services of the **Blade & Soul** game server.  
It allows administrators and developers to effectively manage all aspects of server processes through a user-friendly graphical interface.

Key features include:  
- Starting and stopping game server services.  
- Setting auto-start intervals.  
- Adding new services to the list of managed components.  
- Editing server configurations through the `config.json` file.  
- Viewing logs of all executed operations.

The program is designed to simplify management of the Blade & Soul server architecture, providing intuitive tools for centralized control.

---

## Installation and Running

### System Requirements
- **Python 3.8+**
- Dependencies: `ttkbootstrap`

### Installing Dependencies
To install the required libraries, run the command:  

```bash
pip install ttkbootstrap
```

### Running the Application

1. Save the program code to the file `bns_server_manager.py`.
2. Execute the command:

```bash
python bns_server_manager.py
```
### Main Tabs

#### Management

- Manage service states (Start, Stop, Enable/Disable).
- Display all added services.
- Buttons for bulk starting/stopping all services.

#### Settings

- Modify paths to executable files.
- Configure auto-start intervals.
- Save changes.

#### Add New Service

- Add new services to the system.
- Fields to input the name and path to the executable file.

#### Console

- Log all operations performed in the application.
- Display the status of command execution.

### Example Configuration File (config.json)

The configuration file contains a list of services in JSON format. Example:

```json
[
    {
        "name": "RankingDaemon",
        "path": "D:\\service\\RankingDaemon\\bin\\RankingDaemon.exe",
        "interval": 10,
        "enabled": true
    },
    {
        "name": "AccountInventoryDaemon",
        "path": "D:\\service\\AccountInventoryDaemon\\bin\\AccountInventoryDaemon.exe",
        "interval": 15,
        "enabled": false
    }
]
```
### Configuration File Parameters

- `name` — The name of the service.
- `path` — The path to the executable file.
- `interval` — The auto-start interval (in seconds).
- `enabled` — The activation flag (enabled/disabled).

### Dependencies

The program uses the following libraries:

- `ttkbootstrap` — for creating a modern and intuitive interface.
- `tkinter` — a standard library for creating graphical interfaces in Python.
- `json` — for working with the configuration file.
- `subprocess` — for managing processes (starting and stopping services).

# Creating an Executable File (.exe) from Your Python Script

To create an executable file (.exe) without the console window from your Python script, follow these steps:

## Step 1. Install PyInstaller
If you haven’t installed PyInstaller yet, run the following command:

```bash
pip install pyinstaller
```
## Step 2. Prepare an Icon (if required)
Make sure the icon file `icon.ico` is in the same folder as your script `BNS-Server-Manager.py`. If you have an image in another format, convert it to .ico.

## Step 3. Create the .exe with PyInstaller
### To create the .exe without the console window, run the following command:

```bash
pyinstaller --onefile --windowed --icon=icon.ico BNS-Server-Manager.py
```
### Command parameters:
- `--onefile` — packs all files into one executable file.
- `--windowed` — excludes the console window.
- `--icon=icon.ico` — adds a custom icon.

## Step 4. Check the Created Executable File
After running the command, PyInstaller will create a `dist` folder where you will find the `BNS-Server-Manager.exe` file.

## Step 5. Run the Created File
Go to the `dist` folder and run `BNS-Server-Manager.exe` to check if it works correctly.

### License

The program is distributed freely. You can use and modify it according to your needs.
