import pickle
import renderer
import pygame
from scipy import misc
import numpy as np
from numpy.random import randint
import os

def run_example( font_path, bg_path, out_path, color_file, texts, max_imgs ):
    """
    Run the sample and the result is saved as 'result.jpg'
    """
    # init pygame to utilize its renderer
    pygame.init()

    # get base color, fonts and background images
    color_file = open( color_file )
    colors = pickle.load( color_file )
    n_colors = len( colors )
    color_file.close()

    fonts = os.listdir( font_path )
    n_fonts = len(fonts)
    
    bgs = os.listdir( bg_path )
    n_bgs = len(bgs)

    index = 0
    error = 0
    misson_stop = False
    while index < max_imgs and not misson_stop:

        bg = bgs[ randint(0,n_bgs) ]    
        if bg[-3:] != 'jpg':
            continue
        bg = misc.imread( os.path.join( bg_path, bg ))
        for text in texts:
            print "%05d"%index, text
            # random elements
            color = colors[ randint(0,n_colors) ]
            font_name = fonts[ randint(0,n_fonts) ]
            font = os.path.join( font_path, font_name )

            try:
                a = renderer.render( text, font, color, bg, 48 ).astype('uint8')            
                misc.imsave( os.path.join(out_path, text+"%05d"%index+'.jpg'), a )
                index += 1
            except: 
                print 'error',error
                error += 1
                if error >= 20:
                    misson_stop = True
                    break

if __name__ == '__main__':
    texts = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    run_example( './fonts', './bgs', './result', 'color.pickle', texts, 20)

