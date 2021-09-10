# -*- coding: utf-8 -*-


def create_genus_from_mushrooms(df_mushrooms):

   # Displaying info about Mushrooms DataFrame
   print('\nDataFrame "mushrooms" info:')
   print('\tshape  : ', df_mushrooms.shape)
   print('\tcolumns: ', df_mushrooms.columns)

   # Keeping only genus from Mushrooms DataFrame to build genus DataFrame
   df_genus = df_mushrooms[ df_mushrooms['taxon_rank'] == 'genus' ]

   # Filtering on images
   # Only image of type 'jpg' and with format 640 were scapped from mushroomObserver website
   df_genus = df_genus[ df_genus['image_type'] == 'jpg' ]
   df_genus = df_genus[ df_genus['image_format'] == '640' ]

   # Keeping only non-deprecated entries
   df_genus = df_genus[ df_genus['deprecated'] != True ]

   # Keeping only non-misspelled entries
   df_genus = df_genus[ df_genus['misspelled'] != True ]

   # Removing all entries which does not have an image_url
   df_genus.dropna(
         axis    = 'index'
      ,  how     = 'any'
      ,  thresh  = None
      ,  subset  = ['image_url']
      ,  inplace = True
   )

   # Adjusting data types
   df_genus = df_genus.astype(
        dtype = {
             'image_id'   : 'int64'
           , 'image_views': 'int64'
        }
      , copy = True
      , errors = 'raise'
   )

   # Displaying info about Mushrooms DataFrame
   print('\nDataFrame "genus" info:')
   print('\tshape  : ', df_genus.shape)
   print('\tcolumns: ', df_genus.columns)

   return df_genus





def clean_genus(df_genus):

   errCnt = 0

   print('DataFrame info:')
   print('\tshape  : ', df_genus.shape)
   print('\tcolumns: ', df_genus.columns)

   # Searching for Null values
   print('\n[*] Identifying columns with null values:\n')
   cols_with_null = df_genus.isna().sum()
   print(cols_with_null[ cols_with_null > 0 ])
   del cols_with_null

   # Removing unneeded columns
   print('\n[*] Removing unneeded columns ...')
   print('(reason: contains null values)')
   unneeded_cols = [
        'primary_image_date'
      , 'primary_image_license'
      , 'primary_image_quality'
      , 'image_quality'
      , 'image_width'
      , 'image_height'
   ]
   print('\nColumns to be removed:')
   print(unneeded_cols)
   df_genus.drop(columns = unneeded_cols, inplace = True)

   # Checking that consensus_* columns correspond to taxon_* columns
   res = df_genus[
      (df_genus['consensus_id']     != df_genus['taxon_id']) \
      | (df_genus['consensus_rank'] != df_genus['taxon_rank'])
      | (df_genus['consensus_name'] != df_genus['taxon_name'])
   ]
   if (res.shape[0] == 0):
      print('\n[*] Removing unneeded columns ...')
      print('(reason: duplicated values)')
      unneeded_cols = [
           'consensus_id'
         , 'consensus_rank'
         , 'consensus_name'
         , 'consensus_synonym_id'
      ]
      print('\nColumns to be removed:')
      print(unneeded_cols)
      df_genus.drop(columns = unneeded_cols, inplace = True)
   else:
      print('\nERROR: "consensus_*" columns do not correspond to "taxon_*" columns !')
      errCnt += 1

   # Removing unneeded columns
   print('\n[*] Removing unneeded columns ...')
   print('(reason: columns not needed)')
   unneeded_cols = [
        'primary_image_id'
      , 'image_content_type'
      , 'deprecated'
      , 'misspelled'
   ]
   print('\nColumns to be removed:')
   print(unneeded_cols)
   df_genus.drop(columns = unneeded_cols, inplace = True)

   #
   # Identification du genus
   #

   # Distinct names and ids for all genus
   genusNameCnt = df_genus['taxon_name'].nunique()
   genusIdCnt   = df_genus['taxon_id'].nunique()
   print('genus [#names]: ', genusNameCnt)
   print('genus [#id]   : ', genusIdCnt)

   # Distinct ids per genus name
   print('\n[*] Searching for genus names associated with multiple Ids ...')
   ids_per_genusName = df_genus.groupby(by=['taxon_name']).agg('nunique')['taxon_id']
   ids_per_genusName = ids_per_genusName[ ids_per_genusName > 1 ]
   print('Genus names associated with multiple ids:')
   print(ids_per_genusName)

   # Distinct names per genus id
   print('\n[*] Searching for genus ids associated with multiple Names ...')
   names_per_genusId = df_genus.groupby(by=['taxon_id']).agg('nunique')['taxon_name']
   names_per_genusId = names_per_genusId[ names_per_genusId > 1 ]
   print('Genus ids associated with multiple names:')
   print(names_per_genusId)
   #
   # no result: names_per_genusId is not needed any more
   del names_per_genusId

   for name in ids_per_genusName.index:
      print('name: ', name)
      ids = df_genus[ df_genus['taxon_name'] == name ]['taxon_id'].unique()
      if (len(ids) > 1):
         df_genus.loc[:,'taxon_id'] = df_genus.loc[:,'taxon_id'].replace(to_replace = ids[1:], value = ids[0], inplace = False)

   # Distinct names and ids for all genus (verification)
   genusNameCnt = df_genus['taxon_name'].nunique()
   genusIdCnt   = df_genus['taxon_id'].nunique()
   print('\ngenus [#names]: ', genusNameCnt)
   print('genus [#id]   : ', genusIdCnt)

   # Filtering microscopic mushrooms
   print('\n[*] Filtering microscopic mushrooms ...')
   df_cpy = df_genus.copy()
   for key in ['stereomicrscopic', 'micro', 'spore', 'scale']:
      notes = df_cpy['image_notes'].str.lower()
      df_cpy = df_cpy[ ~ notes.str.contains(key, na = False) ].copy()
   df_genus = df_cpy.copy()
   del df_cpy

   return errCnt