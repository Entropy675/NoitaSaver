#!/usr/bin/env python

import os
import subprocess
import argparse
import shutil
import time
from datetime import datetime

# Config:
savesPath = os.path.join(os.getcwd(), 'saves')
backupPathName = 'autosave'
backupPath = os.path.join(savesPath, backupPathName)
saveFolder = os.path.join(os.getcwd(), 'save00')
autosavePollingRate = 5 # mins

def drawGreeting():
    print("A lightweight Noita saver. Takes away all surprises.")
    print("Noita is a very punishing game, its difficult to imagine getting far without great effort. This tool eases the quest!")
    print("Includes features such as an autosave system, a backup save whenever you overwrite ")
    print("Have fun - Entropy")

def moveData(saveFrom, saveTo):
    try:
        if os.path.exists(saveTo):
            saveName = os.path.basename(saveTo)
            try:
                saveName = saveName.split["."][0]
            except TypeError as e:
                pass
            if saveName != "BACK" and saveTo != saveFolder:
                print(f"Saving old file to backup path: {backupPath}")
                moveData(saveTo, os.path.join(backupPath, f"BACK.{os.path.basename(saveTo)}.{datetime.now().strftime('%H_%M_%S')}"))

            shutil.rmtree(saveTo)
        print(f"Moving {saveFrom} to {saveTo}")
        shutil.copytree(saveFrom, os.path.join(os.getcwd(), "TEMP"))
        shutil.move(os.path.join(os.getcwd(), "TEMP"), saveTo)
    except FileNotFoundError:
        print("Source file not found.")
    except PermissionError:
        print("Permission error. Make sure you have the required permissions.")
    #except Exception as e:
        #print(f"An error occurred: {e}")

def save(args):
    if ensureSavesFolderExists():
        drawGreeting();
    
    saveTo = os.path.join(savesPath, args.name)
    print(f"Saving to: {saveTo}")
    moveData(saveFolder, saveTo)

def load(args):
    print(f"Loading from save: {args.name}")   
    
    loadSave = os.path.join(savesPath, args.name)
    if not os.path.exists(loadSave):
        print("The name you chose was not found.")
        list();
        return;
    
    if args.name != "BACK":
        backupSave = os.path.join(savesPath, "BACK")
        print(f"Saving current save to backup file: {saveFolder} -> {backupSave}")
        moveData(saveFolder, backupSave);
    
    print(f"Loading file: {loadSave} -> {saveFolder}")
    moveData(loadSave, saveFolder)

def list(args=None):

    files = None
    saveLists = 2
    
    try:
        files = os.listdir(savesPath)
    except FileNotFoundError:
        if not ensureSavesFolderExists():
            print("Could not list directory: Directory does not exist and could not be created.")
    if files:
        print("List of saves:")
        for save in files:
            if os.path.join(savesPath, save) == backupPath:
                continue
            print(f"  {save.ljust(25)} |\t (Last Modified: {datetime.fromtimestamp(os.path.getmtime(os.path.join(savesPath, save)))})");
    else:
        saveLists -= 1
    
    try:
        files = os.listdir(backupPath)
    except FileNotFoundError:
        if not ensureSavesFolderExists():
            print("Could not list directory: Directory does not exist and could not be created.")
    if files:
        print("List of backup saves:")
        for save in files:
            print(f"  {save.ljust(25)} |\t (Last Modified: {datetime.fromtimestamp(os.path.getmtime(savesPath + save))})");
    else:
        saveLists -= 1
    
    if not saveLists:
        print("No saves currently stored.")

def ensureSavesFolderExists():
    if os.path.exists(savesPath):
        return False
    try:
        os.makedirs(savesPath)
        os.makedirs(backupPath)
        print(f"Folder '{savesPath}' created.")
        print(f"Folder '{backupPath}' created.")
        return True
    except OSError as e:
        print(f"Error creating folder '{savesPath}': {e}")
        return False

def autosave(args):
    print(f"Entering autosave mode with {args.name} file.")
    while True:
        save(args)
        time.sleep(args.interval * 60)  # Convert minutes to seconds

def delete(args):
    normalSave = os.path.join(savesPath, args.name)
    if os.path.exists(normalSave):
        print(f"Removing {normalSave}")
        shutil.rmtree(normalSave)
    
    backupSave = os.path.join(backupPath, args.name)
    if os.path.exists(backupSave):
        print(f"Removing {backupSave}")
        shutil.rmtree(backupSave)

def help(args):
    
    if ensureSavesFolderExists():
        drawGreeting();
    # Instructions for different commands go here
    
    runname = os.path.basename(__file__).split(".")[0];
    
    commandList = [
    f"""
{runname} help:
    Displays this manual.
    """,
    f"""
{runname} save [name]:
    Saves current progress to the name specified. 
    """,
    f"""
{runname} autosave [name] [interval]:
    Saves current progress to the name specified, repeating on a specified number of minutes, default {autosavePollingRate}. 
    """,
    f"""
{runname} load [name]:
    Loads the save with given name, if it doesn't exist
    it lists the ones that do (same as list) and does
    nothing else.
    """,
    f"""
{runname} delete [name]:
    Deletes any save with the given name.
    """,
    f"""
{runname} list:
    Lists the saves locally stored in specified folder.
    """,
    f"""
{runname} run:
    Runs the game.
    """
    ]
    
    for command in commandList:
        print(command)
    return 0;

def run(args):
    subprocess.run(["start", "cmd", "/c", f"start steam://run/881100"], shell=False)

def main():
    parser = argparse.ArgumentParser(description='Profile saver for Faster Than Light')
    subparsers = parser.add_subparsers(title='commands', dest='command')
    
    # Define commands here
    parserHelp = subparsers.add_parser('help', help='Displays commands.')
    parserHelp.set_defaults(func=help)
    
    parserSave = subparsers.add_parser('save', help='Makes a save with a name, like: \'save game2\' or \'save superawesomerun\'.')
    parserSave.add_argument('name', type=str, default="NEW", help='Name of save file (default is [NEW])')
    parserSave.set_defaults(func=save)
    
    parserAutosave = subparsers.add_parser('autosave', help=f'Saves current progress to the name specified, repeating on a specified number of minutes, default {autosavePollingRate}.')
    parserAutosave.add_argument('name', type=str, default="NEW", help='Name of save file (default is [NEW])')
    parserAutosave.add_argument('interval', type=int, default=autosavePollingRate, help='Interval in minutes before saving again.')
    parserAutosave.set_defaults(func=autosave)
    
    parserLoad = subparsers.add_parser('load', help='Loads the given name if such file exists, otherwise does list.')
    parserLoad.add_argument('name', type=str, default="NEW", help='''
Loads the save with given name, if it doesn't exist
it lists the ones that do (same as list) and does
nothing else.'''
    )
    parserLoad.set_defaults(func=load)
    
    parserDelete = subparsers.add_parser('delete', help='Deletes a save with a name, like: \'delete game1\' or \'delete superbadrun\'.')
    parserDelete.add_argument('name', type=str, default="NEW", help='Name of save file (default is [NEW])')
    parserDelete.set_defaults(func=delete)
    
    parserList = subparsers.add_parser('list', help='Lists the saves locally stored in specified folder. ')
    parserList.set_defaults(func=list)
    
    parserStart = subparsers.add_parser('run', help='Starts the game through steam api.')
    parserStart.set_defaults(func=run)


    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
        
    
if __name__ == '__main__':
    main()