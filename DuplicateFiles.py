#!/usr/bin/env python2

"""Find duplicate files inside a directory tree."""

from os import walk, remove, stat
from os.path import join as joinpath
from md5 import md5
from argparse import ArgumentParser
from DuplicatesDeletion import duplicates_gui


ARGP = ArgumentParser(description='Finds duplicate files.')
ARGP.add_argument('-gui', action='store_true',
                    help='Display graphical user interface.')
ARGP.add_argument(
    '-root',
    metavar='<path>',
    default='',
    help='Dir to search.')
ARGP.add_argument('-remove', action='store_true',
                    help='Delete duplicate files.')

def find_duplicates(rootdir):
    """Find duplicate files in directory tree."""
    filesizes = {}
    # Build up dict with key as filesize and value is list of filenames.
    for path, _, files in walk(rootdir):
        for filename in files:
            filepath = joinpath(path, filename)
            filesize = stat(filepath).st_size
            filesizes.setdefault(filesize, []).append(filepath)
    unique = set()
    duplicates = []
    # We are only interested in lists with more than one entry.
    for files in [flist for flist in filesizes.values() if len(flist) > 1]:
        for filepath in files:
            with open(filepath) as openfile:
                filehash = md5(openfile.read()).hexdigest()
            if filehash not in unique:
                unique.add(filehash)
            else:
                duplicates.append(filepath)
    return duplicates

def main():
    """Main CLI tool."""
    argp = ARGP.parse_args()

    if argp.gui:
        app = duplicates_gui()
        app.set_root(argp.root)
        app.master.title("DuplicatesDeletion")
        app.mainloop()
    else:
        if argp.root == '':
            ARGP.print_help()
        else:
            duplicates = find_duplicates(argp.root)
            print '%d Duplicate files found.' % len(duplicates)
            for file_path in sorted(duplicates):
                if argp.remove:
                    remove(file_path)
                    print '\tDeleted ' + file_path
                else:
                    print '\t' + file_path

if __name__ == '__main__':
    main()
