# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
from enum import Enum, auto, unique
import streamlit as st





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@unique
class CSSKeys(Enum):
   MODELS_STATE                  = 'MODELS_STATE'
   IMAGE_SELECT_MODE             = 'IMAGE_SELECT_MODE'
   FORCE_RECOGNITION             = 'FORCE_RECOGNITION'
   MUSHROOM_DETECTION_STATE      = 'MUSHROOM_DETECTION_STATE'
   MUSHROOM_CLASSIFICATION_STATE = 'MUSHROOM_CLASSIFICATION_STATE'
   IMAGE_CLASSIFICATION_STATE    = 'IMAGE_CLASSIFICATION_STATE'
   # Component: Model Interpretability
   IMAGE_INTERPRETABILITY_STATE  = 'IMAGE_INTERPRETABILITY_STATE'
   MODEL_INTERPRET_LCL_UPLDR_IMG = 'MODEL_INTERPRET_LCL_UPLDR_IMG'
   INTERPRET_CHOICE_MODEL_IDX    = 'INTERPRET_CHOICE_MODEL_IDX'
   #
   CLASSIFIERS       = 'CLASSIFIERS'
   PROFILE_IDX       = 'PROFILE_IDX'
   MODEL_STATE       = 'MODEL_STATE'
   KEEP_LOADED_IMAGE = 'KEEP_LOADED_IMAGE'




class CSessionState():

   @staticmethod
   def remove(key):
      st.session_state.pop(key, None)

   @staticmethod
   def set(key, value):
      st.session_state[key] = value

   @staticmethod
   def get(key):
      return st.session_state.get(key)

