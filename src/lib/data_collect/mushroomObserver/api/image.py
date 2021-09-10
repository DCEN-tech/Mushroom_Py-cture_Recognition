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

IMAGE_TABLE_NAME = 'images'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CMO_API_GET_Image(api.CMO_API_GET):
   '''
   DESCRIPTION
      This class implements the code needed to realize Http GET commands on IMAGES through MushroomObserver API.
   '''

   def __init__(
         self
      ,  moAPIHttp_GET_image_req
      ,  moAPIHttp = None
   ):
      '''
      DESCRIPTION
         Constructor for the class CMO_API_GET_Image.
      ARGUMENTS
         moAPIHttp_GET_image_req
            Default: no default
            this argument is expected to contain the GET request that must be done on Images (i.e. the request must
            contain the criteria to filter Images that are requested).
         moAPIHttp
            Default: None
            this argument corresponds to an instance of CMO_API_HTTP class.
            As a reminder CMO_API_HTTP is the class that implements Http commands through MushroomObserver API.
            If None, then an instance of CMO_API_HTTP class will be created internally by the constructor.
      '''

      global IMAGE_TABLE_NAME

      self.__tableName = IMAGE_TABLE_NAME

      super().__init__(
            self.__tableName
         ,  moAPIHttp_GET_request = moAPIHttp_GET_image_req
         ,  moAPIHttp             = moAPIHttp
      )




class CMO_API_GET_Image_Request(api.CMO_API_GET_REQUEST):
   '''
   DESCRIPTION
      This class implements the object that will be used as request to GET Images through MushroomObserver API.
   '''

   def __init__(self
      ,  imageId         = None
      ,  name            = None           # name list
      ,  observation     = None           # observation list
      ,  confidence      = None           # confidence range (limit=-3..3)
      ,  contentType     = None           # bmp | gif | jpg | png | raw | tiff
      ,  createdAt       = None           # time range
      ,  date            = None           # date range (when photo taken)
      ,  hasNotes        = None           # boolean
      ,  hasObservation  = None           # boolean
      ,  hasVotes        = None           # boolean
      ,  includeSubtaxa  = None           # boolean
      ,  includeSynonyms = None           # boolean
      ,  license         = None
      ,  location        = None
      ,  okForExport     = None           # boolean
      ,  project         = None           # project list
      ,  quality         = None           # quality range (limit=1..4)
      ,  size            = None           # limit = huge | large | medium | small | thumbnail,
                                          # width or height at least:
                                          #     160 for thumbnail
                                          #     320 for small
                                          #     640 for medium
                                          #     960 for large
                                          #     1280 for huge
      ,  detail          = 'low'
      ,  format          = 'json'
   ):

      super().__init__()

      if (imageId is not None):
         self.set(key = 'id', value = imageId)

      if (name is not None):
         self.set(key = 'name', value = name)

      if (observation is not None):
         self.set(key = 'observation', value = observation)

      if (confidence is not None):
         self.set(key = 'confidence', value = confidence)

      if (contentType is not None):
         self.set(key = 'content_type', value = contentType)

      if (createdAt is not None):
         self.set(key = 'created_at', value = createdAt)

      if (date is not None):
         self.set(key = 'date', value = date)

      if (hasNotes is not None):
         self.set(key = 'has_notes', value = hasNotes)

      if (hasObservation is not None):
         self.set(key = 'has_observation', value = hasObservation)

      if (hasVotes is not None):
         self.set(key = 'has_notes', value = hasVotes)

      if (includeSubtaxa is not None):
         self.set(key = 'include_subtaxa', value = includeSubtaxa)

      if (includeSynonyms is not None):
         self.set(key = 'include_synonyms', value = includeSynonyms)

      if (license is not None):
         self.set(key = 'license', value = license)

      if (location is not None):
         self.set(key = 'location', value = location)

      if (okForExport is not None):
         self.set(key = 'ok_for_export', value = okForExport)

      if (project is not None):
         self.set(key = 'project', value = project)

      if (quality is not None):
         self.set(key = 'quality', value = quality)

      if (size is not None):
         self.set(key = 'size', value = size)

      self.set(key = 'detail', value = detail)

      self.set(key = 'format', value = format)




class CMO_API_Image_Data:
   '''
   DESCRIPTION
      This class implements the object that will contain the data extracted from the result of an Http GET command on
      IMAGE.
   '''

   def __init__(
         self
      ,  imgHttpResult    # CMO_API_HTTP_Result
   ):
      self.__recsetImg        = []
      self.__recsetImgFile    = []
      self.__recsetImgObsIdsr = []

      null_recImg = {
            'id'                   : None
         ,  'date'                 : None
         ,  'notes'                : None
         ,  'quality'              : None
         ,  'views'                : None
         ,  'ok_for_export'        : None
         ,  'license'              : None
         ,  'content_type'         : None
         ,  'width'                : None
         ,  'height'               : None
      }

      null_recImgFile = {
            'image_id' : None
         ,  'file_url' : None
      }

      null_recImgObsIdsr = {
            'image_id'         : None
         ,  'observation_idsr' : None
      }

      if (imgHttpResult is not None):

         for imgData in imgHttpResult.get_data():

            imgId       = imgData.get('id')
            imgFiles    = imgData.get('files')
            imgObsIdsrs = imgData.get('observation_idsr')

            # Image record
            recImg = null_recImg.copy()
            recImg['id']           = imgId
            recImg['date']         = imgData.get('date')
            recImg['notes']        = imgData.get('notes')
            recImg['quality']      = imgData.get('quality')
            recImg['views']        = imgData.get('number_of_views')
            recImg['ok_for_export']= imgData.get('ok_for_export')
            recImg['license']      = imgData.get('license')
            recImg['content_type'] = imgData.get('content_type')
            recImg['width']        = imgData.get('width')
            recImg['height']       = imgData.get('height')
            self.__recsetImg.append(recImg)

            # Image_files record
            if (imgFiles is not None):
               for fileUrl in imgFiles:
                  recImgFile = null_recImgFile.copy()
                  recImgFile['image_id'] = imgId
                  recImgFile['file_url'] = fileUrl
                  self.__recsetImgFile.append(recImgFile)

            # Image_Observation_idsr recordset
            if (imgObsIdsrs is not None):
               for obsIdsr in imgObsIdsrs:
                  recImgObsIdsr = null_recImgObsIdsr.copy()
                  recImgObsIdsr['image_id']         = imgId
                  recImgObsIdsr['observation_idsr'] = obsIdsr
                  self.__recsetImgObsIdsr.append(recImgObsIdsr)

   def get_recsetImg(self):
      return self.__recsetImg

   def get_recsetImgFile(self):
      return self.__recsetImgFile

   def get_recsetImgObsIdsr(self):
      return self.__recsetImgObsIdsr
