# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries

import streamlit as st

# Import User libraries

from apps.base_app import CBaseApp
from components.modelSelector    import CModelSelector
from components.imageSelector    import CImageSelector
from components.dataAugmentation import CDataAugmentation
from components.imageClassifier  import CImageClassifier
from session_state.image_state   import CImageState



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CApp(CBaseApp):

   def render(self):

      # component: ModelSelector
      compOpts = dict(
      )
      modelSelector = CModelSelector(compOpts = compOpts)
      modelSelector.render()


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







