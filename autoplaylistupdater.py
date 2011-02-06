import pprint
import xml.dom.minidom
import os
import sys
from xml.dom.minidom import Node
from MP3Info import *

# References:
#   http://docs.python.org/contents.html
#   http://oreilly.com/catalog/pythonxml/chapter/ch01.html#94838

doc = xml.dom.minidom.parse("C:\Users\Christabel\Documents\Auto Playlist Updater\playlists.xml")
 
playlists = []
i = 0

# For each playlist, grab the filename of the playlist and the folders to scan for each.
for node in doc.getElementsByTagName("playlist"):
  valid_filename = 0
  valid_folder = 0

  # Grab and set the filename to the variable "filename".  
  filename = ""
  L = node.getElementsByTagName("filename")
  for node2 in L:
    for node3 in node2.childNodes:
      if node3.nodeType == Node.TEXT_NODE:
        filename += node3.data
        valid_filename = 1

  # Grab and set the folders for this playlist to the list "folder_list". 
  folder_list = []
  L = node.getElementsByTagName("folder")
  for node2 in L:
    folder_recursive = node2.getAttribute("recursive")
    for node3 in node2.childNodes:
      if node3.nodeType == Node.TEXT_NODE:
        folder_list.append(node3.data)
        valid_folder = 1

  # If the filename was found and at least one folder was found, append the item to the list of playlists.        
  if valid_filename == 1 and valid_folder == 1:
      playlists.append([i, filename, folder_list])
      i = i + 1
    
# Pretty-print the list of playlists.
#pprint.pprint(playlists)

# Check to see if we can write to the M3U file.
for playlist in playlists:
    #print "Playlist file:", playlist[1]

    # If the playlist file does not exist yet, create it.
    # If it exists, open it in write mode (destroying all existing data).
    if os.access(playlist[1], os.F_OK) == False:
        FILE = open(playlist[1], "w")
    else:
        if os.access(playlist[1], os.W_OK) == True:
            FILE = open(playlist[1], "w")
        else:
            #print "ERROR: Cannot open", playlist[1], "in write mode. Aborting."
            break

    # Write the required M3U header line.
    FILE.write('#EXTM3U\n')

    # For each folder we pull, traverse the file list and write the contents of the M3U file.    
    for folder_name in playlist[2]:
        list_allfiles = []
        
        try:
            list_allfiles = os.listdir(folder_name)
        except:
            #print "Didn't find the directory", folder_name
            break

        # Traverse the list of files and create a list of just MP3 files.
        list_mp3 = []
        for item_allfiles in list_allfiles:
            basename, extension = os.path.splitext(item_allfiles)
            if extension == ".mp3":
                list_mp3.append(os.path.join(folder_name, item_allfiles))

        # Traverse the list of MP3s and get the artist name, track name, and length of the file (in seconds).
        for item_mp3 in list_mp3:
            mp3info_file = MP3Info(open(item_mp3, 'rb'))
            FILE.write('#EXTINF:' + str(mp3info_file.mpeg.__dict__["total_time"]) + ',' + mp3info_file.__dict__["artist"] + ' - ' + mp3info_file.__dict__["title"])
            FILE.write('\n')
            FILE.write(item_mp3)
            FILE.write('\n')
            
    # Close the playlist file.
    FILE.close()

    #print ''    

#print ''