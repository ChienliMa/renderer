"""
This script with help you extract downloaded zip files.
"""

from __future__ import print_function
import os
import zipfile

def transfer( src, dst, delete = False ):
    """
    Extrace all zip files in src to dst
    -------------------------
    Parameters:
        src - String, source folder 
        dst - String, output folder
    -------------------------
    Returns:
        None
    """
    for file_name in os.listdir(src):
        if file_name.split('.') == 'zip':
            try:
                print ("Extracting \'%s\'" % file_name, end='')
                zip_ref = zipfile.ZipFile( os.path.join( src, file_name ), 'r')
                zip_ref.extractall( dst)
                zip_ref.close()
                print('  Done!')
                if delete:
                    print( "Delete: %s" % file_name )
                    os.remove( os.path.join( src, file_name ))
            except:
                print(' ###Error encounterd, passed!###')

def clean( dst, extension = ['ttf','TTF'] ):
    """
    Delete files in dst with unexpected extension name.
    -----------------
    Parameters:
        dst - folder to be clean
        extension - expected extension name
    -----------------
    Returns:
        None
    """
    for file_name in os.listdir(dst):
        if file_name.split('.') not in extension:
            print( "Delete \'%s\'" % file_name )
            os.remove( os.path.join(dst, file_name) )


if __name__ == '__main__':
    src = './zips/'
    dst = './fonts_1/'
    transfer( src, dst )
    clean( dst )