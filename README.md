# WARNING:

## THIS IS CURRENTLY IN DEVELOPMENT AND SHOULD NOT BE USED AS A REAL HONEYPOT!

### Current version

Version: 0.1.2 [Beta]

### Current tasks:

File system:

    Add the ability to have policies for file access to simulate a secure file system
    Optimize the file system to handle several hundred requests per second
    Expand the errors so that when an error is raised other programers can handle it according to type instead of output

Server connections:

    Listen for new connections
    Allow for multiple connections to be handled
    Create a way to return to a port scan with a header / motd
    Create a way to ban certain IPv4 and IPv6 addresses from connecting
    Call the FTP-honeypot.py file for handling the honeypot connection after establishing the connection

Creating base file system:

    Possibly increase the dataset for creating a fake base level file system for Linux

Encryption for SFTP / FTPS:
    
    Develop method for generating a secure key
    Develop a way to encrypt / decrept data

Honeypot API:

    Make there a way to have a banner for handling port scans in realistic ways
    Make the Handle_FTP_Session.download_file() method transfer file data to the remote client
    Make the Handle_FTP_Session.upload_file() method transfer file data from the remote client
    Make the Handle_FTP_Session.listen_for_command() method handle each command from the user

logging.py:

    Nothing to do! Yippe!

Installer file:

    Create a basic installer for getting all the needed; 
      files created, packages installed and do a system check to ensure the device is capable of running this script


## Basic Explination

ErroxPot is a python based FTP honeypot that works via simulating an entire file system and FTP server.

## How it is possible

Due to how python works, we can have legitamite files on a file system exist within a dictionary. This dictionary will hold the fake file system's path for the file along with a refrence to the real file's path for when the file is downloaded or interacted with in any way that would require the true file system.
