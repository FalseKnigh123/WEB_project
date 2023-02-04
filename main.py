from io import BytesIO
import pygame
import requests
import sys
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = "Москва, ул. Ак. Королева, 12"

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
if not response:
    sys.exit()

if __name__ == "__main__":
    image = response.content
    pygame.init()
    pygame.display.set_caption("ЭТО БАЗА")
    size = wight, height = 800, 600
    screen = pygame.display.set_mode(size)
    fps = 50
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fon = pygame.transform.scale(pygame.image.fromstring(image, (800, 600), "RGB"), (wight, height))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()