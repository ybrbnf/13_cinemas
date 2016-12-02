Скрипт формирует список фильмов отсортированный по рейтингу или по количеству кинотеатров, в которых идет показ этого фильма. Исходные данные (название фильма и количество кинотеатров) берутся с сайта http://www.afisha.ru/msk/schedule_cinema/. Рейтинг фильма берется с сайта www.kinopoisk.ru. 

<hr>>

ЗАПУСК.

Запуск из командной строки: python3.5 cinemas.py [key]
Для сортировки по рейтингу используется ключ '-r', для сортировки по количеству кинотеатров '-с'.
Запуск без ключа невозможен

<hr>

ТРЕБОВАНИЯ

Python3.5
BeautifulSoup (<a href=https://pypi.python.org/pypi/beautifulsoup4>документация</a>)
Requests (<a href=http://docs.python-requests.org/en/master/>документация</a>)
