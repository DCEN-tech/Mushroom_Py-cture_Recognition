# -*- coding: utf-8 -*-
########################################################################################################################
#
# HyperTransferLearningModel
#
########################################################################################################################

import tensorflow as tf
import keras_tuner as kt


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DFLT_WEIGHTS_TRANFER_LEARNING_SRC = 'imagenet'
DFLT_POOLING                      = 'avg'
DFLT_ACTIVATION                   = 'relu'
DFLT_WEGHTS_INITIALIZER           = 'RandomNormal'
DFLT_BIASES_INITIALIZER           = 'Zeros'
DFLT_OPTIMIZER_NAME               = 'adam'



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pooling(hp):

   pooling = hp.get('pooling')

   if pooling is None:
      pooling = DFLT_POOLING
      print(f'[WARNING]: pooling is not set in hyperparameters: using default value: "{pooling}"')

   pooling = pooling.lower()
   layer = None
   if pooling == 'flatten':
      layer = tf.keras.layers.Flatten()
   elif pooling == 'avg':
      layer = tf.keras.layers.GlobalAveragePooling2D()
   elif pooling == 'max':
      layer = tf.keras.layers.GlobalMaxPooling2D()

   if layer is None:
      raise Exception('The requested pooling is not implemented by this model: "{pooling}"')

   return layer



def denseActivation(hp):

   activationName = hp.get('dense_activation')

   if activationName is None:
      activationName = DFLT_ACTIVATION
      print(f'[WARNING]: activation name is not set in hyperparameters: using default value: "{activationName}"')

   activationName = activationName.lower()
   layer = None
   if activationName == 'relu':
      layer = tf.keras.layers.ReLU()
   elif activationName == 'leakyrelu':
      layer = tf.keras.layers.LeakyReLU()

   if layer is None:
      raise Exception('The requested activation function is not implemented by this model: "{activationName}"')

   return layer



def denseWInitializer(hp):

   initializerName = hp.get('dense_weigths_initializer')

   if initializerName is None:
      initializerName = DFLT_WEGHTS_INITIALIZER
      print(f'[WARNING]: weights initializer is not set in hyperparameters: using default value: "{initializerName}"')

   initializerName = initializerName.lower()
   layer = None
   if initializerName == 'glorotnormal':
      layer = tf.keras.initializers.GlorotNormal()
   elif initializerName == 'glorotuniform':
      layer = tf.keras.initializers.GlorotUniform()
   elif initializerName == 'randomnormal':
      layer = tf.keras.initializers.RandomNormal()
   elif initializerName == 'randomuniform':
      layer = tf.keras.initializers.RandomUniform()

   if layer is None:
      raise Exception('The requested weights initializer is not implemented by this model: "{initializerName}"')

   return layer



def denseBInitializer(hp):

   initializerName = hp.get('dense_biases_initializer')

   if initializerName is None:
      initializerName = DFLT_BIASES_INITIALIZER
      print(f'[WARNING]: biases initializer is not set in hyperparameters: using default value: "{initializerName}"')

   initializerName = initializerName.lower()
   layer = None
   if initializerName == 'zeros':
      layer = tf.keras.initializers.Zeros()

   if layer is None:
      raise Exception('The requested biases initializer is not implemented by this model: "{initializerName}"')

   return layer




def addDenseLayer(
      x
   ,  units
   ,  activation
   ,  kernelInitializer
   ,  biasInitializer
   ,  batchNorm
   ,  dropoutRate
):

   x = tf.keras.layers.Dense(
         units              = units
      ,  activation         = activation
      ,  kernel_initializer = kernelInitializer
      ,  bias_initializer   = biasInitializer
   )(x)

   if batchNorm:
      x = tf.keras.layers.BatchNormalization()(x)

   if dropoutRate:
      x = tf.keras.layers.Dropout(dropoutRate)(x)

   return x




def compile(
      model        = None
   ,  modelLoss    = None
   ,  modelMetrics = None
   ,  hp           = None
):

   # Define learning rate
   learningRate = hp.get('learning_rate')
   if learningRate is None:
      print(f'[WARNING]: <learning rate> is not set in hyperparameters: the optimizer\'s learning rate default value will be used !')

   # Define optimizer
   optimizerName = hp.get('optimizer')
   if optimizerName is None:
      optimizerName = DFLT_OPTIMIZER_NAME
      print(f'[WARNING]: optimizer name is not set in hyperparameters: using default one: "{optimizerName}"')

   optimizerName = optimizerName.lower()
   optimizer = None
   if optimizerName == 'sgd':
      optimizer = tf.keras.optimizers.SGD(learning_rate = learningRate)
   elif optimizerName == 'rmsprop':
      optimizer = tf.keras.optimizers.RMSprop(learning_rate = learningRate)
   elif optimizerName == 'adam':
      optimizer = tf.keras.optimizers.Adam(learning_rate = learningRate)
   elif optimizerName == 'adamax':
      optimizer = tf.keras.optimizers.Adamax(learning_rate = learningRate)

   if optimizer is None:
      raise Exception('The requested optimizer is not implemented by this model: "{optimizerName}"')

   # Compile the model
   model.compile(
         optimizer = optimizer
      ,  loss      = modelLoss
      ,  metrics   = modelMetrics
   )

   return model





   # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Classe:
   # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HyperTransferLearningModel(kt.HyperModel):


   #
   # ~~~ CONSTRUCTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   #


   def __init__(self
      ,  nbClasses         = None
      ,  inputShape        = None
      ,  inputTensor       = None
      ,  inputPreprocessFn = None
      ,  modelName         = None
      ,  baseModelFn       = None
      ,  baseModelParams   = None
      ,  freezeBaseModel   = True
      ,  modelLoss         = None
      ,  modelMetrics      = None
      ,  verbose           = False
   ):
      super(HyperTransferLearningModel, self).__init__(name = modelName, tunable = False)

      # Checking parameters
      if nbClasses is None:
         raise ValueError('The mandatory <nbClasses> argument is not set.')
      if inputShape is None and inputTensor is None:
         raise ValueError('You must specify either <inputShape> or <inputTensor>.')
      if baseModelFn is None:
         raise ValueError('The mandatory <baseModelFn> argument is not set.')
      if freezeBaseModel is None:
         raise ValueError('The mandatory <freezeBaseModel> argument is not set correctly: a <boolean> is expected.')

      self.nbClasses         = nbClasses
      self.inputShape        = inputShape
      self.inputTensor       = inputTensor
      self.inputPreprocessFn = inputPreprocessFn
      self.modelName         = modelName
      self.baseModelFn       = baseModelFn
      self.freezeBaseModel   = freezeBaseModel
      self.modelLoss         = modelLoss
      self.modelMetrics      = modelMetrics
      self.verbose           = verbose

      self.baseModel   = None

      # Base model parameters
      self.baseModelParams = None
      if baseModelParams:
         self.baseModelParams = baseModelParams
      else:
         self.baseModelParams = dict()
      if not isinstance(self.baseModelParams, dict):
         raise TypeError('Invalid type for argument <baseModelParams>: a type <dict> was expected.')




   #
   # ~~~ PRIVATE METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   #

   def _msg(self, message):
      if self.verbose:
         print(message)


   def _loadBaseModel(self, params):

      model = None

      if params is None:
         self._msg('[WARNING]: no parameters were given for the Transfer Learning: default values will be used !')
         model = self.baseModelFn()
      else:
         self._msg(f'[INFO]: Building the base model with the following parameters:\n{params}')
         model = self.baseModelFn(**params)

      # Défensif
      if model is None:
         raise Exception('Failed to load Keras Application Model !')

      self._msg(f'[INFO]: successfully loaded base model: "{model.name}"')

      return model




   #
   # ~~~ PUBLIC METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   #
   def build(self, hp):

      inputs  = None
      outputs = None

      self._msg(f'Building model: {self.modelName}')

      # Input layer
      if self.inputTensor is not None:
         #inputs = tf.keras.utils.get_source_inputs(self.inputTensor)
         inputs = self.inputTensor
      else:
         inputs = tf.keras.layers.Input(shape = self.inputShape)

      x = inputs

      # Input preprocessing
      if self.inputPreprocessFn is not None:
         x = self.inputPreprocessFn(x)

      # Load the base model
      self.baseModelParams['include_top']  = False
      self.baseModelParams['input_tensor'] = x
      self.baseModelParams['pooling']      = None
      if self.baseModelParams.get('weights') is None:
         self.baseModelParams['weights'] = DFLT_WEIGHTS_TRANFER_LEARNING_SRC
      self.baseModel = self._loadBaseModel(self.baseModelParams)

      # Freeze the base model ?
      if self.freezeBaseModel:
         self.baseModel.trainable = False

      x = self.baseModel(x, training = False)
      x = self.baseModel.output

      #
      # Build the classifier part of the model
      #

      # Pooling
      x = pooling(hp)(x)

      # num_dense_layers
      numDenseLayers = hp.get('num_dense_layers')
      if numDenseLayers is None:
         raise Exception('Missing hyperparameter <num_dense_layers>')

      # denseUnits
      denseUnits = hp.get('dense_units')
      if denseUnits is None:
         raise Exception('Missing hyperparameter <denseUnits>')

      # denseUseBatchNorm
      batchNorm = hp.get('dense_use_batchnorm')
      if batchNorm is None:
         raise Exception('Missing hyperparameter <dense_use_batchnorm>')

      # dropoutRate
      dropoutRate = hp.get('dropout_rate')
      if dropoutRate is None:
         raise Exception('Missing hyperparameter <dropout_rate>')

      # Dense + Dropout layers
      for i in range(numDenseLayers):

         # denseActivation
         denseActivationLayer = denseActivation(hp)

         # Weights initializer
         denseWInitLayer = denseWInitializer(hp)

         # Biases initializer
         denseBInitLayer = denseBInitializer(hp)

         # Building the Dense layer
         x = addDenseLayer(
               x                 = x
            ,  units             = denseUnits
            ,  activation        = denseActivationLayer
            ,  kernelInitializer = denseWInitLayer
            ,  biasInitializer   = denseBInitLayer
            ,  batchNorm         = batchNorm
            ,  dropoutRate       = dropoutRate
         )

      # Building the model last layer
      activationName = hp.get('classifier_activation')
      outputs = tf.keras.layers.Dense(units = self.nbClasses, activation = activationName)(x)
      self._msg(f'   output layer units: {self.nbClasses}')

      # Build the model
      model = tf.keras.Model(inputs = inputs, outputs = outputs)

      # Compile the model
      model = compile(
            model        = model
         ,  modelLoss    = self.modelLoss
         ,  modelMetrics = self.modelMetrics
         ,  hp           = hp
      )

      return model



   def getNbClasses(self):
      return self.nbClasses


   def getInputShape(self):
      return self.inputShape


