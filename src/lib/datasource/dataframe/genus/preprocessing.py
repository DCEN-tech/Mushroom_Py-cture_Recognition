# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from datasource.image.path import getImageFilepath


def ensuring_image_unicity(df_genus):

   print('\nPreprocessing step: [ Ensuring image unicity ] in progress...')

   # Retrieving the number of distinct images in the DataFrame
   nbDistImages_before = df_genus['image_id'].nunique()

   # Retrieving the number of entries in the DataFrame
   nbEntries_before = df_genus.shape[0]

   # Removing all rows corresponding with images associated with multiple genus
   df_filtered = df_genus.drop_duplicates(subset = 'image_id', keep = False, inplace = False, ignore_index = False)

   # Retrieving the number of distinct images in the DataFrame
   nbDistImages_after = df_filtered['image_id'].nunique()

   # Retrieving the number of entries in the DataFrame
   nbEntries_after = df_filtered.shape[0]

   # Printing results
   print('Results:')
   print('   Number of distinct images in the DataFrame:')
   print('      before : ', nbDistImages_before)
   print('         now : ', nbDistImages_after)
   print('   Number of entries in the DataFrame:')
   print('      before : ', nbEntries_before)
   print('         now : ', nbEntries_after)
   print('Done.')

   return df_filtered



def redefine_index(df_genus):
   print('\nPreprocessing step: [ Setting "image_id" column as index ] in progress...')
   # Setting the column 'image_id' as index for our DataFrame
   df_updated = df_genus.set_index(
         keys = 'image_id'
      ,  drop = False
      ,  append = False
      ,  inplace = False
      ,  verify_integrity = True
   )
   print('Results:')
   print(f'   Dataframe Index names: {df_updated.index.names}')
   print('Renaming index labels: "image_id" -> "id":')
   df_updated.index.rename('id', inplace = True)
   print(f'   Dataframe Index names: {df_updated.index.names}')
   print('Done.')
   return df_updated



def add_col_filepath(df_genus, image_root_dir):
   print('\nPreprocessing step: [ Adding column "image_filepathid" ] in progress...')
   # Adding column: image_filepath
   df_genus.loc[:,'image_filepath'] = \
      df_genus['image_id'].apply( \
            func = getImageFilepath
         ,  args = ('jpg', image_root_dir)
      )
   print('Results:')
   print(f'   Dataframe cols: {df_genus.columns}')
   print('Done.')

'''
def one_hot_encode_label(df_genus):
    print('\nPreprocessing step: [ One Hot Encoding the labels "taxon_name" ] in progress...')
    df_ohe = pd.get_dummies(
            data       = df_genus['taxon_name']
        ,   prefix     = None
        ,   prefix_sep = None
        ,   dummy_na   = False
        ,   columns    = ['taxon_name']
        ,   sparse     = False
        ,   drop_first = False
        ,   dtype      = np.uint8
    )
    df_genus = df_genus.join(
            other = df_ohe
        ,   how = 'inner'
        ,   lsuffix = '_1'
        ,   rsuffix = '_2'
    )
    print('Results:')
    print(f'   Dataframe cols: {df_genus.columns}')
    print('Done.')

    return df_genus
'''


def one_hot_encode_label(df_genus):
    print('\nPreprocessing step: [ One Hot Encoding the labels "taxon_name" ] in progress...')
    df_ohe = pd.get_dummies(
            data       = df_genus['taxon_name']
        ,   prefix     = None
        ,   prefix_sep = None
        ,   columns    = ['taxon_name']
        ,   sparse     = False
        ,   drop_first = False
        ,   dtype      = np.uint8
    )

    label_col = df_ohe.apply(lambda x: np.array(x.values), axis = 1)

    label_col.rename('label', inplace = True)

    df_genus = df_genus.join(
            other = label_col
        ,   how = 'inner'
        ,   lsuffix = '_1'
        ,   rsuffix = '_2'
    )
    print('Results:')
    print(f'   Dataframe cols: {df_genus.columns}')
    print('Done.')

    return df_genus



def checkStatus(b_ret):
   if b_ret:
      status = 'OK'
   else:
      status = 'FAILED'
   print(f'Check status: {status}')
   if not b_ret:
      raise Error(f'Preprocessing check failed !')



def check_image_unicity(df_genus):
   print('\nCheck step: [ Image unicity ] in progress...')
   nbImages  = df_genus['image_id'].nunique()
   nbSamples = df_genus.shape[0]
   print(f'distinct images: {nbImages}')
   print(f'        samples: {nbSamples}')
   return (nbImages == nbSamples)



def check_filepath_col(df_genus):
   print('\nCheck step: [ Adding column "image_filepathid" ] in progress...')
   print(f'Columns: {df_genus.columns}')
   return ('image_filepath' in df_genus.columns)



def preprocessing(df_genus, image_root_dir):
   # Ensuring image unicity
   df_updated = ensuring_image_unicity(df_genus)
   # Redifine index
   df_updated = redefine_index(df_updated)
   # Adding column image_filepath
   add_col_filepath(df_updated, image_root_dir)
    # One hot encoding the labels
   df_updated = one_hot_encode_label(df_updated)
   return df_updated



def preprocessing_check(df_genus):

   # check: image unicity
   b_ret = check_image_unicity(df_genus)
   checkStatus(b_ret)

   # Check col "image_filepath" exists
   b_ret = check_filepath_col(df_genus)
   checkStatus(b_ret)

