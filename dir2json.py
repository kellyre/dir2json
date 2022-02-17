#!/usr/bin/env python3

import argparse
from datetime import datetime
import glob
import json
import os
from os.path import exists, join, split, isdir, isfile
import sys

IMAGE_EXT_LIST = [
    'ase', 'art', 'bmp', 'blp', 'cd5', 'cit', 'cpt', 'cr2', 'cut',
    'dds', 'dib', 'djvu', 'egt', 'exif', 'gif', 'gpl', 'grf', 'icns',
    'ico', 'iff', 'jng', 'jpeg', 'jpg', 'jfif', 'jp2', 'jps', 'lbm',
    'max', 'miff', 'mng', 'msp', 'nef', 'nitf', 'ota', 'pbm', 'pc1',
    'pc2', 'pc3', 'pcf', 'pcx', 'pdn', 'pgm', 'PI1', 'PI2', 'PI3',
    'pict', 'pct', 'pnm', 'pns', 'ppm', 'psb', 'psd', 'pdd', 'psp',
    'px', 'pxm', 'pxr', 'qfx', 'raw', 'rle', 'sct', 'sgi', 'rgb',
    'int', 'bw', 'tga', 'tiff', 'tif', 'vtf', 'xbm', 'xcf', 'xpm',
    '3dv', 'amf', 'ai', 'awg', 'cgm', 'cdr', 'cmx', 'dxf', 'e2d',
    'egt', 'eps', 'fs', 'gbr', 'odg', 'svg', 'stl', 'vrml', 'x3d',
    'sxd', 'v2d', 'vnd', 'wmf', 'emf', 'art', 'xar', 'png', 'webp',
    'jxr', 'hdp', 'wdp', 'cur', 'ecw', 'iff', 'lbm', 'liff', 'nrrd',
    'pam', 'pcx', 'pgf', 'sgi', 'rgb', 'rgba', 'bw', 'int', 'inta',
    'sid', 'ras', 'sun', 'tga', 'heic', 'heif']

VIDEO_EXT_LIST = [
    'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng',
    'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4',
    'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi',
    '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a',
    'f4b', 'mod']

def get_mime(afile):
    ext = split(afile)[-1].split('.')[-1].lower()
    if ext in VIDEO_EXT_LIST:
        return f"video/{ext}"
    if ext in IMAGE_EXT_LIST:
        return f"image/{ext}"
    else:
        return f"{ext}/{ext}"

def glob_list(folder, outfile, match, mime, dirs):
    glob_string = join(folder, "**", match)
    records = []
    file_count = 0
    start_time = datetime.now()
    try:
        with open(outfile, 'w') as out_f:
            for afile in glob.glob(glob_string, recursive=True):
                afile = afile.replace('\\', '/')
                if not dirs and isdir(afile):
                    continue
                elif not isfile(afile) and not isdir(afile):
                    continue
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
                if (mime):
                    file_rec['MIMEType'] = get_mime(afile)
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
    parser.add_argument('--mime', dest='mime', action='store_true',
                        help='add a MIMEType value based on file extention')
    parser.add_argument('--no-mime', dest='mime', action='store_false',
                        help='don\'t add a MIMEType value based on file extention')
    parser.add_argument('--dirs', dest='dirs', action='store_true',
                        help='include directories')
    parser.add_argument('--no-dirs', dest='dirs', action='store_false',
                        help='don\'t include directories')
    parser.set_defaults(match='*', mime=False, dirs=False)
    args = parser.parse_args()

    if not args.folder:
        parser.print_help(sys.stderr)
        sys.exit(0)
    
    glob_list(
        folder=args.folder,
        outfile=args.outfile,
        match=args.match,
        mime=args.mime,
        dirs=args.dirs
    )

