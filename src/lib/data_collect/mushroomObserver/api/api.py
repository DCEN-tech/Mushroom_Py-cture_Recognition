# -*- coding: utf-8 -*-

# Importing needed modules
import requests
import time



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASE_API_URL = 'https://mushroomobserver.org/api2'
DFLT_HTTP_DELAY_SEC = 5


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CMO_API_HTTP:
   '''
   DESCRIPTION
      This class implements Http commands accessible through MushroomObserver API.
      As our needs are only to be able to download data from MushroomObserver website, only the Http GET method as been
      implemented inside this class.
   '''

   def __init__(
        self
      , base_api_url = BASE_API_URL
      , httpDelaySec = DFLT_HTTP_DELAY_SEC
   ):
      f'''
      DESCRIPTION
         Constructor for the class CMO_API_HTTP.
      ARGUMENTS
         base_api_url
            Default value: {BASE_API_URL}
            this is the url prefix that is used by MushroomObserver API.
            You should use the default value unless you know what you are doing.
         httpDelaySec
            Default value: {DFLT_HTTP_DELAY_SEC}
            this parameter is the delay you want to use between two Http commands.
            The main purpose of this argument is to prevent to flood the MushroomObserver website by reducing the number
            of Http commands per unit of time.
      '''
      self.__base_api_url = base_api_url
      if not (httpDelaySec is None or type(httpDelaySec) == int):
         raise TypeError('Invalid type for argument: <httpDelaySec>. Expected type: None | int.')
      self.__httpDelaySec = httpDelaySec


   def get_baseAPIUrl(self):
      return self.__base_api_url


   def get_httpDelay(self):
      return self.__httpDelaySec


   def get(
        self
      , url
      , params
      , httpDelaySec = None
      , verbose      = False
   ):
      if (httpDelaySec is not None):
         delaySec = httpDelaySec
      else:
         delaySec = 0 if (self.__httpDelaySec is None) else self.__httpDelaySec

      # Defensif
      if (delaySec is None):
         delaySec = 0

      if (verbose):
         print('[DEBUG]: HTTP GET with:')
         print('\turl   : ', url)
         print('\tparams: ', params)
         print('\tdelay : ', delaySec)

      if (delaySec > 0):
         if (verbose):
            print('[DEBUG]: HTTP GET request delayed for ', delaySec, ' second(s)', flush=True)
            time.sleep(delaySec)

      httpResult = requests.get(url, params)

      httpCode = httpResult.status_code

      httpResult = httpResult.json()

      if (httpResult is None):
         success  = False
         error    = 'Conversion to JSON format failed.'
         data     = None
         metadata = None
      else:
         success  = True if (httpCode == 200) else False
         error    = httpResult.pop('errors', None)
         data     = httpResult.pop('results', None)
         metadata = httpResult

      if (verbose):
         print('[DEBUG]: HTTP return: ')
         print('[DEBUG]:\tsuccess           : ', str(success))
         print('[DEBUG]:\tcode              : ', httpCode)
         print('[DEBUG]:\terror             : ', error)
         if (metadata is not None):
            print('[DEBUG]:\tnumber_of_records : ', metadata.get('number_of_records'))
            print('[DEBUG]:\tnumber_of_pages   : ', metadata.get('number_of_pages'))
            print('[DEBUG]:\tpage_number       : ', metadata.get('page_number'), flush=True)

      return CMO_API_HTTP_Result(
            success
         ,  httpCode
         ,  error
         ,  metadata
         ,  data
      )



class CMO_API_HTTP_Result:

   def __init__(
        self
      , success  = None
      , httpCode = None
      , error    = None
      , metadata = None
      , data     = None
   ):
      self.__success  = success
      self.__httpCode = httpCode
      self.__error    = error
      self.__metadata = metadata
      self.__data     = data
      self.__end      = False


   def __getInt(self, intValue):
      if (intValue is None):
         return 0
      else:
         return intValue


   def isSuccess(self):
      return self.__success


   def get_httpCode(self):
      return self.__httpCode


   def get_error(self):
      return self.__error


   def get_metadata(self):
      return self.__metadata


   def get_data(self):
      return self.__data


   def get_currentPage(self):
      return self.__getInt(self.__metadata.get('page_number'))


   def get_nbPages(self):
      return self.__getInt(self.__metadata.get('number_of_pages'))


   def get_nbRecords(self):
      return self.__getInt(self.__metadata.get('number_of_records'))


   def hasMoreData(self):
      curPage = self.get_currentPage()
      nbPages = self.get_nbPages()
      if ( (curPage is None) or (nbPages is None) ):
         return True
      else:
         return (curPage < nbPages)




class CMO_API_GET:
   '''
   DESCRIPTION
      This the base class to implement the code that realizes Http GET commands on different tables through
      MushroomObserver API.
   '''

      #
      #~~~ method: __init__
      #
   def __init__(
         self
      ,  tableName
      ,  moAPIHttp_GET_request
      ,  moAPIHttp = None
   ):
      self.__moAPIHttp_request = moAPIHttp_GET_request

      if (moAPIHttp is None):
         self.__moAPIHttp = CMO_API_HTTP()
      else:
         self.__moAPIHttp = moAPIHttp

      self.__params         = self.__moAPIHttp_request.get().copy()
      self.__url            = moAPIHttp.get_baseAPIUrl() + '/' + tableName
      self.__params['page'] = 1
      self.__result         = None



      #
      #~~~ method: get
      #
   def get(self
      ,  httpDelaySec = None
      ,  verbose      = False
   ):

      if ( (self.__result is None)
           or self.__result.hasMoreData()
         ):
         # Sending the request
         self.__result = self.__moAPIHttp.get(
               url          = self.__url
            ,  params       = self.__params
            ,  httpDelaySec = httpDelaySec
            ,  verbose      = verbose
        )

         # Http request is a success
         if ( self.__result.isSuccess()
             and (self.__result.get_error() == None)
           ):
            # on se positionne sur la prochaine page
            self.__params['page'] += 1
            # On renvoie True si le résultat contient des enregistements, False autrement
            return ( self.__result.get_nbRecords() > 0 )

         # Http request has failed
         else:
            return False

      # Il n'y a plus d'enregistrement à retourner
      else:
         return False



      #~~~~~~~~~~~~~~~~~~~~~~
      #~~~ method: get_result
      #~~~~~~~~~~~~~~~~~~~~~~
   def get_result(self):
      return self.__result



      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      #~~~ class: CMO_API_GET_REQUEST
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CMO_API_GET_REQUEST:

   def __init__(self):
      self.__params = {}

   def set(self,
         key
      ,  value
   ):
      self.__params[key] = value

   def get(self):
      return self.__params
