## General
____________

### Author
* Josh McIntyre

### Website
* jmcintyre.net

### Overview
* CorduroyCarver is an experimental file carver for JPG photo data recovery

## Development
________________

### Git Workflow
* master for releases (merge development)
* development for bugfixes and new features

### Building
* make build
Build the application
* make clean
Clean the build directory

### Features
* Takes a disk device to search for JPG file signatures
* Takes a directory to recover data to
* Searches the disk byte-by-byte for JPG file signatures (file carving)
* Writes discovered files to disk at the specified directory

### Requirements
* Requires Python 3.7

### Platforms
* Linux
* MacOSX

## Usage
____________

### Command line usage
* Run `python corduroycarver.py <disk_file> <recovery_dir>`
* Ex: `python corduroycarver.py /dev/sdb /home/josh/testrec`
* CorduroyCarver will search the disk device or ISO file byte-by-byte for JPG file signatures (file carving)
* It will write the discovered files back to disk in the specified directory