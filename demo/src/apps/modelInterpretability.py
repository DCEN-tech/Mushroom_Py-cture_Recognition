# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries

import streamlit as st

# Import User libraries

from apps.base_app import CBaseApp
from session_state.image_state import CImageState


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CApp(CBaseApp):

   def render(self):

      # Retrieving the image
      imageState = CImageState()
      imageState.setFromRegistry()
      if not imageState.getLoadSuccess():
         raise RuntimeError('No image available ! Please load an image and try again.')
      imgData = imageState.getData()
      if imgData is None:
         raise ValueError('<None Type> is not a valid image ! Please load an image and try again.')
      '''
      st.radio(
         label = ''
      )
      '''

      '''
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
      '''







