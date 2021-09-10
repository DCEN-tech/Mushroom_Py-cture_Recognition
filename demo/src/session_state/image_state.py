# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import streamlit as st

# Import User Libraries
from session_state.base_state          import CBaseState
from session_state.session_state_utils import CSSKeys as ssKeys


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CImageState(CBaseState):

   def __init__(self):
      super().__init__(key = ssKeys.IMAGE_STATE.value, state = None)


   def set(self
      ,  loadSuccess
      ,  imgData
      ,  exception = None
   ):
      state = {
            'loadSuccess': loadSuccess
         ,  'imgData'    : imgData
         ,  'exception'  : exception
      }
      super().set(state)


   def getLoadSuccess(self):
      state = self.get()
      if state:
         return state.get('loadSuccess')
      else:
         return None


   def getData(self):
      state = self.get()
      if state:
         return state.get('imgData')
      else:
         return None


   def getException(self):
      state = self.get()
      if state:
         return state.get('exception')
      else:
         return None

