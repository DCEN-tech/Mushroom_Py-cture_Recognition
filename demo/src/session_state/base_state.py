# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import streamlit as st

# Import User Libraries
from session_state.session_state_utils import CSessionState as ss


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CBaseState:

   def __init__(self
      ,  key
      ,  state = None
   ):
      self.key   = key
      self.state = state


   def set(self, state):
      self.state = state


   def get(self):
      return self.state


   def register(self):
      ss.set(self.key, self.state)


   def unregister(self):
      ss.remove(self.key)


   def setFromRegistry(self):
      CBaseState.set(self, ss.get(self.key))


