# WARNING:

## THIS IS CURRENTLY IN DEVELOPMENT AND SHOULD NOT BE USED AS A REAL HONEYPOT!

### Current version

Version: 0.1 [Beta]

## Basic Explination

ErroxPot is a python based FTP honeypot that works via simulating an entire file system and FTP server.

## How it is possible

Due to how python works, we can have legitamite files on a file system exist within a dictionary. This dictionary will hold the fake file system's path for the file along with a refrence to the real file's path for when the file is downloaded or interacted with in any way that would require the true file system.
