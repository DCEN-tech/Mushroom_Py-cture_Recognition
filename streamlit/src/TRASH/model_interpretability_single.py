# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import streamlit as st
import matplotlib.pyplot as plt

# Import User libraries
from apps.base_app import CBaseApp
from session_state.session_state_utils import CSSKeys as ss
from session_state.image_state import CImageInterpretabilityState, CImageClassificationState
from components.image_selector import CImageSelector
from components.model_selector import CModelSelector
from image.image_utils import prepareImageData
from model.interpretability import make_gradcam_heatmap


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ANSWER_YES = 'yes'
ANSWER_NO  = 'no'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CApp(CBaseApp):

   def __init__(self
      ,  title           = None
      ,  availableModels = None
   ):
      super().__init__(title)
      self.availableModels = availableModels


   def doModelInterpretability(self
      ,  model
      ,  image
      ,  console
   ):
      try:
         # Ensure that a model is available
         if model is None:
            raise RuntimeError('No model available ! Please select a model try again.')
         # Ensure that an image is available
         if image is None:
            raise RuntimeError('No image available ! Please load an image and try again.')

         # Ensure that the model is loaded
         console.info('Load the model...')
         model.load()

         # Get the model input shape
         modelInputShape = model.getModelInputShape()

         # Prepare the data for the model
         console.info('Image preprocessing...')
         data = prepareImageData(
               image         = image
            ,  target_size   = modelInputShape[1:3]
            ,  interpolation = 'bilinear'
         )

         # Print what the top predicted class is
         #pred = model.predict(data)

         # Compute the gardcam heatmap
         console.info('Compute the gardcam heatmap...')
         heatmap = make_gradcam_heatmap(
               model = model.getInstance()
            ,  image = data
         )

         # Display heatmap
         console.info('Display the heatmap...')
         fig, ax = plt.subplots()
         ax.matshow(heatmap)
         st.pyplot(fig)

         console.empty()


      except Exception as e:
         console.exception(e)



   def main(self):

      # Retrieving the model state
      #modelState = CImageInterpretabilityState()
      #imageState.setFromRegistry()

      # component: ModelSelector
      compOpts = dict(
      )
      modelSelector = CModelSelector(
            compOpts = compOpts
         ,  models   = self.availableModels
      )
      modelSelector.render()


      # Retrieving the image used for the model interpretability
      imageState = CImageInterpretabilityState()
      imageState.setFromRegistry()

      # component: ImageSelector
      compOpts = dict(
            localFileUploader_label               = 'Upload a local image:'
         ,  localFileUploader_allowedTypes        = ['png', 'jpg', 'jpeg']
         ,  localFileUploader_acceptMultipleFiles = False
         ,  localFileUploader_key                 = ss.MODEL_INTERPRET_LCL_UPLDR_IMG.value
         ,  localFileUploader_help                = 'Upload here an image containing a mushroom.'
         ,  remoteFileUploader_label              = 'URL:'
         ,  remoteFileUploader_maxChars           = 2048
         ,  remoteFileUploader_help               = 'Enter an URL pointing to an image containing a mushroom.'
      )
      imageSelector = CImageSelector(compOpts = compOpts, compState = imageState)
      imageSelector.render()

      imageState.setFromRegistry()
      image = imageState.getData()
      if image:
         # Displaying the image
         st.write('Displaying the uploaded image:')
         st.image(image, caption = 'uploaded image')

      #
      # Button: "Launch Interpretability"
      #
      btn_launchInterpretability = st.button(
            label    = 'Launch Interpretability'
         ,  help     = 'Click on this button to launch interpretability on the selected model'
      )

      console = st.empty()

      # Button clicked: "btn_launchInterpretability"
      if btn_launchInterpretability:
         self.doModelInterpretability(
               model   = modelSelector.getSelectedModel()
            ,  image   = image
            ,  console = console
         )












