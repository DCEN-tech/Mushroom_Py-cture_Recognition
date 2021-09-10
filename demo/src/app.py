# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import streamlit as st
import streamlit.components.v1 as stc

# Import User libraries
from apps.home                         import CApp as appHome
from apps.singleImageRecognition       import CApp as appSingleImageRecognition
from apps.multipleImagesPredictions    import CApp as appMultipleImagesPrediction
from apps.modelInterpretability        import CApp as appModelInterpretability
from apps.about                        import CApp as appAbout


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Sub-Application Labels
APP_HOME                        = 'home'
APP_SINGLE_IMAGE_RECOGNITION    = 'single_image_recognition'
APP_MULTIPLE_IMAGES_RECOGNITION = 'multiple_images_recognition'
APP_MODEL_INTERPRETABILITY      = 'model_intepretability'
APP_ABOUT                       = 'about'

DFLT_PAGE_CONFIG = dict(
      page_title            = '[MPR] - Demo App'
   ,  page_icon             = '🍄'
   ,  layout                = 'wide'
   ,  initial_sidebar_state = 'expanded'
)

TITLE_MODE_TEXT=0
TITLE_MODE_IMAGE=1
APP_TITLE = 'MUSHROOM PY-CTURE RECOGNITION'
APP_TITLE_HTML = f'''
   <div style="background-color:#3872fb; padding:5px; border-radius:10px">
		<h1 style="color:white;text-align:center;">{APP_TITLE}</h1>
	</div>
'''
APP_TITLE_IMAGE='../resources/images/Mushroom py-cture_recognition_.png'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setPageConfig(pageConfig):

   # -------------------------------------------
   # Streamlit Initialization
   #
   # CAUTION:
   #     Must be the first activity of streamlit
   # -------------------------------------------

   '''
   def getOption(optName):
      return initOpts.get(optName) or DFLT_INIT_OPTS.get(optName)
   '''

   if pageConfig:
      config = pageConfig.copy()
   else:
      config = dict()

   config.update(DFLT_PAGE_CONFIG)

   # Apply the configuration
   st.set_page_config(**config)



def showTitle(mode):
   if mode == TITLE_MODE_IMAGE:
      st.image(APP_TITLE_IMAGE)
   else:
      stc.html(APP_TITLE_HTML)



def main(pageConfig = None):

   # Intialization
   setPageConfig(pageConfig)

   # Displaying the application title
   showTitle(TITLE_MODE_IMAGE)

   apps = [
         APP_HOME
      ,  APP_SINGLE_IMAGE_RECOGNITION
      ,  APP_MULTIPLE_IMAGES_RECOGNITION
      ,  APP_MODEL_INTERPRETABILITY
      ,  APP_ABOUT
   ]

   choice = st.sidebar.selectbox('Menu', apps)

   if choice == APP_HOME:
      app = appHome(title = '[ Home ]')
   elif choice == APP_SINGLE_IMAGE_RECOGNITION:
      app = appSingleImageRecognition(title = '[ Single Image Recognition ]')
   elif choice == APP_MULTIPLE_IMAGES_RECOGNITION:
      app = appMultipleImagesPrediction(title = '[ Multiple Images Recognition ]')
   elif choice == APP_MODEL_INTERPRETABILITY:
      app = appModelInterpretability(title = '[ Model interpretability ]')
   elif choice == APP_ABOUT:
      app = appAbout(title = '[ About ]')
   else:
      ValueError(f'Invalid choice: "{choice}". There is no application corresponding to this choice !')

   # Launch the application
   app.run()


if __name__ == '__main__':
   main()

