"""Core functionality for directory synchronisation using FolderSync."""

import os
import shutil
from pathlib import Path
from filecmp import dircmp


def sync_directories(src: str, dst: str, dry_run: bool = False) -> None:
    """
    Synchronise files from src to dst.

    This will make the destination directory match the source directory
    by copying new/updated files and removing files not in source.
    """
    src_path = Path(src).resolve()
    dst_path = Path(dst).resolve()

    if not src_path.is_dir():
        raise ValueError(f"Source path {src} is not a directory.")
    if not dst_path.is_dir():
        raise ValueError(f"Destination path {dst} is not a directory.")

    # _sync_recursive will return a list of actions performed
    actions = _sync_recursive(src_path, dst_path, dry_run)

    # Only print the summary and ASCII art if actual changes were made
    # and we are not in dry_run mode.
    if actions and not dry_run:
        # Print all actions
        for action_message in actions:
            print(action_message)

        # Print ASCII art once
        print("Very Nice, Borat Approves!")
        print(r"""
                                                                              
                                                                                   
                                                                                
                                    ./*,*/(//                                   
                               .,#/&@@@@@@@&@@&@@,                              
                             ##%%&@@@@&&&@@@&@@@@@#*,                           
                            .@@&@@&&##(######%(#&&@@&*/                         
                            #@@@@@%///*,,.. .,,***&&@@@@                        
                            /@@@@@%(/**,,,..,.,,**(&@@@&                        
                             .(@@@##%#/*,....,,,,*(@@@/                         
                              %##%@@@@@@@&*#@&@&&%%%#                           
                                ##%%%%%%#*,,#%%%%((,                            
                                /###//,**/,,,////,/                             
                                 ,#(%%%%@&%&%###//                              
                                  %#/##%/.,*,//%*,                              
                                   ##,//*//*,,.//                               
                                 &@###/*,,,,,**,*                               
                               #/&&&%#######(*,*#,                              
                         ,.,,,,,,#/#&&&%((**(((((,,,,                           
                  ,,,,,...,.,,,,,,/*/((***.//(/*/,.......,,                     
             *,,,,,......,..,,,,,./(*/&%/,*(&**(.............,,,,               
           *,.,,,,,,,...,#......,.,**//#/,.(///,...............*.,.,.           
          .*,...,.,,,,..........,..***//,..//*#.......*...,...,*,,.,.,          
          /,,,.,*,.,,,,,,...**......**,,.,.,/*...............*........          
          *,,,..*,,,****,**....***,.**,,,..,/,..(...........(/........,         
         **,,.,,,..,.....,,.....,,%#,*..,...#.........((....*(*........         
         (#,.(((,.......,,............,.............../((.....(***....,.        
        */*,,.(##,,.....*,...*.............*........*((((((,...#*,*,,(..        
        /*,,,#@&%##(/((..,,...(...........*.........(((((((((...(###(,,..       
        *,,,**@#((###(...,,....(..........,..........(((((#((((*##/*,,#,,       
       *******(@@%%%&,...,......(........(............((((((((##(&/,*#*,,       
      **(***/*/(/*/%#....,,......(.....,/...............,((((#%%(/#/%%.,,,      
     ,,((**/(/((((#%.,...,........(,...,(................,.(#%%#(/#(%%,,,,,     
     ,**//*/((.(&&%*,,..,,,........(/..,,................,,##%%#((#*.(,,,,,.    
    ,****#/(#&##((*,*,..,,,,........((.(................,,*#%#%#((#(##(*,,,,    
     %,(*#/(##((/**%*,,.,,,,.........,(,................,,## #%##(((#/**,,,     
    """)


def _sync_recursive(src_path: Path, dst_path: Path, dry_run: bool) -> list[str]:
    actions = []
    comparison = dircmp(src_path, dst_path)

    # Files in source but not in destination
    for filename in comparison.left_only:
        src_file = src_path / filename
        dst_file = dst_path / filename
        if src_file.is_dir():
            if dry_run:
                print(f"Would copy directory '{src_file}' to '{dst_file}'")
            else:
                shutil.copytree(src_file, dst_file)
                actions.append(f"Copied directory '{src_file}' to '{dst_file}'")
        else:
            if dry_run:
                print(f"Would copy file '{src_file}' to '{dst_file}'")
            else:
                shutil.copy2(src_file, dst_file)
                actions.append(f"Copied file '{src_file}' to '{dst_file}'")

    # Check common files for differences
    for filename in comparison.common_files:
        src_file = src_path / filename
        dst_file = dst_path / filename
        if not _files_are_equal(src_file, dst_file):
            if dry_run:
                print(f"Would update '{dst_file}' from '{src_file}'")
            else:
                shutil.copy2(src_file, dst_file)
                actions.append(f"Updated '{dst_file}' from '{src_file}'")

    # Files in destination not in source
    for filename in comparison.right_only:
        dst_file = dst_path / filename
        if dst_file.is_dir():
            if dry_run:
                print(f"Would remove directory '{dst_file}'")
            else:
                shutil.rmtree(dst_file)
                actions.append(f"Removed directory '{dst_file}'")
        else:
            if dry_run:
                print(f"Would remove file '{dst_file}'")
            else:
                dst_file.unlink()
                actions.append(f"Removed file '{dst_file}'")

    # Recursively sync subdirectories
    for common_dir in comparison.common_dirs:
        sub_actions = _sync_recursive(src_path / common_dir, dst_path / common_dir, dry_run)
        actions.extend(sub_actions)

    return actions


def _files_are_equal(file1: Path, file2: Path) -> bool:
    # Quick checks: size, then content if needed.
    if file1.stat().st_size != file2.stat().st_size:
        return False

    with file1.open("rb") as f1, file2.open("rb") as f2:
        chunk_size = 8192
        while True:
            b1 = f1.read(chunk_size)
            b2 = f2.read(chunk_size)
            if b1 != b2:
                return False
            if not b1:  # End of file
                break
    return True
