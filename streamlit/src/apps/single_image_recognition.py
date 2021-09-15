# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries

import streamlit as st

# Import User libraries

from apps.base_app import CBaseApp
from components.image_selector    import CImageSelector
from components.imageRecognition import CImageRecognition
from session_state.image_state import CImageClassificationState


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CApp(CBaseApp):

   #def _loadMushroomDetectionModel(self):


   def render(self):

      # component: ImageSelector
      compOpts = dict(
            localFileUploader_label               = 'Upload a local image:'
         ,  localFileUploader_allowedTypes        = ['png', 'jpg', 'jpeg']
         ,  localFileUploader_acceptMultipleFiles = False
         ,  localFileUploader_help                = 'Upload here an image containing a mushroom.'
         ,  remoteFileUploader_label              = 'URL:'
         ,  remoteFileUploader_maxChars           = 2048
         ,  remoteFileUploader_help               = 'Enter an URL pointing to an image containing a mushroom.'
      )
      imageSelector = CImageSelector(compOpts = compOpts)
      imageSelector.render()

      # Displaying the image
      #
      # Image state instanciation
      imageState = CImageState()
      imageState.setFromRegistry()
      image = imageState.getData()
      if image:
         st.write('Displaying the uploaded image:')
         st.image(image, caption = 'uploaded image')


      # component: imageRecognition
      compOpts = dict(
         title = 'Image Recognition'
      )
      imageRecognition = CImageRecognition(compOpts = compOpts)
      imageRecognition.render()

   '''
   def render(self):

      # component: ModelSelector
      compOpts = dict(
      )
      modelSelector = CModelSelector(compOpts = compOpts)
      modelSelector.render()





      # component: DataAugmentation
      compOpts = dict(
         title = 'Data Augmentation'
      )
      dataAugment = CDataAugmentation(compOpts = compOpts)
      dataAugment.render()


      # component: imageClassifier
      compOpts = dict(
         title = 'Image Classifier'
      )
      imageClassifier = CImageClassifier(compOpts = compOpts)
      imageClassifier.render()
   '''






