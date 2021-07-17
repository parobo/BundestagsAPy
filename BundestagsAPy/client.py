import requests
import logging
import sys
from platform import python_version
log = logging.getLogger(__name__)
import time
from BundestagsAPy.errors import (
    BadRequest, Forbidden, HTTPException, NotFound, TooManyRequests,
    BundestagsAPyException, Unauthorized)
from BundestagsAPy.models import (Fundstelle,Aktivitaet,Drucksache,DrucksacheText,
                    Person,Plenarprotokoll,PlenarprotokollText,Vorgang,Vorgangsposition)
from BundestagsAPy.parsers import Parser

class Client:
    def __init__(self,api_key=None,retry_count=0,retry_delay=0,retry_errors=None,
                timeout=60,user_agent=None):
        if api_key==None:
            raise BundestagsAPyException("API Key is required. See https://dip.bundestag.de/%C3%BCber-dip/hilfe/api#content on how to get a valid API Key.")
        self.api_key=api_key
        self.retry_count=retry_count
        self.retry_errors=retry_errors
        self.retry_delay=retry_delay
        if user_agent is None:
            user_agent = (
                f"Python/{python_version()} "
                f"Requests/{requests.__version__} "
                )
        self.user_agent=user_agent
        self.session = requests.Session()
        self.parser=Parser()
    
    def call(
        self,endpoint,model,id=None,endpoint_parameters=(),
        headers=None,params=None,payload_list=False,**kwargs):
        if headers is None:
            headers = {}
        headers["User-Agent"]=self.user_agent
        headers['Authorization']=f"ApiKey {self.api_key}"

        #build URL
        if id is not None:
            url = f"https://search.dip.bundestag.de/api/v1/{endpoint}/{id}"
        else:
            url = f"https://search.dip.bundestag.de/api/v1/{endpoint}"
        
        if params is None:
            params = {}
            params['format']='json'
    
        for k, arg in kwargs.items():
            if arg is None:
                continue
            if k not in endpoint_parameters:
                log.warning(f'Unexpected parameter: {k}')
            if k in ['format','cursor']:
                params[k] = str(arg)
            elif k =='start_date':
                params['f.datum.start'] = str(arg)
            elif k =='end_date':
                params['f.datum.end'] = str(arg)
            else:
                params[f"f.{k}"] = str(arg)
        log.debug("PARAMS: %r", params)
        
        try:
            #attempt request until it is successful or the maximum
            #retries are reached
            retries_performed = 0
            while retries_performed<=self.retry_count:
                try:
                    response = self.session.request(
                        'GET',url,params=params,headers=headers)
                except Exception as e:
                    raise BundestagsAPyException(f"Failed to send request: {e}").with_traceback(sys.exc_info()[2])
                
                if response.status_code==200:
                    break
            
                retry_delay = self.retry_delay
            
                if not self.retry_errors or response.status_code not in self.retry_errors:
                    break
            
                # Sleep before retrying request again
                time.sleep(retry_delay)
                retries_performed += 1
        
            #Exceptions for Errors
            self.last_response = response
            
            if response.status_code == 400:
                raise BadRequest(response)
            if response.status_code == 401:
                raise Unauthorized(response)
            if response.status_code == 403:
                raise Forbidden(response)
            if response.status_code == 404:
                raise NotFound(response)
            if response.status_code == 429:
                raise TooManyRequests(response)
            if response.status_code and not response.status_code==200:
                raise HTTPException(response)
        
            # Parse the response payload
            parser=self.parser
            result = parser.parse_json(
                response.text, model=model,payload_list=payload_list)
            
            return result
        finally:
            self.session.close()
    
    def get_data(self,endpoint,model,max_results=50,endpoint_parameters=(),**kwargs):
        #run the actual request and iterate through cursor
        #if the request is only for one file
        if 'id' in kwargs:
            id = kwargs['id']
            if isinstance(id,list):
                if len(id)==1:
                    return self.call(endpoint,model=model,id=id[0],
                                     endpoint_parameters=endpoint_parameters)
            elif isinstance(id,int):
                return self.call(endpoint,model=model,id=id,
                                 endpoint_parameters=endpoint_parameters)
        
        #all other cases
        results_collected = 0
        total_results=1
        results = []
        while results_collected < max_results or not max_results:
            result = self.call(endpoint,model=model,
                               endpoint_parameters=endpoint_parameters,payload_list=True,
                              **kwargs)
            if isinstance(result,tuple):
                results = results + result[0]
                results_collected+=len(result[0])
                kwargs['cursor']=result[1]
                total_results=result[2]
                if results_collected>=total_results:
                    break
            else:
                results = results + result[0]
                break     
        return results
    
    #Aktivitaet requests
    def bt_aktivitaet(self,max_results = 50, **kwargs):
        """
        bt_aktivitaet(id,start_date,end_date,drucksache,
            plenarprotokoll,zuordnung,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date', 'drucksache', 'plenarprotokoll', 'zuordnung',
                'format', 'cursor')
        
        model =Aktivitaet()   
        return self.get_data('aktivitaet',model,max_results,endpoint_parameters,**kwargs)
    
    #Drucksache requests
    def bt_drucksache(self,max_results = 50, **kwargs):
        """
        bt_drucksache(id,start_date,end_date,zuordnung,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date', 'zuordnung',
                'format', 'cursor')
        
        model =Drucksache()   
        return self.get_data('drucksache',model,max_results,endpoint_parameters,**kwargs)
    
    #DrucksacheText requests
    def bt_drucksache_text(self,max_results = 50, **kwargs):
        """
        bt_drucksache_text(id,start_date,end_date,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date','format', 'cursor')
        
        model =DrucksacheText()   
        return self.get_data('drucksache-text',model,max_results,endpoint_parameters,**kwargs)
    
    #Person requests
    def bt_person(self,max_results = 50, **kwargs):
        """
        bt_person(id,start_date,end_date,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date','format', 'cursor')
        
        model = Person()   
        return self.get_data('person',model,max_results,endpoint_parameters,**kwargs)
    
    #Plenarprotokoll requests
    def bt_plenarprotokoll(self,max_results = 50, **kwargs):
        """
        bt_plenarprotokoll(id,start_date,end_date,zuordnung,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date','zuordnung','format', 'cursor')
        
        model = Plenarprotokoll()   
        return self.get_data('plenarprotokoll',model,max_results,endpoint_parameters,**kwargs)

    #PlenarprotokollText requests
    def bt_plenarprotokoll_text(self,max_results = 50, **kwargs):
        """
        bt_plenarprotokoll_text(id,start_date,end_date,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date','format', 'cursor')
        
        model = PlenarprotokollText()   
        return self.get_data('plenarprotokoll-text',model,max_results,endpoint_parameters,**kwargs)
    
    #Vorgang requests
    def bt_vorgang(self,max_results = 50, **kwargs):
        """
        bt_vorgang(id,start_date,end_date,drucksache,
            plenarprotokoll,format,max_results,cursor)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date', 'drucksache', 'plenarprotokoll',
                'format', 'cursor')
        
        model =Vorgang()   
        return self.get_data('vorgang',model,max_results,endpoint_parameters,**kwargs)
    
    #Vorgang requests
    def bt_vorgangsposition(self,max_results = 50, **kwargs):
        """
        bt_vorgangsposition(id,start_date,end_date,drucksache,
            plenarprotokoll,vorgang,zuordnung,format,max_results,cursor,)
            
        Returns the at least the first 50 results.
        max_results may be False, in which case all results will be returned
        """
        #define endpoint parameters
        endpoint_parameters=(
                'id', 'start_date', 'end_date', 'drucksache', 'plenarprotokoll','vorgang','zuordnung',
                'format', 'cursor')
        
        model =Vorgangsposition()   
        return self.get_data('vorgangsposition',model,max_results,endpoint_parameters,**kwargs)
    