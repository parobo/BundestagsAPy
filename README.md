# BundestagsAPy: A python wrapper for the Bundestags DIP API.
## Installation
The easiest way to install the latest stable version from PyPI is by using pip:

```
pip install bundestagsapy
```
Alternatively, install directly from the GitHub repository:

```
pip install git+https://github.com/parobo/BundestagsAPy
```

## Usage
To use the API wrapper, simply call the client object with your API key.
See https://dip.bundestag.de/%C3%BCber-dip/hilfe/api#content on how to get an API key.

### Initialization
```Python
import BundestagsAPy
api_key='XXXXXXXXXXXXXXX'
client = BundestagsAPy.Client(api_key)
```
### Endpoints
The client provides access to all available documents through methods named after the endpoints (`bt_{endpoint}`). E.g.
```Python
client.bt_aktivitaet(max_results=50,id,start_date,end_date,drucksache,plenaeprotokoll,zuordnung)
```
The available endpoint are:
- aktivitaet: `bt_aktivitaet()`
- drucksache: `bt_drucksache()`
- drucksache-text: `bt_drucksache_text()`
- person: `bt_person()`
- plenarprotokoll: `bt_plenarprotokoll()`
- plenarprotokoll-text: `bt_plenarprotokoll_text()`
- vorgang: `bt_vorgang()`
- vorgangsposition: `bt_vorgangsposition()`

All methods accept `max_results` as input. It takes either an interger as value, in which case the method returns the first `max_results` supplied by the API, or `False`, in which case all available documents are returned.

`id` can either be an integer (for single document returned) or a list of integers (for multiple).

see https://dip.bundestag.de/documents/informationsblatt_zur_dip_api.pdf for details on other acceptable parameters for each endpoint.

### Results
The results from each request to an endpoint is an object named after the document requested if a single document was requested. Each object has as its attributes all the available data named in the same way as documented on https://dip.bundestag.de/documents/informationsblatt_zur_dip_api.pdf.

If multiple documents were requested, BundestagsAPy returns a list of the documents. E.g.

```Python
for result in client.bt_aktivitaet(max_results=False, start_date='2020-01-01',end_date='2020-01-02'):
	print(result.id,result.titel)
```
