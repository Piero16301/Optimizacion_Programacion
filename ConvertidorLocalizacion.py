import requests


class ConvertidorLocalizacion:
    def __init__(self):
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
                'key': 'AIzaSyDXwhfcs7ssjeFlSVe7OWboZVG-G1z69Tc',
                'address': direccion,
                'sensor': 'false',
                'region': 'peru',
                'language': 'es'
            }

            request = requests.get(URLGoogleMaps, params=parametros)
            response = request.json()
            resultado = response['results'][0]

            direccionFormal = resultado['formatted_address']
            latitud = resultado['geometry']['location']['lat']
            longitud = resultado['geometry']['location']['lng']

            self.direcciones[centro] = {"direccionFormal": direccionFormal, "latitud": latitud, "longitud": longitud}

            return direccionFormal, latitud, longitud
