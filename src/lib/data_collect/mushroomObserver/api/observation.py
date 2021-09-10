# -*- coding: utf-8 -*-

# Import Librairies
#
# Python
import requests
#
# User
from data_collect.mushroomObserver.api import api


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OBSERVATION_TABLE_NAME = 'observations'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CMO_API_GET_Observation(api.CMO_API_GET):
   '''
   DESCRIPTION
      This class implements the code needed to realize Http GET commands on OBSERVATIONS through MushroomObserver API.
   '''

   def __init__(self
      ,  moAPIHttp_GET_obs_req
      ,  moAPIHttp = None
   ):
      '''
      DESCRIPTION
         Constructor for the class CMO_API_GET_Observation.
      ARGUMENTS
         moAPIHttp_GET_obs_req
            Default: no default
            this argument is expected to contain the GET request that must be done on Observations (i.e. the request
            must contain the criteria to filter Observations that are requested).
         moAPIHttp
            Default: None
            this argument corresponds to an instance of CMO_API_HTTP class.
            As a reminder CMO_API_HTTP is the class that implements Http commands through MushroomObserver API.
            If None, then an instance of CMO_API_HTTP class will be created internally by the constructor.
      '''

      global OBSERVATION_TABLE_NAME

      self.__tableName = OBSERVATION_TABLE_NAME

      super().__init__(
            self.__tableName
         ,  moAPIHttp_GET_request = moAPIHttp_GET_obs_req
         ,  moAPIHttp             = moAPIHttp
      )




class CMO_API_GET_Obs_Request(api.CMO_API_GET_REQUEST):
   '''
   DESCRIPTION
      This class implements the object that will be used as request to GET Observations through MushroomObserver API.
   '''

   def __init__(self
      ,  obsId           = None    # Integer | List of integers
      ,  taxonId         = None    # Integer | List of integers
      ,  taxonName       = None    # Sting | List of strings
      ,  hasName         = None    # Boolean
      ,  hasImages       = None    # Boolean
      ,  includeSubtaxa  = None    # Boolean
      ,  includeSynonyms = None    # Boolean
      ,  detail          = 'low'
      ,  format          = 'json'
   ):

      super().__init__()

      if (obsId is not None):
         self.set(key = 'id', value = obsId)

      if (taxonId is not None):
         self.set(key = 'name', value = taxonId)

      if (taxonName is not None):
         self.set(key = 'name', value = taxonName)

      if (hasName is not None):
         self.set(key = 'has_name', value = hasName)

      if (hasImages is not None):
         self.set(key = 'has_images', value = hasImages)

      if (includeSubtaxa is not None):
         self.set(key = 'include_subtaxa', value = includeSubtaxa)

      if (includeSynonyms is not None):
         self.set(key = 'include_synonyms', value = includeSynonyms)

      self.set(key = 'detail', value = detail)

      self.set(key = 'format', value = format)




class CMO_API_Obs_Data:
   '''
   DESCRIPTION
      This class implements the object that will contain the data extracted from the result of an Http GET command on
      OBSERVATION.
   '''

   def __init__(
         self
      ,  obsHttpResult    # CMO_API_HTTP_Result
   ):
      self.__recsetObs       = []
      self.__recsetObsNaming = []
      self.__recsetObsImage  = []

      null_recObs = {
            'id'                   : None
         ,  'date'                 : None
         ,  'views'                : None
         ,  'consensus_id'         : None
         ,  'consensus_name'       : None
         ,  'consensus_rank'       : None
         ,  'consensus_synonym_id' : None
         ,  'location_id'          : None
         ,  'location_name'        : None
         ,  'primary_image_id'     : None
         ,  'primary_image_date'   : None
         ,  'primary_image_license': None
         ,  'primary_image_quality': None
      }

      null_recObsNaming = {
            'obs_id'           : None
         ,  'naming_id'        : None
         ,  'naming_confidence': None
         ,  'name_id'          : None
         ,  'name'             : None
         ,  'name_rank'        : None
         ,  'name_syn_id'      : None
      }

      null_recObsImage = {
            'obs_id'           : None
         ,  'image_id'         : None
         ,  'image_date'       : None
         ,  'image_license'    : None
         ,  'image_quality'    : None
      }

      if (obsHttpResult is not None):

         for obsData in obsHttpResult.get_data():

            obsId           = obsData.get('id')
            obsConsensus    = obsData.get('consensus')
            obsLocation     = obsData.get('location')
            obsNamings      = obsData.get('namings')
            obsPrimaryImage = obsData.get('primary_image')
            obsImages       = obsData.get('images')

            # Observation record
            recObs = null_recObs.copy()
            recObs['id']    = obsId
            recObs['date']  = obsData.get('date')
            recObs['views'] = obsData.get('number_of_views')
            if (obsConsensus is not None):
               recObs['consensus_id']         = obsConsensus.get('id')
               recObs['consensus_name']       = obsConsensus.get('name')
               recObs['consensus_rank']       = obsConsensus.get('rank')
               recObs['consensus_synonym_id'] = obsConsensus.get('synonym_id')
            if (obsLocation is not None):
               recObs['location_id']           = obsLocation.get('id')
               recObs['location_name']         = obsLocation.get('name')
            if (obsPrimaryImage is not None):
               recObs['primary_image_id']      = obsPrimaryImage.get('id')
               recObs['primary_image_date']    = obsPrimaryImage.get('date')
               recObs['primary_image_license'] = obsPrimaryImage.get('license')
               recObs['primary_image_quality'] = obsPrimaryImage.get('quality')
            self.__recsetObs.append(recObs)

            # Observation_naming record
            if (obsNamings is not None):
               for obsNaming in obsNamings:
                  recObsNaming = null_recObsNaming.copy()
                  if (obsNaming is not None):
                     recObsNaming['obs_id']            = obsId
                     recObsNaming['naming_id']         = obsNaming.get('id')
                     recObsNaming['naming_confidence'] = obsNaming.get('confidence')
                     name = obsNaming.get('name')
                     if (name is not None):
                        recObsNaming['name_id']     = name.get('id')
                        recObsNaming['name']        = name.get('name')
                        recObsNaming['name_rank']   = name.get('rank')
                        recObsNaming['name_syn_id'] = name.get('synonym_id')
                     self.__recsetObsNaming.append(recObsNaming)

            # Observation_image recordset
            if (obsImages is not None):
               for obsImage in obsImages:
                  recObsImage = null_recObsImage.copy()
                  if (obsImage is not None):
                     recObsImage['obs_id']        = obsId
                     recObsImage['image_id']      = obsImage.get('id')
                     recObsImage['image_date']    = obsImage.get('date')
                     recObsImage['image_license'] = obsImage.get('license')
                     recObsImage['image_quality'] = obsImage.get('quality')
                     self.__recsetObsImage.append(recObsImage)

   def get_recsetObs(self):
      return self.__recsetObs

   def get_recsetObsNaming(self):
      return self.__recsetObsNaming

   def get_recsetObsImage(self):
      return self.__recsetObsImage
