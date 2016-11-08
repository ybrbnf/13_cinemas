from bs4 import BeautifulSoup
import requests

film_names = []
url = 'http://www.afisha.ru/msk/schedule_cinema/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
list_of_films = soup.findAll('h3', {'class': 'usetags'})
for film in list_of_films:
    film_names.append(film.text)  # названия фильмов


qqq = soup.
"""
film_names[20] = film_names[20].replace(' ', '%20')
search_url = 'https://www.kinopoisk.ru/index.php?first=no&what=&kp_query='
search_query = search_url + film_names[20]
response = requests.get(search_query)
soup = BeautifulSoup(response.text, 'lxml')
qwerty = soup.find('p', {'class': 'name'})
film_id = qwerty.a.get('data-id')

film_url = 'https://www.kinopoisk.ru/film/' + film_id
response = requests.get(film_url)
soup = BeautifulSoup(response.text, 'lxml')
rating_ball = soup.find('span', {'class': 'rating_ball'})
rating_count = soup.find('span', {'class': 'ratingCount'})
print (rating_ball.text)
print (rating_count.text)
"""