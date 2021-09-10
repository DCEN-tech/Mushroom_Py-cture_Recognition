# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries

from abc import ABC, abstractmethod
import streamlit as st



class CBaseApp(ABC):

   def __init__(self
      ,  title = None
   ):
      self.title = title
      pass



   def showTitle(self):
      '''
      DESCRIPTION
            Display the title of the application.
            Skipped if the title has not been defined.
      '''
      if self.title:
         st.title(self.title)



   @abstractmethod
   def render(self):
      pass



   def run(self):
      self.showTitle()
      self.render()