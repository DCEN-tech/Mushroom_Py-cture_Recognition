# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Import User Libraries
from components.base_component                     import CBaseComponent
from session_state.session_state_utils             import CSSKeys as ssKeys
from session_state.mushroom_detection_state        import CMushroomDetectionState
from session_state.mushroom_classification_state   import CMushroomClassificationState
from image.image_utils                             import prepareImageData
from model.model                                   import EnsembleClassifier
from model.all_models                              import MushroomDetectorClasses




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CImageRecognition(CBaseComponent):

   def __init__(self
      ,  compOpts
      ,  image
      ,  mushroomDetector   = None
      ,  mushroomClassifier = None
   ):
      super().__init__(compOpts)
      self.image = image
      self.mushroomDetector   = mushroomDetector
      self.mushroomClassifier = mushroomClassifier



   def isMushroomDetected(self
      ,  model
      ,  image
      ,  console
      ,  threshold = 0.65
   ):

      def isDetected(pred):
         print(f'model[ Mushroom detector ] predictions: {pred}')
         idxMax = np.argmax(pred)
         resDetection = model.getClass(idxMax)
         if resDetection.value == MushroomDetectorClasses.PRESENT.value:
            return float(pred[idxMax]) >= threshold
         elif resDetection.value == MushroomDetectorClasses.NOT_PRESENT.value:
            return False
         else:
            raise ValueError('Failed to find the corresponding class to the model prediction. Please contact the administrator.')

      # Get the model name
      modelName = model.getName()

      # Get the model ready (loading it if necessary)
      console.info(f'Load the model {modelName}...')
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

      # Launch the prediction
      pred = model.predict(
            x       = data
         ,  verbose = 1
      )

      return isDetected(pred[0])



   def _classify(self
      ,  classifierModel
      ,  image
      ,  console
      ,  progressBar
   ):

      def doPrediction():
         '''
         print(f'model[ Mushroom detector ] predictions: {pred}')
         idxMax = np.argmax(pred)
         resDetection = model.getClass(idxMax)
         if resDetection.value == MushroomDetectorClasses.PRESENT.value:
            return pred[idxMax] >= threshold
         elif resDetection.value is MushroomDetectorClasses.NOT_PRESENT:
            return False
         else:
            raise ValueError('Failed to find the corresponding class to the model prediction. Please contact the administrator.')
         '''
         pass

      if not isinstance(classifierModel, EnsembleClassifier):
         raise NotImplementedError('Classification is only supported for the moment if the model has been inherited from class <EnsembleClassifier>. Using other kind of classifier is not yet implemented !')

      ensembleModel = classifierModel

      membersProbas = list()
      membersNames  = list()
      membersCnt    = len(ensembleModel.getMembers())
      classNames    = ensembleModel.getClasses()

      for cnt, model in enumerate(ensembleModel.getMembers()):

         # Get the model name
         modelName = model.getName()

         # Get the model ready (loading it if necessary)
         console.info(f'Load the model {modelName}...')
         model.load()

         progressBar.progress((cnt + 1/3) / membersCnt)

         # Get the model input shape
         modelInputShape = model.getModelInputShape()

         # Prepare the data for the model
         console.info(f'Image preprocessing (for model: {modelName})...')
         data = prepareImageData(
               image         = image
            ,  target_size   = modelInputShape[1:3]
            ,  interpolation = 'bilinear'
         )

         progressBar.progress((cnt + 2/3) / membersCnt)

         # Launch the prediction
         console.info(f'Compute classification (for model: {modelName})...')
         proba = model.predict(
               x       = data
            ,  verbose = 1
         )

         membersNames.append(modelName)
         membersProbas.append(proba[0])

         progressBar.progress((cnt + 1) / membersCnt)

      progressBar.progress(1.0)

      # modelState.register()

      df_membersProbas = pd.DataFrame(
            data    = membersProbas
         ,  index   = membersNames
         ,  columns = [ name.value for name in classNames ]
      )

      stackX = np.expand_dims(df_membersProbas, axis = 0)
      stackX = np.reshape(stackX, newshape = (stackX.shape[0], stackX.shape[1] * stackX.shape[2]))

      # Get the model ready (loading it if necessary)
      ensembleModel.load()
      #modelState.register()

      # Compute the predictions for the Ensemble model
      model       = ensembleModel.getInstance()
      modelProbas = model.predict_proba(stackX)

      # Set the classifier results in a DataFrame
      df_modelProbas = pd.DataFrame(
            data    = modelProbas.T
         ,  index   = [ name.value for name in classNames ]
         ,  columns = [ 'Probas' ]
      )

      # Format the DataFrame
      df_modelProbas.index.name = 'Class'
      df_results = df_modelProbas \
         .reset_index(drop = False, inplace = False) \
         .sort_values(
               by           = ['Probas']
            ,  ascending    = False
            ,  inplace      = False
            ,  ignore_index = False
         )

      # Displaying the prediction results
      #
      # GUI component properties
      topColor = '#f63366'
      # Genus
      resultHTML = f'The model thinks the genus of the mushroom on the image is: <span style="border-radius: 0.4rem; color: white; padding: 0.3rem; margin-bottom: 2rem; padding-left: 1rem; font-weight: 700; background-color: {topColor};">{df_results.iloc[0]["Class"]}</span>'
      st.markdown(resultHTML, unsafe_allow_html = True)

      st.write('Predictions were done by an Ensemble Model.')
      st.write('Find below more details on the computed predictions:')

      #
      # Ensemble Model results
      #
      st.markdown('**Ensemble Model results** :')
      st.markdown('* Probabilities:')
      st.dataframe(df_results)

      st.markdown('* Graphic:')
      # Graphic (altair)
      chart = alt.Chart(df_results) \
         .mark_bar() \
         .encode(
               x       = alt.X('Probas:Q')
            ,  y       = alt.Y('Class', title = 'Genus', sort = '-x')
            ,  opacity = alt.value(1)
            ,  color   = alt.condition(
                     alt.datum.Class == df_results.iloc[0]['Class']  # If it's the top ranked prediction
                  ,  alt.value('#f63366')                      # sets the color for the top ranked prediction
                  ,  alt.value('#1F74B4')                      # sets the color for all other non top ranked prediction
               )
         ) \
         .properties(
               width  = 650
            ,  height = 260
         )
      text = chart.mark_text(
            align    = 'left'
         ,  baseline = 'middle'
         ,  dx = 3                # Nudges text to right so it doesn't appear on top of the bar
      ) \
         .encode(
            text = alt.Text('Probas', format = '.2r')
         )
      graph = (chart + text).configure_axis(
            labelFontSize = 13
         ,  titleFontSize = 16
      )
      # Displaying the graphic
      st.altair_chart(graph)

      #
      # Members models results
      #
      st.markdown('**Members models (of the Ensemble Model) results** :')
      st.markdown('* Probabilities:')
      st.dataframe(df_membersProbas)

      st.markdown('* Classification:')
      classification = df_membersProbas.apply(
            func = np.argmax
         ,  axis = 1
      ) \
         .value_counts()
      classification.index.name = 'Class'
      classification = classification.rename(lambda x: classNames[x].value)
      classification.name = 'Count'
      st.write(classification)









   def doMushroomClassification(self
      ,  console
   ):
      try:
         # mushroom classification state instanciation
         mushroomClassificationState = CMushroomClassificationState()
         console.info('Mushroom classification in progress... this may take a while... please wait !')

         progressBar = st.progress(0)

         # Ensure that an image is available
         if self.image is None:
            raise RuntimeError('No image available ! Please load an image and try again.')

         # Ensure that a model for the mushroom detection is available
         if self.mushroomClassifier is None:
            raise RuntimeError('No model available for the mushroom detection ! Please contact the administrator.')

         # Classify the mushroom present in the image
         self._classify(
               classifierModel = self.mushroomClassifier
            ,  image           = self.image
            ,  console         = console
            ,  progressBar     = progressBar
         )


      except Exception as e:
         console.exception(e)
         # Updating the mushroom detection state
         mushroomClassificationState.setData(data = None)








   def recognition(self, console):
      pass

      '''
         # Retrieving the model list

         # Retrieving the model: "Mushroom Detection"
         model_mushDetector = modelListState.get(ModelId.MUSHROOM_DETECTION)

         print(model_mushDetector)
      '''



      '''
         # Retrieving the model
         modelState = CModelState()
         modelState.setFromRegistry()
         if modelState.getLoadSuccess() != True:
            raise RuntimeError('No model available ! Please load a model and try again.')
         modelInstance = modelState.getModelInstance()
         if modelInstance is None:
            raise RuntimeError('<None Type> is not a valid model ! Please load a model and try again.')
         classNames = modelState.getClassNames()

         # Retrieving the expected input shape for the model
         modelInputShape  = modelInstance.input_shape
         imageTargetShape = modelInputShape[1:]



         # Data Preprocessing
         imgData = self.dataPreprocessing(
               image            = imgData
            ,  imageTargetShape = imageTargetShape
         )
         console.info('prediction in progress...')
         rawPreds, durationSec = self.predict(modelInstance, imgData, console)
         console.info(f'prediction done (in {round(durationSec * 1000, 2)} ms)')

         # Here we have valid results
         if (rawPreds is not None) and rawPreds.shape[0] > 0:
            preds = pd.DataFrame(
                  data = {
                     'Probas': rawPreds[0]
                  }
               ,  index = classNames
            )
            preds.index.name = 'Class'
            result = preds


      except Exception as e:
         console.exception(e)
         result = None

      finally:
         return result
      '''

   def doMushroomDetection(self
      ,  console
   ):
      try:
         # mushroom detection state instanciation
         mushroomDetectionState = CMushroomDetectionState()

         console.info('Mushroom detection in progress...')

         # Ensure that an image is available
         if self.image is None:
            raise RuntimeError('No image available ! Please load an image and try again.')
         # Ensure that a model for the mushroom detection is available
         if self.mushroomDetector is None:
            raise RuntimeError('No model available for the mushroom detection ! Please contact the administrator.')

         # Detecting if a Mushroom is present in the image
         detected = self.isMushroomDetected(
               model          = self.mushroomDetector
            ,  image          = self.image
            ,  console        = console
         )

         # Updating the mushroom detection state
         mushroomDetectionState.setData(data = detected)

      except Exception as e:
         console.exception(e)
         # Updating the mushroom detection state
         mushroomDetectionState.setData(data = None)

      finally:
         # Registering the Mushroom detection state
         mushroomDetectionState.register()




   def render(self):

      with st.container():

         #
         # Component Title
         #
         # Display the component title
         self.showTitle(self.getOpt('title'))

         #
         # Button: "Launch recognition"
         #
         btn_LaunchRecognition = st.button(
               label = 'Launch recognition'
            ,  help  = 'Click on this button to launch the recognition on the selected image'
         )

         # Placeholder for Mushroom Detection
         console = st.empty()

         enableClassification = False

         # Button: "Launch recognition" has been clicked
         if btn_LaunchRecognition:

            st.write('[Phase 1]: Mushroom detection on the image')
            self.doMushroomDetection(console = console)

            # Displaying the "mushroom detection" status
            #
            # Retrieving the mushroom detection state
            mushroomDetectionState = CMushroomDetectionState()
            mushroomDetectionState.setFromRegistry()

            detectionState = mushroomDetectionState.getData()

            if detectionState is None:
               enableClassification = False
            elif detectionState == True:
               console.success('Mushroom detected in the image according to the model.')
               enableClassification = True
            else:
               console.error('NO mushroom detected on the image according to the model.')
               # Radio: Force recognition
               radio_forceRecognition = st.radio(
                     label       = 'Do you want to force the mushroom recognition anyway ?'
                  ,  key         = ssKeys.IR__FORCE_RECOGNITION.value
                  ,  options     = [False, True]
                  ,  index       = 0                  # False by default
                  ,  format_func = lambda x: 'Yes' if x else 'No'
               )

               # Radio "Force recognition" has changed
               if radio_forceRecognition == True:
                  # Enable the Mushroom Recognition
                  enableClassification = True
               elif radio_forceRecognition == False:
                  # Nothing more to do here
                  enableClassification = False


            # Launch the Mushroom Recognition (if requested)
            if enableClassification:

               st.write('[Phase 2]: Mushroom genus recognition')

               # Placeholder for Mushroom Detection
               console = st.empty()

               self.doMushroomClassification(console = console)

               '''
                  # Retrieving the image
                  imageState = CImageState()
                  imageState.setFromRegistry()
                  if not imageState.getLoadSuccess():
                     raise RuntimeError('No image available ! Please load an image and try again.')
                  imgData = imageState.getData()
                  if imgData is None:
                     raise ValueError('<None Type> is not a valid image ! Please load an image and try again.')

                  # Retrieving all the available models
                  modelState = CModelState()
                  modelState.setFromRegistry()
                  models = modelState.get()
                  if models is None:
                     # Retrieving available models
                     models = getAvailableModels()
                     # Enregistrement des modèles
                     modelState = CModelState(state = models)
                     modelState.register()




               except Exception as e:
                  # Updating the
                  mushroomClassificationState.set(
                        status    = None
                     ,  exception = e
                  )
                  console.exception(e)

               finally:
                  # Registering the Mushroom detection state
                  mushroomClassificationState.register()
               '''

            # preds = self.recognition(console)


         # ==========================================================================


         '''
         preds = self.recognition(console)

         if preds is not None:

            # Format the DataFrame
            data = preds.copy() \
                     .reset_index(inplace = False) \
                     .sort_values(
                           by           = ['Probas']
                        ,  ascending    = False
                        ,  inplace      = False
                        ,  ignore_index = False
                     )

            # GUI component properties
            topColor = '#f63366'
            if data.shape[0] <= 10:
               height = 400
            else:
               height = 800

            # Displaying the prediction results
            #
            # Genus
            genusName = f'The model thinks the genus of the mushroom on the image is: <span style="border-radius: 0.4rem; color: white; padding: 0.3rem; margin-bottom: 2rem; padding-left: 1rem; font-weight: 700; background-color: {topColor};">{data.iloc[0]["Class"]}</span>'
            st.markdown(genusName, unsafe_allow_html = True)

            st.write('Find below more details on the predictions done by the model:')

            # Graphic (altair)
            st.write('**Graphic:**')
            chart = alt.Chart(data) \
               .mark_bar() \
               .encode(
                     x       = alt.X('Probas:Q')
                  ,  y       = alt.Y('Class', title = 'Genus', sort = '-x')
                  ,  opacity = alt.value(1)
                  ,  color   = alt.condition(
                           alt.datum.Class == data.iloc[0]['Class']  # If it's the top ranked prediction
                        ,  alt.value('#f63366')                      # sets the color for the top ranked prediction
                        ,  alt.value('#1F74B4')                      # sets the color for all other non top ranked prediction
                     )
               ) \
               .properties(
                     width  = 650
                  ,  height = height
               )
            text = chart.mark_text(
                  align    = 'left'
               ,  baseline = 'middle'
               ,  dx = 3                # Nudges text to right so it doesn't appear on top of the bar
            ) \
               .encode(
                  text = alt.Text('Probas', format = '.2r')
               )
            graph = (chart + text).configure_axis(
                  labelFontSize = 13
               ,  titleFontSize = 16
            )
            # Displaying the graphic
            st.altair_chart(graph)

            # Full table of predictions
            st.write('**Full table of predictions:**')
            st.dataframe(
                  data   = data.reset_index(drop = True)
               ,  height = height
            )
         '''


   def getOptDflt(self, optName):
      if optName in self.dfltOpts.keys():
         return self.dfltOpts.get(optName)
      raise ValueError(f'Invalid option name: "{optName}". This option does not exist for this component.')








'''

import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import time as t



from session_state.session_state_utils import CSSKeys as ssKeys, CSessionState as ss
from session_state.model_state         import CModelState
from session_state.image_state         import CImageState


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COMP_DFLT_OPTS = dict(
      title = 'Image Selector'
)



class CImageClassifier(CBaseComponent):

   def __init__(self
      ,  compOpts
   ):
      super().__init__(compOpts)



   def dataPreprocessing(self
      ,  image
      ,  imageTargetShape
   ):

      if image is None:
         return None

      targetHeight, targetWidth, targetChannel = imageTargetShape[:3]

      # Make a copy
      imgData = image.copy()

      # As a numpy array
      imgData = np.asarray(image)

      # Applying data preprocessing
      # using tensor
      X = tf.constant(imgData)
      # add a dimension (for batchs)
      X = tf.expand_dims(X, axis = 0)
      # Resizing
      X = tf.image.resize_with_pad(
            image         = X
         ,  target_height = targetHeight
         ,  target_width  = targetWidth
         ,  method        = 'nearest'
      )

      return X




   def predict(self
      ,  model
      ,  image
      ,  console
   ):
      try:
         res = None
         if model is not None \
            and image is not None:
            # Performs the prediction
            begTime = t.time()
            res = model.predict(
                  x          = image
               ,  batch_size = None
               ,  verbose    = 1
            )
            endTime = t.time()
            durationSec = endTime - begTime
      except Exception as e:
         st.write(e)
         console.exception(e)
         res = None

      finally:
         return (res, durationSec)

'''