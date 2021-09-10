# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import os
import math
import numpy as np


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

MAX_CHILD_CNT = 1500
   # the max number of children in the file system arborescence

NAMELEN = 5
   # the length for any subdirectory
   # The name will be left-padded with '0' if needed to reach the length given by 'NAMELEN'.

DEFAULT_IMAGE_TYPE = 'jpg'



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def getImageFilepath(
      imageId
   ,  imageType    = DEFAULT_IMAGE_TYPE
   ,  imageRootDir = None
):
   '''
   DESCRIPTION
         The purpose of this function is to return the path corresponding to the file corresponding to any image whose
         the id has been given inside <imageId>.
         This function will produce the name of

         help keeping a reasonable number of images inside a directory.
         For this the objective is to dispatch images among many sub-directories with the following rule:
         each sub-directory will host a maximum of <MAX_CHILD_CNT> images.
         This fonction will return the name of the sub-directory that will host the image corresponding to the
         <imageId> identifier.
         The name of each subdirectory which will be returned by this function will be a string with a
         length equals to <NAMELEN>.

   ARGUMENTS
         imageId
            an integer corresponding to an identifier of an image.
   RETURN
      A string value that will correspond to the sub-directory name that will contain the image with the <imageId>
      identifier.
      The sub-directory will be located just inside the root directory that will contain all the images.
      The path of the parent directory will be managed outside of this function !
   '''

   if (imageRootDir is not None) and (not isinstance(imageRootDir, str)):
      raise TypeError('ERROR: Invalid type for argument <imageRootDir>: "string" or "None" type was expected')

   def subdirFromImageId(imageId):
      '''
      DESCRIPTION
            The purpose of this function is to help keeping a reasonable number of images inside a directory.
            For this the objective is to dispatch images among many sub-directories with the following rule:
            each sub-directory will host a maximum of <MAX_CHILD_CNT> images.
            This fonction will return the name of the sub-directory that will host the image corresponding to the
            <imageId> identifier.
            The name of each subdirectory which will be returned by this function will be a string with a
            length equals to <NAMELEN>.

      ARGUMENTS
            imageId
               an integer corresponding to an identifier of an image.
      RETURN
         A string value that will correspond to the sub-directory name that will contain the image with the <imageId>
         identifier.
         The sub-directory will be located just inside the root directory that will contain all the images.
         The path of the parent directory will be managed outside of this function !
      '''
      if ( MAX_CHILD_CNT <= 0 ):
         raise ValueError('ERROR: Invalid value for <MAX_CHILD_CNT> parameter: expected value must be > 0.')
      idx = math.ceil( imageId / MAX_CHILD_CNT )
      dirIdx = str(idx).zfill(NAMELEN)
      return dirIdx

   subdir   = subdirFromImageId(imageId)
   filename = str(imageId) + '.' + imageType

   filepath = os.path.join(subdir, filename)

   if (imageRootDir is not None):
      filepath = os.path.join(imageRootDir, filepath)

   return filepath
