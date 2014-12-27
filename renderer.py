import os
import pygame
import numpy as np
from matplotlib import pyplot as plt
from scipy import misc

class renderer( object ):
  def __init__( self, texts  ):
    pygame.init()

    self.texts = texts
    
    self.fonts = os.listdir('./fonts')
    self.bgs = os.listdir('./bgs')
    self.num_of_fonts = len(self.fonts)

    
  def init_surface( size = (800,600) ):
    '''
    Function:initialize window
    '''    
    pygame.init()
    display_surface = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Text renderer')
    return display_surface

  def start( self, sample_per_word, refresh_frequency , out_path ):
    """
    need an auto stop
    font size = single word size in pixel
    """
    self.surface = self.init_surface()

    for bg in self.bgs:
      # refresh background image
      bg = pygame.image.load('./bgs/' + bg ).convert()
      for i in xrange(refresh_frequency):
        self.surface.blit( bg, (0,0) )

        pairs = []
        for text in self.texts:
          # random font random size
          font_name = self.fonts[ np.random.randint(0,self.num_of_fonts) ]
          size = np.random.randint(30,60)
          font = pygame.font.Font( './fonts/'+font_name ,  size )

          # random color, ascding, angle
          # for color ,we create it in hsv color space than transfer into rgb
         
          # render text and set location
          text_surface = font.render(text, False, (255,0,0))
          
          text_rect = text_surface.get_rect()
          # we may need to inverse x and y
          text_h = size
          text_w = len(text) * size
          text_rect.x = np.random.randint(0, 800 - text_w )
          text_rect.y = np.random.randint(0, 600 - text_w )  
          pairs.append( [ text, text_rect ] )

          self.surface.blit( text_surface, text_rect )

        # finish one frame, extract text array
        img =  np.array( pygame.surfarray.array3d( self.surface ) )
        for pair in pairs:
          text, rect = pair
          text_img = img[ rect.x:rect.x+rect.width, rect.y:rect.y+rect.height, : ]
          # extract and save
          plt.imshow(text_img.swapaxes(0,1))
          plt.show()
          print text

if __name__ == '__main__':
  ren = renderer(['FOO', 'BAR', 'Coke Cola'])
  ren.start(3,3,'fd')