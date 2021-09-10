# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
from enum import Enum, auto
import streamlit as st





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSKeys(Enum):
   CLASSIFIERS       = 'CLASSIFIERS'
   PROFILE_IDX       = 'PROFILE_IDX'
   MODEL_IDX         = 'MODEL_IDX'
   MODEL_STATE       = 'MODEL_STATE'
   IMAGE_SELECT_MODE = 'IMAGE_SELECT_MODE'
   IMAGE_STATE       = 'IMAGE_STATE'
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

