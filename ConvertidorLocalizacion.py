import requests
import json


class ConvertidorLocalizacion:
    def __init__(self):
        credenciales = json.load(open('credenciales.json'))
        self.mapsToken = credenciales['keyGoogleMaps']
        self.direcciones = {}

    def convertirDireccionACoordenadas(self, centro, direccion):
        if centro in self.direcciones:
            direccionFormal = self.direcciones[centro]['direccionFormal']
            latitud = self.direcciones[centro]['latitud']
            longitud = self.direcciones[centro]['longitud']
            return direccionFormal, latitud, longitud

        else:
            URLGoogleMaps = 'https://maps.googleapis.com/maps/api/geocode/json'

            parametros = {
                'key': self.mapsToken,
                'address': direccion,
                'sensor': 'false',
                'region': 'peru',
                'language': 'es'
            }

            request = requests.get(URLGoogleMaps, params=parametros)
            response = request.json()

            if len(response['results']) == 0:
                self.direcciones[centro] = {"direccionFormal": 'No encontrado', "latitud": 0,
                                            "longitud": 0}
                return 'No encontrado', 0, 0
            else:
                resultado = response['results'][0]

            direccionFormal = resultado['formatted_address']
            latitud = resultado['geometry']['location']['lat']
            longitud = resultado['geometry']['location']['lng']

            self.direcciones[centro] = {"direccionFormal": direccionFormal, "latitud": latitud, "longitud": longitud}

            return direccionFormal, latitud, longitud
