# PyOS 0.7
My """operational system""" made in python

# pyos 0.1 (base)
A simulated operating system (a command-line environment or "shell") in Python.
  It functions as a virtual interface where you can execute commands, manage files,
  and view the time, simulating the experience of a real system.

# pyos 0.2 (File Management Update)
Added the ability to explore local files.
  - Added 'import shutil'
  - The 'cd' command has been added, allowing you to access the local folder by name
  - The 'disk' has been added, allowing you to view the total and free space on your HDD/SSD.

# pyos 0.3 (Login Update)
Added the ability to log into the system using only a username.
  - The Login Loop: Added a small `while not usuario:` loop that prevents the user from simply pressing "Enter" with an empty username. It will keep asking until a username is entered.
  - Personalized welcome: The system now says `Welcome to PyOS, [Your Name]!`
  - Dynamic Prompt: Before, you used `PyOS>`. Now, if you type "Your-Name", the terminal will look like this: `You-Name@PyOS>`

# pyos 0.4 (File Management Update 2)
Improving the 'File Management Update' process.
  - Added 'import stat'
  - `mkdir` (Make Directory) - To create new folders
  - `rmdir` (Remove Directory) - To delete folders

# pyos 0.5 (List Update)
Improved visualization of files and folders.
  - Now, when you type `list`, your terminal will be much more organized, displaying not only directories but also other files. Like this:
  Current directory contents (C:\Your\Folder):
    [FOLDER]   tests
    [FOLDER]   images
    [ARCHIVE]  docs.txt
    [ARCHIVE]  script.py
  - Added 'import subprocess'
  - Added the ability to execute files, regardless of their type.

# pyos 0.6 (Text Management Update)
  - `read`: To read what is written inside a .txt and others text files
  - `write`: To create a file and type text into it, directly from the terminal

# pyos 0.7 (User Database and Their Settings Update)
  - Added 'import JSON'
  A JSON """database""" has been added that saves the username and password of each program user.
  It also saves each user's color display settings.
  - `adduser`: To create a new user account (with password) directly from the terminal
  - `dltuser`: To delete a user from the database (and we'll put a security lock in place to prevent you from deleting yourself while using the system!)
