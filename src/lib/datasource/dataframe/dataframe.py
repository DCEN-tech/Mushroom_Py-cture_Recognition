# -*- coding: utf-8 -*-

import os
import pandas as pd

def load_data(filePath):

    # Vérification
    if not filePath:
        raise Exception('[load_data]: parameter <filePath> is not set')
    if not os.path.isfile(filePath):
        raise Exception(f'File not found: {filePath}')

    df = pd.read_csv( \
            filepath_or_buffer = filePath
        ,   sep = ','
        ,   header = 0
    )
    print('\nDataFrame Loading Done.')

    return df



def checkImageFiles(
      dataframe
   ,  col_filename = 'image_filepath'
   ,  imageFileRootDir = None
):
   """
   DESCRIPTION
      This function checks that a file corresponding to each mushroom image of the Pandas dataframe <dataframe> really
      exists.

   PARAMETERS
         dataframe
               this is expected to be a Pandas dataframe containing a column whose name is given by parameter
               <col_filename>.
               This function will then check that each file whose path is given by:
                  - imageFileRootDir + dataframe[col_filename]   if imageFileRootDir is not None
                  - dataframe[col_filename]                      if imageFileRootDir is None

         col_filename
               should indicate the name of the <dataframe> that contains the path of the file that must be checked for
               existence.

               corresponding image (assuming that each line of the dataframe <dataframe> should correspond to an image).
         imageFileRootDir
               If not None, its value will become the prefix of the file path that will be checked for existence.
               If set to None (the default), then the file path that will be checked, is the path stored inside
               dataframe[col_filename] column, expecting that this value corresponds to a RELATIVE path to the current
               Python working directory.

   RETURN
      This function will return the following Pandas Series:  missingFiles
      missingFiles will have the same number of rows as <dataframe>.
      missingFiles will contain:
         True  for all rows for which the file path does not exist
         False for all rows for which the file path does exist
      missingFiles can be used to index <dataframe> because the rows between the two match.
   """
   def _checkImageFile(filepath):
      if (imageFileRootDir is not None):
         return os.path.isfile(os.path.join(imageFileRootDir, filepath))
      return os.path.isfile(os.path.join(filepath))

   if not isinstance(dataframe, pd.DataFrame):
      raise TypeError('Invalid type for parameter <dataframe>: "pd.DataFrame" was expected')

   if not isinstance(col_filename, str):
      raise TypeError('Invalid type for parameter <dataframe>: "str" was expected')

   if ((imageFileRootDir is not None) and (not isinstance(imageFileRootDir, str))):
      raise TypeError('Invalid type for parameter <dataframe>: "str" was expected')

   res = dataframe[col_filename].apply(_checkImageFile)
   idxMissingFiles = (~res).copy()

   return idxMissingFiles

