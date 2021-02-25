import os
import glob
import shutil
import pwd
import sys
import time


# Simple shell
# COMMANDS          ERRORS CHECKED
# 1. info XX         - check file/dir exists
# 2. files
# 3. delete  XX      - check file exists and delete succeeds
# 4. copy XX YY      - XX exists, YY does not exist, copy succeeds
# 5. where
# 6. down DD         - check directory exists and change succeeds
# 7. up              - check not at the top of the directory tree - can't go up from root
# 8. finish


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
            # If you do not have permissions to delete a file, an error message is printed
            except PermissionError:
                print("Operation not permitted: You do not have permission to delete: "+ fields[1])
            except OSError:
                print("Error: You cannot delete a directory with this command.")
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
                # If you do not have permissions to copy a file, an error message is printed
                except PermissionError:
                    print("Operation not permitted: You do not have permission to copy: "+ fields[1])
                except IsADirectoryError:
                    print("Error: You cannot copy a directory with this command.")
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
            # If you do not have permissions to read a directory, an error message is printed
            except PermissionError:
                print("Operation not permitted: You do not have permission to view the directory: "+ fields[1])
            except NotADirectoryError:
                print(fields[1] + " is not a directory")
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
    if numArgs == num: return True
    if numArgs > num: print("Unexpected argument", fields[num+1], "for command", fields[0])
    else: print("Missing argument for command", fields[0])
    return False

# ----------------------------------------------------------------------------------------------------------------------

while True:
    line = input("PShell>")
    fields = line.split()
    # split the command into fields stored in the fields list
    # fields[0] is the command name and anything that follows (if it follows) is an argument to the command

    if fields[0] == "files": files_cmd(fields)
    elif fields[0] == "info": info_cmd(fields)
    elif fields[0] == "delete": delete_cmd(fields)
    elif fields[0] == "copy": copy_cmd(fields)
    elif fields[0] == "where": where_cmd(fields)
    elif fields[0] == "up": up_cmd(fields)
    elif fields[0] == "down": down_cmd(fields)
    elif fields[0] == "finish": exit_cmd(fields)
    else: print("Unknown command", fields[0])
