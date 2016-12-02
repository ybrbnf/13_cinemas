from bs4 import BeautifulSoup
import requests
import time
import random
import argparse


def fetch_afisha_page():
    afisha_url = 'http://www.afisha.ru/msk/schedule_cinema/'
    return requests.get(afisha_url)


def parse_afisha_list(afisha_response):
    film_titles = []
    num_of_cinemas = []
    soup = BeautifulSoup(afisha_response.text, 'lxml')
    film_div = soup.findAll('div', {
     'class': 'object s-votes-hover-area collapsed'
                                    }
                            )
    for item in film_div:
        for element in item.findAll('h3', {'class': 'usetags'}):
            film_titles.append(element.text)
        num_of_cinemas.append(len(item.findAll('td', {'class': 'b-td-item'})))
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


def get_rating_and_voters(film_titles):
    rating = []
    voters = []
    sleep_time = 1
    for film_title in film_titles:
        search_response = search_film(film_title)
        soup = BeautifulSoup(search_response.text, 'lxml')
        rating_count = soup.find('span', {'class': 'rating_ball'})
        voters_count = soup.find('span', {'class': 'ratingCount'})
        if rating_count is None:
            rating_count = '0'
        else:
            rating_count = rating_count.text
        if voters_count is None:
            voters_count = '0'
        else:
            voters_count = voters_count.text
        rating.append(rating_count)
        voters.append(voters_count)
        time.sleep(sleep_time)
    return rating, voters


def get_film_info(film_titles,
                  num_of_cinemas,
                  rating,
                  voters):
    film_info = zip(film_titles, num_of_cinemas, voters, rating)
    return film_info


def get_sorted_film(film_info):
    if args.rating:
        sorted_film_info = sorted(film_info, key=lambda i: i[3], reverse=True)
    elif args.cinemas:
        sorted_film_info = sorted(film_info, key=lambda i: i[1], reverse=True)
    return sorted_film_info


def output_top_film_to_console(sorted_film_info):
    top_films = 10
    if args.rating:
        print('Сортировка по рейтингу на www.kinopoisk.ru')
        for item in range(top_films):
            print(sorted_film_info[item][0], '-', sorted_film_info[item][3])
    if args.cinemas:
        print('Сортировка по количеству кинотеатров')
        for item in range(top_films):
            print(sorted_film_info[item][0], '-', sorted_film_info[item][1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-r', '--rating', action="store_true",
                        help='Сортировка по рейтингу')
    parser.add_argument('-c', '--cinemas', action="store_true",
                        help='Сортировка по количеству кинотеатров')
    args = parser.parse_args()
    if not args.rating and not args.cinemas:
        print('Необходимо указать ключ сортировки. Читай README.md')
        exit()
    print('парсим afisha.ru')
    afisha_response = fetch_afisha_page()
    film_titles, num_of_cinemas = parse_afisha_list(afisha_response)
    print('получаем данные с kinopoisk.ru')
    rating, voters = get_rating_and_voters(film_titles)
    film_info = get_film_info(film_titles,
                              num_of_cinemas,
                              rating,
                              voters)
    print('обработка результатов')
    sorted_film_info = get_sorted_film(film_info)
    output_top_film_to_console(sorted_film_info)
