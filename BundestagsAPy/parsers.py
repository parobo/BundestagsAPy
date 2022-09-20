import json as json_lib

class Parser:
    def __init__(self):
        pass

    def parse_json(self,payload,model,payload_list=False):
        try:
            json = json_lib.loads(payload)
        except Exception as e:
            raise BundestagsAPyException(f'Failed to parse JSON payload: {e}')
        if 'cursor' in json:
            cursor = json['cursor']
        else:
            cursor = None
        if 'numFound' in json:
            numFound = json['numFound']
        else:
            numFound=None
        if payload_list:
            result = model.parse_list(json)
        else:
            result = model.parse(json)   
        if cursor:
            if numFound or numFound==0:
                return result, cursor, numFound
            else:
                return result, cursor
        else:
            return result