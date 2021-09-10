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

TAXON_TABLE_NAME = 'names'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CMO_API_GET_Taxon(api.CMO_API_GET):
   '''
   DESCRIPTION
      This class implements the code needed to realize Http GET commands on TAXONS through MushroomObserver API.
   '''

   def __init__(
         self
      ,  moAPIHttp_GET_taxon_req
      ,  moAPIHttp = None
   ):
      '''
      DESCRIPTION
         Constructor for the class CMO_API_GET_Taxon.
      ARGUMENTS
         moAPIHttp_GET_taxon_req
            Default: no default
            this argument is expected to contain the GET request that must be done on Taxons (i.e. the request must
            contain the criteria to filter Taxons that are requested).
         moAPIHttp
            Default: None
            this argument corresponds to an instance of CMO_API_HTTP class.
            As a reminder CMO_API_HTTP is the class that implements Http commands through MushroomObserver API.
            If None, then an instance of CMO_API_HTTP class will be created internally by the constructor.
      '''

      global TAXON_TABLE_NAME

      self.__tableName = TAXON_TABLE_NAME

      super().__init__(
            self.__tableName
         ,  moAPIHttp_GET_request = moAPIHttp_GET_taxon_req
         ,  moAPIHttp             = moAPIHttp
      )




class CMO_API_GET_Taxon_Request(api.CMO_API_GET_REQUEST):
   '''
   DESCRIPTION
      This class implements the object that will be used as request to GET Taxons through MushroomObserver API.
   '''

   def __init__(self
      ,  id                = None
      ,  name              = None
      ,  textNameHas       = None
      ,  rank              = None
      ,  classificationHas = None
      ,  createdAt         = None
      ,  hasClassification = None
      ,  hasDescription    = None
      ,  hasNotes          = None
      ,  hasSynonyms       = None
      ,  includeSubtaxa    = None
      ,  includeSynonyms   = None
      ,  isDeprecated      = None
      ,  location          = None
      ,  misspellings      = None
      ,  detail            = 'low'
      ,  format            = 'json'
   ):
      '''
      DESCRIPTION
            Constructor of CMO_API_GET_Taxon_Request class.
            You just have to provide all criteria you want to use to retrieve only Taxons of concerned.
            Then the constructor will internally produced a corresponding filter that could be used by the
            CMO_API_GET_Taxon's get method to retrieve Taxons.
      ARGUMENTS
            id
               specifies the ID the Taxon you want to get.
            name
               specifies the NAME the Taxon you want to get.
            textNameHas
               specifies a substring
            rank
               specifies the taxonomy rank you are interested in (ex: family, genus, ...)
            detail
               Possible values: { 'low' | 'high' | None }
               Specifies the detail level that the GET method will use to produce the result.
               As a reminder the GET method is implemented by the CMO_API_GET_Taxon class.
            format
               Possible values: { 'json' }
               Specifies the format that the GET method will use to produce the result.
               As a reminder the GET method is implemented by the CMO_API_GET_Taxon class.
      '''

      super().__init__()

      if (id is not None):
         self.set(key = 'id', value = id)

      if (name is not None):
         self.set(key = 'name', value = name)

      if (textNameHas is not None):
         self.set(key = 'text_name_has', value = textNameHas)

      if (rank is not None):
         self.set(key = 'rank', value = rank)

      if (classificationHas is not None):
         self.set(key = 'classification_has', value = classificationHas)

      if (createdAt is not None):
         self.set(key = 'created_at', value = createdAt)

      if (hasClassification is not None):
         self.set(key = 'has_classification', value = hasClassification)

      if (hasDescription is not None):
         self.set(key = 'has_description', value = hasDescription)

      if (hasNotes is not None):
         self.set(key = 'has_notes', value = hasNotes)

      if (hasSynonyms is not None):
         self.set(key = 'has_synonyms', value = hasSynonyms)

      if (includeSubtaxa is not None):
         self.set(key = 'include_subtaxa', value = includeSubtaxa)

      if (includeSynonyms is not None):
         self.set(key = 'include_synonyms', value = includeSynonyms)

      if (isDeprecated is not None):
         self.set(key = 'is_deprecated', value = isDeprecated)

      if (location is not None):
         self.set(key = 'location', value = location)

      if (misspellings is not None):
         self.set(key = 'misspellings', value = misspellings)

      self.set(key = 'detail', value = detail)

      self.set(key = 'format', value = format)




class CMO_API_Taxon_Data:
   '''
   DESCRIPTION
      This class implements the object that will contain the data extracted from the result of an Http GET command on
      TAXON.
   '''

   def __init__(
         self
      ,  taxonHttpResult         # CMO_API_HTTP_Result
   ):
      self.__recsetTaxon        = []
      self.__recsetTaxonParent  = []
      self.__recsetTaxonSynonym = []

      null_recTaxon = {
            'id'         : None
         ,  'name'       : None
         ,  'rank'       : None
         ,  'deprecated' : None
         ,  'misspelled' : None
         ,  'views'      : None
      }

      null_recTaxonParent = {
            'taxon_id'    : None
         ,  'parent_name' : None
         ,  'parent_rank' : None
      }

      null_recTaxonSynonym = {
            'taxon_id'           : None
         ,  'id'                 : None
         ,  'synonym_name'       : None
         ,  'synonym_rank'       : None
         ,  'synonym_deprecated' : None
         ,  'synonym_id'         : None
      }

      if (taxonHttpResult is not None):

         for taxonData in taxonHttpResult.get_data():

            taxonId       = taxonData.get('id')
            taxonParents  = taxonData.get('parents')
            taxonSynonyms = taxonData.get('synonyms')

            # Taxon record
            recTaxon = null_recTaxon.copy()
            recTaxon['id']         = taxonId
            recTaxon['name']       = taxonData.get('name')
            recTaxon['rank']       = taxonData.get('rank')
            recTaxon['deprecated'] = taxonData.get('deprecated')
            recTaxon['misspelled'] = taxonData.get('misspelled')
            recTaxon['views']      = taxonData.get('number_of_views')
            self.__recsetTaxon.append(recTaxon)

            # Taxon_parent record
            if (taxonParents is not None):
               for parent in taxonParents:
                  recTaxonParent = null_recTaxonParent.copy()
                  if (parent is not None):
                     recTaxonParent['taxon_id'] = taxonId
                     recTaxonParent['parent_name'] = parent.get('name')
                     recTaxonParent['parent_rank'] = parent.get('rank')
                     self.__recsetTaxonParent.append(recTaxonParent)

            # Taxon_synonym recordset
            if (taxonSynonyms is not None):
               for synonym in taxonSynonyms:
                  recTaxonSynonym = null_recTaxonSynonym.copy()
                  if (synonym is not None):
                     recTaxonSynonym['taxon_id']           = taxonId
                     recTaxonSynonym['id']                 = synonym.get('id')
                     recTaxonSynonym['synonym_name']       = synonym.get('name')
                     recTaxonSynonym['synonym_rank']       = synonym.get('rank')
                     recTaxonSynonym['synonym_deprecated'] = synonym.get('deprecated')
                     recTaxonSynonym['synonym_id']         = synonym.get('synonym_id')
                     self.__recsetTaxonSynonym.append(recTaxonSynonym)

   def get_recsetTaxon(self):
      return self.__recsetTaxon

   def get_recsetTaxonParent(self):
      return self.__recsetTaxonParent

   def get_recsetTaxonSynonym(self):
      return self.__recsetTaxonSynonym
