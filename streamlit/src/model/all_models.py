# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import numpy as np
import os
import PIL
from enum import Enum, unique
import tensorflow as tf

# Import User libraries
from model.model import Classifier, EnsembleClassifier, DFLT_MODEL_PATH



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@unique
class MushroomDetectorClasses(Enum):
   PRESENT     = 0
   NOT_PRESENT = 1


@unique
class MushroomClasses(Enum):
   AGARICUS    = 'Agaricus'
   AMANITA     = 'Amanita'
   ARMILLARIA  = 'Armillaria'
   CORTINARIUS = 'Cortinarius'
   ENTOLOMA    = 'Entoloma'
   GYMNOPUS    = 'Gymnopus'
   HYGROCYBE   = 'Hygrocybe'
   LACTARIUS   = 'Lactarius'
   MARASMIUS   = 'Marasmius'
   RUSSULA     = 'Russula'


MUSHROOM_10_CLASSES = [
      MushroomClasses.AGARICUS
   ,  MushroomClasses.AMANITA
   ,  MushroomClasses.ARMILLARIA
   ,  MushroomClasses.CORTINARIUS
   ,  MushroomClasses.ENTOLOMA
   ,  MushroomClasses.GYMNOPUS
   ,  MushroomClasses.HYGROCYBE
   ,  MushroomClasses.LACTARIUS
   ,  MushroomClasses.MARASMIUS
   ,  MushroomClasses.RUSSULA
]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Model: Mushroom Detector
mushroomDetector = Classifier(
      classes      = [ MushroomDetectorClasses.PRESENT, MushroomDetectorClasses.NOT_PRESENT ]
   ,  modelName    = 'Mushroom Detector'
   ,  filepath     = os.path.join(DFLT_MODEL_PATH, 'is_mushroom_enetb0.h5')
)

# EfficientNetB0
efficientNetB0 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'EfficientNetB0'
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb0.h5')
)

# EfficientNetB1
efficientNetB1 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'EfficientNetB1'
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb1.h5')
)

# EfficientNetB2
efficientNetB2 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'EfficientNetB2'
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb2.h5')
)

# EfficientNetB3
efficientNetB3 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'EfficientNetB3'
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb3.h5')
)

# EfficientNetB4
efficientNetB4 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'EfficientNetB4'
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb4.h5')
)

# EfficientNetB5
efficientNetB5 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'EfficientNetB5'
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb5.h5')
)

# EfficientNetB6
efficientNetB6 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb6.h5')
   ,  modelName = 'EfficientNetB6'
)

# EfficientNetB7
efficientNetB7 = Classifier(
      classes   = MUSHROOM_10_CLASSES
   ,  filepath  = os.path.join(DFLT_MODEL_PATH, 'efficientnetb7.h5')
   ,  modelName = 'EfficientNetB7'
)

# VGG16
vgg16 = Classifier(
      classes      = MUSHROOM_10_CLASSES
   ,  filepath     = os.path.join(DFLT_MODEL_PATH, 'vgg16.h5')
   ,  modelName    = 'VGG16'
   ,  preprocessFn = tf.keras.applications.vgg16.preprocess_input
)

# VGG19
vgg19 = Classifier(
      classes      = MUSHROOM_10_CLASSES
   ,  modelName    = 'VGG19'
   ,  filepath     = os.path.join(DFLT_MODEL_PATH, 'vgg19.h5')
   ,  preprocessFn = tf.keras.applications.vgg19.preprocess_input
)

# EnsembleClassifier
ensembleClassifier = EnsembleClassifier(
      classes   = MUSHROOM_10_CLASSES
   ,  modelName = 'Mushroom Classifier'
   ,  filepath = os.path.join(DFLT_MODEL_PATH, 'ensemble_model.sav')
   ,  members = [
            efficientNetB0
         ,  efficientNetB1
         ,  efficientNetB2
         ,  efficientNetB3
         ,  efficientNetB4
         ,  efficientNetB5
         ,  efficientNetB6
         ,  efficientNetB7
         ,  vgg16
         ,  vgg19
      ]
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#
# Data Preprocessing functions for models
#

# Image resize + adding a dimension for batchs
def getClassicImagePreprocessing(
      target_size
   ,  interpolation = 'bilinear'
):
   def imagePreprocessing(image):
      # Converting the image type if necessary: objective to get an image of type numpy.ndarray
      if isinstance(image, PIL.JpegImagePlugin.JpegImageFile):
         # Converting <image> to a numpy ndarray
         image = tf.keras.preprocessing.image.img_to_array(image)
      elif isinstance(image, np.ndarray):
         # Nothing more to do here: the image already has the valid type
         pass
      else:
         raise TypeError('Invalid type for argument <image>: actual type: {type(image)}')
      # Resizing the image
      image = tf.keras.preprocessing.image.smart_resize(
            x             = image
         ,  size          = target_size
         ,  interpolation = interpolation
      )
      # Adding a dimension to transform our array into a "batch" of size (1, X, X, 3)
      image = np.expand_dims(image, axis = 0)
      return image

   return imagePreprocessing


