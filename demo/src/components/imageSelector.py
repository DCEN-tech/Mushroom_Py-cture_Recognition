# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import sys
import streamlit as st
import streamlit.components.v1 as stc


# Import User Libraries
from components.base_component import CBaseComponent
from image.image_utils import loadImage, loadImageFromUrl
from session_state.session_state_utils import CSessionState as ss, CSSKeys as ssKeys
from session_state.image_state         import CImageState


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COMP_DFLT_OPTS = dict(
      title = 'Image Selector'
)

# Mode
MODE_LOCAL=0
MODE_REMOTE=1



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def modeLabel(mode):
   if mode == MODE_LOCAL:
      return 'Local'
   return 'Remote'





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CImageSelector(CBaseComponent):

   # Constructor
   def __init__(self
      ,  compOpts
   ):
      super().__init__(compOpts)
      self.dfltOpts = COMP_DFLT_OPTS
      self.compOpts = compOpts


   @st.cache
   def loadImage(self, imageFile):
      return loadImage(imageFile)


   @st.cache
   def loadImageFromUrl(self, url):
      return loadImageFromUrl(url)




   def render(self):

      with st.container():

         #
         # Component Title
         #
         # Display the component title
         self.showTitle(self.getOpt('title'))

         #
         # Radio: Local vs Remote
         #
         radio_selectMode = st.radio(
               label       = 'Mode'
            ,  key         = ssKeys.IMAGE_SELECT_MODE.value
            ,  options     = [MODE_LOCAL, MODE_REMOTE]
            ,  index       = 0
            ,  format_func = modeLabel
         )

         # Radio "Mode" has changed
         #
         # mode: LOCAL
         if radio_selectMode == MODE_LOCAL:
            # Displaying the Local Image Uploader
            localFileUploader = st.file_uploader(
                  label                 = self.compOpts.get('localFileUploader_label')
               ,  type                  = self.compOpts.get('localFileUploader_allowedTypes')
               ,  accept_multiple_files = self.compOpts.get('localFileUploader_acceptMultipleFiles')
               ,  help                  = self.compOpts.get('localFileUploader_help')
            )

            # Placeholder for Load status
            console = st.empty()

            # Image state instanciation
            imageState = CImageState()

            # A local image has been selected
            if localFileUploader:
               try:
                  # Loading the image
                  console.info('Loading the image...')
                  image = self.loadImage(localFileUploader)
                  if image is None:
                     raise ValueError('<None Type> is not a valid image.')
                  # From here the image loading is OK
                  # Updating the image state
                  imageState.set(
                        loadSuccess = True
                     ,  imgData     = image
                     ,  exception   = None
                  )
                  # Registering the image state
                  imageState.register()

               except:
                  e = sys.exc_info()[0]
                  imageState.set(
                        loadSuccess = False
                     ,  imgData     = None
                     ,  exception   = e
                     )
                  # Registering the image state
                  imageState.register()

         # REMOTE Selection Mode
         elif radio_selectMode == MODE_REMOTE:
            # Displaying the Remote Image Uploader
            remoteImageUploader = st.text_input(
                  label     = self.compOpts.get('remoteFileUploader_label')
               ,  max_chars = self.compOpts.get('remoteFileUploader_maxChars')
               ,  type      = 'default'
               ,  help      = self.compOpts.get('remoteFileUploader_help')
            )

            # Placeholder for Load status
            console = st.empty()

            # Image state instanciation
            imageState = CImageState()


            # A remote image has been selected

            if remoteImageUploader:
               try:
                  # Loading the image
                  console.info('Loading the image...')
                  image = self.loadImageFromUrl(remoteImageUploader)
                  if image is None:
                     raise ValueError('<None Type> is not a valid image.')
                  # From here the image loading is OK
                  # Updating the image state
                  imageState.set(
                        loadSuccess = True
                     ,  imgData     = image
                     ,  exception   = None
                  )
                  # Registering the image state
                  imageState.register()

               except:
                  e = sys.exc_info()[0]
                  imageState.set(
                        loadSuccess = False
                     ,  imgData     = None
                     ,  exception   = e
                     )
                  # Registering the image state
                  imageState.register()

         # Invalid Selection Mode
         else:
            st.exception('Invalid selection mode !')


         # Displaying the "load image" status
         #
         # Retrieving the image state
         imageState.setFromRegistry()
         if imageState.get() == None:
            console.info('No image loaded yet')
         else:
            loadSuccess = imageState.getLoadSuccess()
            if loadSuccess is None:
               console.info('No image loaded yet')
            elif loadSuccess == True:
               console.success('Image loading: [ OK ]')
            else:
               console.error('Image loading: [ FAILED ]')
               e = imageState.getException()
               if e:
                  st.exception(e)



   def getOptDflt(self, optName):
      if optName in self.dfltOpts.keys():
         return self.dfltOpts.get(optName)
      raise ValueError(f'Invalid option name: "{optName}". This option does not exist for this component.')


