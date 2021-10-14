import requests


def convertirDireccionACoordenadas(direccion):
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

    return resultado['geometry']['location']['lat'], resultado['geometry']['location']['lng']
