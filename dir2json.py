#!/usr/bin/env python3

import argparse
from datetime import datetime
import glob
import json
import os
from os.path import exists, join
import sys

def glob_list(folder, outfile, match):
    glob_string = join(folder, "**", match)
    records = []
    file_count = 0
    start_time = datetime.now()
    try:
        with open(outfile, 'w') as out_f:
            for afile in glob.glob(glob_string, recursive=True):
                afile = afile.replace('\\', '/')
                file_info = os.stat(afile)
                m_dt = datetime.fromtimestamp(int(file_info.st_mtime))
                m_str = m_dt.astimezone().strftime("%Y:%m:%d %H:%M:%S%z")
                c_dt = datetime.fromtimestamp(int(file_info.st_ctime))
                c_str = c_dt.astimezone().strftime("%Y:%m:%d %H:%M:%S%z")
                file_rec = {
                    "SourceFile": afile,
                    "FileModifyDate": m_str,
                    "FileCreateDate": c_str,
                    "FileSize": file_info.st_size
                }
                records.append(file_rec)
                file_count += 1
            out_f.write(json.dumps(records, indent=0))
            if file_count % 500 == 0:
                curr_time = datetime.now()
                total_mins = (curr_time - start_time).seconds/60.
                print(f"processed: {file_count} files so far in {total_mins} minutes.")
    except Exception as e:
        print(f"ERROR: {e}")
        return
    end_time = datetime.now()
    total_secs = (end_time - start_time).seconds
    total_mins = total_secs/60.
    print(f"Found {file_count} files in {total_mins} minutes.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find files in folder and subfolders and write listing to JSON')
    parser.add_argument('--folder', '-f', dest='folder', action='store',
                        help='folder to find files for listing')
    parser.add_argument('--outfile', '-o', dest='outfile', action='store',
                        help='outfile JSON file to write listing')
    parser.add_argument('--match', '-m', dest='match', action='store',
                        help='filename pattern to match (detault: *)') 
    parser.set_defaults(match='*')
    args = parser.parse_args()

    if not args.folder:
        parser.print_help(sys.stderr)
        sys.exit(0)
    
    glob_list(
        folder=args.folder,
        outfile=args.outfile,
        match=args.match
    )
      
    
