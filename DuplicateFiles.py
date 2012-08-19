"""Find duplicate files inside a directory tree."""

from os import walk, remove, stat
from os.path import join as joinpath
from md5 import md5

def find_duplicates( rootdir ):
    """Find duplicate files in directory tree."""
    filesizes = {}
    # Build up dict with key as filesize and value is list of filenames.
    for path, dirs, files in walk( rootdir ):
        for filename in files:
            filepath = joinpath( path, filename )
            filesize = stat( filepath ).st_size
            filesizes.setdefault( filesize, [] ).append( filepath )
    unique = set()
    duplicates = [] 
    # We are only interested in lists with more than one entry.
    for files in [ flist for flist in filesizes.values() if len(flist)>1 ]:
        for filepath in files:
            with open( filepath ) as openfile:
                filehash = md5( openfile.read() ).hexdigest()
            if filehash not in unique:
                unique.add( filehash )
            else:
                duplicates.append( filepath )
    return duplicates

if __name__ == '__main__':
    from argparse import ArgumentParser
    from DuplicatesDeletion import duplicates_gui
    
    PARSER = ArgumentParser( description='Finds duplicate files.' )
    PARSER.add_argument( '-gui', action='store_true', 
			 help='Display graphical user interface.' )
    PARSER.add_argument( '-root', metavar='<path>', default = '', help='Dir to search.' )
    PARSER.add_argument( '-remove', action='store_true', 
                         help='Delete duplicate files.' )
    ARGS = PARSER.parse_args()

    if ARGS.gui == True:
        app  =  duplicates_gui()
	app.setroot(ARGS.root)
	app.master.title("DuplicatesDeletion")
	app.mainloop()
    else:
	if ARGS.root == '':
	    PARSER.print_help()
	else:
            DUPS = find_duplicates( ARGS.root )
	    print '%d Duplicate files found.' % len(DUPS)
            for f in sorted(DUPS):
                if ARGS.remove == True:
                    remove( f )
                    print '\tDeleted '+ f
                else:
                    print '\t'+ f

