# -*- coding: utf-8 -*-

import pandas as pd

# Scikit-learn
from sklearn.model_selection import train_test_split

# Matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Seaborn
import seaborn as sns



def top_n_famous_genus_names(df_genus, n):
   genusNames = \
   df_genus.groupby('taxon_name').agg('nunique')['image_id'] \
      .sort_values(ascending = False, inplace = False, ignore_index = False) \
      .index \
      .to_list()

   if (len(genusNames) > n):
      genusNames = genusNames[:n]

   return genusNames



def genus_filter_by_name(df_genus, keep_names):
   if not isinstance(keep_names, list):
      raise TypeError('Invalid type used for parameter <keep_names> : a list was expected')
   return df_genus[ df_genus['taxon_name'].isin(keep_names) ]



def limit_images_per_genus(df_genus, max_imagesPerGenus):

   print('*** Limiting images per Genus ...')
   print(f'max images per genus: {max_imagesPerGenus}')

   min_ImagesPerGenus = df_genus[['taxon_name', 'image_id']].groupby(by=['taxon_name']).agg('count')['image_id'].min()
   print(f'min images per genus (detected): {min_ImagesPerGenus}')

   target_imagesPerGenus = min(min_ImagesPerGenus, max_imagesPerGenus)

   # Altering the dataframe
   for genusName in df_genus['taxon_name'].unique().tolist():
      index = df_genus[ df_genus['taxon_name'] == genusName ].iloc[target_imagesPerGenus:].index
      df_genus.drop(labels = index, axis = 0, inplace = True)

   print('\nDataframe shape: ', df_genus.shape)



def split_df_genus(df_genus, test_ratio, valid_ratio, seed1 = None, seed2 = None):
   # return: X_train, X_valid, X_test

   # Building TEST dataset
   df_remain, X_test = train_test_split(
         df_genus
      ,  test_size    = test_ratio
      ,  shuffle      = True
      ,  random_state = seed1
      ,  stratify     = df_genus['taxon_name']
   )

   # Building TRAIN and VALIDATION datasets
   X_train, X_valid = train_test_split(
         df_remain
      ,  test_size    = valid_ratio
      ,  shuffle      = True
      ,  random_state = seed2
      ,  stratify     = df_remain['taxon_name']
   )

   return X_train, X_valid, X_test



def displayImagesPerGenus(df_genus):

   # Using 'taxon_name' column
   imagesPerGenus = df_genus['taxon_name'].value_counts()

   print('')
   print('Graphically:')

   sns.barplot(
        x = imagesPerGenus
      , y = imagesPerGenus.index
      , orient = 'h'
   )
   plt.xlabel('Genre')
   plt.ylabel('Nombre d''images')
   plt.title('Graphe du nombre d''images par genre')
   plt.show()

   print('')
   print('Numerically:')

   # Displaying image repartition by class
   print(df_genus['taxon_name'].value_counts())

   print('')
   print('min[imagePerGenus]: ', imagesPerGenus.min())
   print('max[imagePerGenus]: ', imagesPerGenus.max())
   print('')