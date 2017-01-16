from bs4 import BeautifulSoup
import requests
import random
import argparse
import time


def get_args():
    parser = argparse.ArgumentParser(
        description='Shows top films sorted by rating www.kinopoisk.ru'
         )
    parser.add_argument('-c', '--cinemas',
                        help='Shows top films sorted by the number of cinemas',
                        action='store_true'
                        )
    args = parser.parse_args()
    return args


def fetch_afisha_page():
    afisha_url = 'http://www.afisha.ru/msk/schedule_cinema/'
    return requests.get(afisha_url)


def parse_afisha_list(afisha_response):
    base_film_info = []
    soup = BeautifulSoup(afisha_response.text, 'lxml')
    film_div = soup.findAll(
        'div',
        {'class': 'object s-votes-hover-area collapsed'}
    )
    for item in film_div:
        for element in item.findAll('h3', {'class': 'usetags'}):
            base_film_info.append({
                'film_title': element.text,
                'cinemas': len(item.findAll(
                    'td',
                    {'class': 'b-td-item'}
                )
                )
            }
            )
    return base_film_info


def search_film(film_title):
    s = requests.Session()
    user_agents = [
     'Mozilla/5.0 (X11; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0',
     'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.17',
     'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
    ]
    header = {'User-Agent': random.choice(user_agents)}
    request_params = {'kp_query': film_title}
    search_url = 'http://kinopoisk.ru/index.php?first=yes&'
    search_response = s.get(search_url, params=request_params, headers=header)
    return search_response


def get_films_info_from_kp(base_film_info):
    sleep_time = 5
    full_film_info = []
    for item in base_film_info:
        film_title = item['film_title']
        search_response = search_film(film_title)
        soup = BeautifulSoup(search_response.text, 'lxml')
        rating_count = soup.find('span', {'class': 'rating_ball'})
        voters_count = soup.find('span', {'class': 'ratingCount'})
        if rating_count is None:
            rating = None
        else:
            rating = rating_count.text
        if voters_count is None:
            voters = None
        else:
            voters = int(voters_count.text.replace('\xa0', ''))
        full_film_info.append({
            'film_title': item['film_title'],
            'cinemas': item['cinemas'],
            'rating': rating,
            'voters': voters
        }
        )
        time.sleep(sleep_time)
    return full_film_info


def get_sorted_films(full_film_info):
    if args.cinemas:
        sorted_films = sorted(full_film_info, key=lambda i: i['cinemas'])
    else:
        sorted_films = sorted(full_film_info,
                              key=lambda i:
                              (i['rating'] is not None, i['rating'])
                              )
    sorted_films.reverse()
    return sorted_films


def output_top_films_to_console(sorted_films):
    top_films = 10
    if args.cinemas:
        print('Top films sorted by the number of cinemas')
    else:
        print('Top films sorted by rating www.kinopoisk.ru:')
    for item in sorted_films[:top_films]:
        print(item['film_title'])


if __name__ == '__main__':
    args = get_args()
    afisha_response = fetch_afisha_page()
    base_film_info = parse_afisha_list(afisha_response)
    full_film_info = get_films_info_from_kp(base_film_info)
    sorted_films = get_sorted_films(full_film_info)
    output_top_films_to_console(sorted_films)
