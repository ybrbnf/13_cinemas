from bs4 import BeautifulSoup
import requests
import random
import argparse
import time


def fetch_afisha_page():
    afisha_url = 'http://www.afisha.ru/msk/schedule_cinema/'
    return requests.get(afisha_url)


def parse_afisha_list(afisha_response):
    film_titles = []
    num_of_cinemas = {}
    soup = BeautifulSoup(afisha_response.text, 'lxml')
    film_div = soup.findAll('div', {
     'class': 'object s-votes-hover-area collapsed'
    }
    )
    for item in film_div:
        for element in item.findAll('h3', {'class': 'usetags'}):
            film_titles.append(element.text)
            num_of_cinemas[element.text] = len(item.findAll('td',
                                               {'class': 'b-td-item'}
            )
            )
    return film_titles, num_of_cinemas


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


def get_films_rating_and_voters(film_titles):
    sleep_time = 1
    rating = {}
    voters = {}
    for film_title in film_titles:
        search_response = search_film(film_title)
        soup = BeautifulSoup(search_response.text, 'lxml')
        rating_count = soup.find('span', {'class': 'rating_ball'})
        voters_count = soup.find('span', {'class': 'ratingCount'})
        if rating_count is not None:
            rating[film_title] = rating_count.text
        if voters_count is not None:
            voters[film_title] = voters_count.text
        time.sleep(sleep_time)
    return rating, voters


def get_sorted_films(rating, num_of_cinemas):
    if args.cinemas:
        sorted_films = sorted(num_of_cinemas.items(), key=lambda x: x[1])
    else:
        sorted_films = sorted(rating.items(), key=lambda x: x[1])
    sorted_films.reverse()
    return sorted_films


def output_top_films_to_console(sorted_films):
    top_films = 10
    if args.cinemas:
        print('TOP фильмов, сортированных по количеству мест показа:')
    else:
        print('TOP фильмов, сортированных по рейтингу КИНОПОИСКа:')
    for item in sorted_films[:top_films]:
      print(item[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='help',
                        help='Справкв')
    parser.add_argument('-c', '--cinemas', action="store_true",
                        help='Сортировка по количеству кинотеатров')
    args = parser.parse_args()
    afisha_response = fetch_afisha_page()
    film_titles, num_of_cinemas = parse_afisha_list(afisha_response)
    rating, voters = get_films_rating_and_voters(film_titles)
    sorted_films = get_sorted_films(rating, num_of_cinemas)
    output_top_films_to_console(sorted_films)
