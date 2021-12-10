#!/usr/bin/env python3

import os
import shutil
import time
from run import main

source = 'cameraImageRepo/'  # files location
destination = 'bufferStorage/'  # where to move to
folder = os.listdir(source)  # returns a list with all the files in source

while folder:  # True if there are any files, False if empty list
      # 5 files at a time
    
    for i in range(min(5,len(folder))):
        file = folder[0]  # select the first file's name
        
        curr_file = source + file  # creates a string - full path to the file
        
        shutil.move(curr_file, destination)  # move the files
        
        print(f'{file} moved to {destination}')
        folder.pop(0)


    main()
