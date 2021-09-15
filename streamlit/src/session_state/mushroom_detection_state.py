# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import User Libraries
from session_state.base_state          import CObjectState
from session_state.session_state_utils import CSSKeys as ssKeys


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CMushroomDetectionState(CObjectState):

   def __init__(self):
      super().__init__(key = ssKeys.MUSHROOM_DETECTION_STATE.value, state = None)


   def set(self
      ,  status    = None
      ,  exception = None
   ):
      state = {
            'status'    : status
         ,  'exception' : exception
      }
      super().set(state)


   def getStatus(self):
      state = self.get()
      if state:
         return state.get('status')
      return None


   def getException(self):
      state = self.get()
      if state:
         return state.get('exception')
      return None

