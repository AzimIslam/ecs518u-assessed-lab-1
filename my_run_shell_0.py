import os, sys
import shutil
from datetime import datetime
import signal
import time
import glob
import shutil
import pwd
#add other imports as needed by your script
# The purpose of this script is to give you simple functions for locating an executable program in common locations in the Linux path

# Simple shell
# COMMANDS          ERRORS CHECKED
# 1. info XX         - check file/dir exists
# 2. files
# ... omitted for simplicity
# 8. Default is to run the program


# Here the path is hardcoded, but you can easily optionally get your PATH environ variable
# by using: path = os.environ['PATH'] and then splitting based on ':' such as the_path = path.split(':')
THE_PATH = ["/bin/", "/usr/bin/", "/usr/local/bin/", "./"]

new_pid = -1

def signal_handler(signum, frame):
    if new_pid == 0:
        sys.exit(9)

signal.signal(signal.SIGINT, signal_handler)

# ========================
#    Run command
#    Run an executable somewhere on the path
#    Any number of arguments
# ========================
def runCmd(field, new_pid):
  global PID, THE_PATH

  cmd = fields[0]
  cnt = 0
  args = []
  while cnt < len(fields):
      args.append(fields[cnt])
      cnt += 1

  execname = add_path(cmd, THE_PATH)

  # execv executes a new program, replacing the current process; on success, it does not return. 
  # On Linux systems, the new executable is loaded into the current process, and will have the same process id as the caller.
  if new_pid == 0:
    if not execname:
        print ("Executable file", cmd, "not found")
    else:
        try:
            os.execv(execname, args)
        except :
            print("Something went wrong there")
            os._exit(0)
  else:
    status = os.waitpid(0,0)
    exitCode = os.WEXITSTATUS(status[1])
    print("Process exited with code: " + str(exitCode))

# ========================
#    Constructs the full path used to run the external command
#    Checks to see if the file is executable. Returns False on failure.
# ========================
def add_path(cmd, path):
    if cmd[0] not in ['/', '.']:
        for d in path:
            execname = d + cmd
            if os.path.isfile(execname) and os.access(execname, os.X_OK):
                return execname
        return False
    else:
        return cmd

# ================================
#    files command
#    List file and directory names
#    No arguments
# ================================
def files_cmd(fields):
    if checkArgs(fields, 0):
        for filename in os.listdir('.'):
            if os.path.isdir(os.path.abspath(filename)): print("dir:", filename)
            else: print("file:", filename)

# ========================
#  info command
#     List file information
#     1 argument: file name
# ========================
def info_cmd(fields):
    # Checks if one argument is provided to the command
    if checkArgs(fields, 1):
        #   Checks if the file or directory exists - if it does it display info
        #   Otherwise, it states that the path was not found
        if os.path.exists(os.path.abspath(fields[1])):
            #   Checks if the path provided is a directory or file
            #   and then prints the relevant info
            if os.path.isdir(fields[1]):
                print("Type: Directory")
            else:
                print("Type: File")
                print("File Size (Bytes): " + str(os.path.getsize(fields[1])))
                print("Executable: " + str(os.access(fields[1], os.X_OK)))

            print("Owner: " + pwd.getpwuid(os.stat(fields[1]).st_uid).pw_name)
            print("Last changed: " + time.ctime(os.path.getmtime(fields[1])))
            
        else: print(fields[1] + " does not exist.")



# ==========================
#  delete command
#     Delete file
#     1 argument: file name
# ==========================
def delete_cmd(fields):
    # Checks if one argument is provided to the command
    if checkArgs(fields, 1):
        #   Checks if the file exists
        #   Otherwise, it states that the file was not found
        if os.path.exists(os.path.abspath(fields[1])):
            #   Attempt to use OS.remove() to delete the file and display a message stating the file is deleted
            #   OSError exception is only thrown when you try to delete a directory
            #   This exception is handled and when this does occur and error message is printed
            try:
                os.remove(fields[1])
                print(fields[1] + " has been deleted.")
            except OSError:
                print("Error: You cannot delete a directory with this command.")
            # If you do not have permissions to delete a file, an error message is printed
            except PermissionError:
                print("Operation not permitted: You do not have permission to delete: "+ fields[1])
        else: print(fields[1] + " does not exist.")


# ============================================
#  copy command
#     Copies a file
#     1 argument: file that exists
#     2 argument: file name that doesn't exist
# ============================================
def copy_cmd(fields):
    # Checks if two arguments are provided to the command
    if checkArgs(fields, 2):
        #   Checks if the file name provided in the first argument exists in the current directory
        #   If it does not exist an error message is printed
        if os.path.exists(os.path.abspath(fields[1])):
            # Checks that the file name provided in the second argument does not exist
            # This is because we do not want to override a file that currently exists
            # If the file does exist an error message is printed to the console
            if not(os.path.exists(os.path.abspath(fields[2]))):
                # Attempt to use shutil.copyfile() to copy file specified and print a message stating that this has be done
                # IsADirectoryError is only thrown when the path name provided is a directory
                # This exception is handled and when the exception occurs and error message is printed
                try:
                    shutil.copyfile(fields[1], fields[2])
                    print(fields[1] + " has been copied as " + fields[2])
                except IsADirectoryError:
                    print("Error: You cannot copy a directory with this command.")
                # If you do not have permissions to copy a file, an error message is printed
                except PermissionError:
                    print("Operation not permitted: You do not have permission to copy: "+ fields[1])
            else: print("The file " + fields[2] + " exists already. Please choose a different file name.")
        else: print("The file to copy: " + fields[1] + " does not exist.")

# ===================================================================
#  down command
#     Change to the specified directory, inside the current directory
#     1 argument: directory name
# ===================================================================

def down_cmd(fields):
    # Checks if one argument is provided to the command
    if checkArgs(fields, 1):
        # Ensures that the user cannot go up a directory
        if fields[1] == '../': 
            print("Operation not permitted: Please use up to change to the parent directory")
            return
        # Checks if the directory exists
        # If it doesn't an error message is printed
        if os.path.exists(os.path.abspath(fields[1])):
            # Attempts to change directory using os.chdir()
            # NotADirectoryError is only thrown when the path name provided is a directory
            # This exception is handled and when the exception occurs and error message is printed
            try:
                os.chdir(fields[1])
            except NotADirectoryError:
                print(fields[1] + " is not a directory")
            # If you do not have permissions to read a directory, an error message is printed
            except PermissionError:
                print("Operation not permitted: You do not have permission to view the directory: "+ fields[1])
        else: print("Directory " + fields[1] + " does not exist.")

# =================================================
#  up command
#     Change to the parent of the current directory
# =================================================        
def up_cmd(fields):
    # Checks that no arguments are provided
    if checkArgs(fields, 0):
        # Checks that you're in the root directory
        # If you are in the root directory it prints an error message that you cannot go up any further
        if not(os.getcwd() == '/'):
            # We use os.chdir(../) to go to the parent directory
            os.chdir('../')
        else:
            print('The root directory has no parent directory.')

# ========================
#  exit command
#     Exits the shell
# ======================== 
def exit_cmd(fields):
    # Checks that no arguments are provided
    if checkArgs(fields, 0): sys.exit(0)

# ==============================
#  where command
#     Show the current directory
# ==============================
def where_cmd(fields):
    # Checks that no arguments are provided
    if checkArgs(fields, 0): print(os.getcwd())


# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
    numArgs = len(fields) - 1
    if numArgs == num:
        return True
    if numArgs > num:
        print("Unexpected argument", fields[num+1], "for command", fields[0])
    else:
        print("Missing argument for command", fields[0])

    return False

# ----------------------------------------------------------------------------------------------------------------------

while True:
    line = input("PShell>")
    fields = line.split()
    
    if fields[0] == "files": files_cmd(fields)
    elif fields[0] == "info": info_cmd(fields)
    elif fields[0] == "delete": delete_cmd(fields)
    elif fields[0] == "copy": copy_cmd(fields)
    elif fields[0] == "where": where_cmd(fields)
    elif fields[0] == "up": up_cmd(fields)
    elif fields[0] == "down": down_cmd(fields)
    elif fields[0] == "finish": exit_cmd(fields)
    else:
        new_pid = os.fork()
        runCmd(fields, new_pid)
