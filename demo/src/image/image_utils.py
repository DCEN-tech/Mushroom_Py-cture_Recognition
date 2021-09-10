# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import requests
from PIL import Image


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def loadImage(filepath):
   '''
   DESCRIPTION
         This function loads an image content whose file hook is given by <imgFile>.
   ARGUMENT(S)
         filepath
            the full path name of the file.
   RETURN
         A PIL.Image object.
   '''
   return Image.open(fp = filepath, mode = 'r')



def loadImageFromUrl(url):
   return Image.open(requests.get(url, stream=True).raw)
