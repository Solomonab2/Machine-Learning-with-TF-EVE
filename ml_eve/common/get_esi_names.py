""" takes a list of id numbers and calls Eve's ESI API to return a list of names """
import json
import requests
def get(id_list):
    try:
        id_list
        headers = {'accept': 'application/json', 'Cache-Control': 'no-cache', }
        params = {'datasource': 'tranquility', }
        esi_response = requests.post('https://esi.evetech.net/latest/universe/names/', headers=headers, params=params,
                                     json=id_list)
        esi_data = json.loads(esi_response.text)
        return esi_data
    except Exception as e:
        return "N/A"