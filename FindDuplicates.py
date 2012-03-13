"""Find duplicate files inside a directory tree."""

from os import walk, remove, stat
from os.path import join as joinpath
from md5 import md5
import threading
import Queue
import time
import sys

class Scanner(threading.Thread):
    def __init__(self, path, queue, finished_scan):
        threading.Thread.__init__(self)
        self._path = path
        self._queue = queue
        self._finished_scan = finished_scan

    def run(self):
        """Find duplicate files in directory tree and return array with lists of duplicateted files."""
        filesizes = {}
        # Build up dict with key as filesize and value is list of filenames.
        for path, dirs, files in walk( self._path ):
            for filename in files:
                filepath = joinpath( path, filename )
                filesize = stat( filepath ).st_size
                filesizes.setdefault( filesize, [] ).append( filepath )


        #Compare content hash of all files which have the same size
        #if two or more files have same hash and size they are added to the queue     
        for files in [ flist for flist in filesizes.values() if len(flist)>1 ]:
            #run over all files in dir with the same size if there is more then one
            duplicates = {}
            for filepath in files:
                with open( filepath ) as openfile:
                    filehash = md5( openfile.read() ).hexdigest()
                if filehash not in duplicates:
                    duplicates.setdefault(filehash, []).append (filepath)
                else:
                    duplicates[filehash].append(filepath)
            for duplicate in [ duplicate for duplicate in  duplicates.values() if len(duplicate)>1 ]:
                self._queue.put(duplicate)
        self._finished_scan[0] = 1

class Updater(threading.Thread):
    
    def __init__(self, queue, duplicates, updateFunction, finished_scan, time):
        threading.Thread.__init__(self)
        self._queue = queue
        self._updateFunc = updateFunction
        self._duplicates =duplicates
        self._finished_scan = finished_scan
        self._time_duration = time

    def run(self):

        while True:
            try:
                item = self._queue.get(True,0.03)         #  seems to be a good time value
            except Queue.Empty:
                #if queue is empty and scan is finished then stop this thread
                if self._finished_scan[0] == 1:
                    self._time_duration = time.time() - self._time_duration
                    print  'Finished in ' + repr(self._time_duration) + ' seconds!'
		    self._updateFunc()
                    break
                else:
                    continue

            self._duplicates.append(item)
            self._queue.task_done()
            self._updateFunc()
