# A simple experimental file carving program
# This program will look for files by signature
# It will then attempt to recover the files to a new location
#
# Author: Josh McIntyre
#
import os
import argparse

# Define constants
JPG_START = b"\xFF\xD8\xFF"
JPG_END = b"\xFF\xD9"

# Actually recover found files to disk
def recover(diskpath, save, found):

    # Open the disk again for reading
    with open(diskpath, "rb") as disk:
        
        # Iterate over the found list and write files to the save location
        for num, posdict in found.items():

            # Seek to the file position
            disk.seek(posdict["start"] - 1)
            
            # Calculate the number of bytes to read
            filesize = posdict["end"] - posdict["start"]
            print(f"Attempting recovery of jpg {num} of size {filesize} bytes")

            # Read the data into a buffer, then write to disk
            buf = disk.read(filesize)

            # Write the recovered image to disk
            with open(f"{save}/{num}.jpg", "wb") as rec:
                rec.write(buf)
            print("Wrote recovered file {num}.jpg to disk")

# Search for files by signature
def search(diskpath):
    
    # A list of tuples to store found file positions
    found = {}
    counter = 0

    # Open the disk for reading and search for signatures
    with open(diskpath, "rb") as disk:
        
        # Get the size
        size = disk.seek(0, os.SEEK_END)
        print(f"Disk of size {size} bytes")

        # Start at the beginning
        # Search for file signatures
        buf = [ b"\x00", b"\x00", b"\x00" ]
        posbuf = [ 0, 0, 0 ]

        disk.seek(0,0)
        while True:

            # Read the next byte in
            curbyte = disk.read(1)
            if not curbyte:
                break

            # First, check if we have a matching JPG start or end
            # If so, update the found list
            if  b"".join(buf) == JPG_START:
                print(f"Found start of JPG at pos {posbuf[0]}")
                found[counter] = {"start" : posbuf[0] } 
            elif JPG_END in b"".join(buf):
                # If there's not already a start entry for this, skip it (false positive)
                if counter in found:
                    print(f"Found end of JPG at pos {posbuf[2]}")
                    found[counter]["end"] = posbuf[2]
                    counter = counter + 1

            # Now update the data buffer and position buffer with the new read
            buf[0] = buf[1]
            buf[1] = buf[2]
            buf[2] = curbyte

            posbuf[0] = posbuf[1]
            posbuf[1] = posbuf[2]
            posbuf[2] = disk.tell()
            

        print(f"Found {counter} JPG files.")
        return found

def main():

    parser = argparse.ArgumentParser(description="A simple experimental file carver")
    parser.add_argument("disk", type=str, help="The low-level disk to search (ex: /dev/sdb")
    parser.add_argument("save", type=str, help="The location to save the recovered files to")
    args = parser.parse_args()

    found = search(args.disk)
    recovered = recover(args.disk, args.save, found)

if __name__ == "__main__":
    main()

