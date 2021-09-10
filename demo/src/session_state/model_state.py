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

class CModelState(CBaseState):

   def __init__(self):
      super().__init__(key = ssKeys.MODEL_STATE.value, state = None)


   def set(self
      ,  loadSuccess
      ,  modelInstance
      ,  modelName
      ,  classNames = None
      ,  exception  = None
   ):
      state = {
            'loadSuccess': loadSuccess
         ,  'instance'   : modelInstance
         ,  'name'       : modelName
         ,  'classNames' : classNames
         ,  'exception'  : exception
      }
      super().set(state)


   def getLoadSuccess(self):
      state = self.get()
      if state:
         return state.get('loadSuccess')
      else:
         return None


   def getModelInstance(self):
      state = self.get()
      if state:
         return state.get('instance')
      else:
         return None


   def getClassNames(self):
      state = self.get()
      if state:
         return state.get('classNames')
      else:
         return None


   def getException(self):
      state = self.get()
      if state:
         return state.get('exception')
      else:
         return None
