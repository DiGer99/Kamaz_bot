import datetime
from bs4 import BeautifulSoup
import requests


class Schedule:
    def __init__(self, fr, to, lst_schedule):
        self.fr = fr # От какого числа расписание на неделю
        self.to = to # До какого числа
        self._lst_schedule = lst_schedule # Список с расписанием на неделю

    # Создаем словарь с датами и раписанием -- 9.11: Выходной
    def schedule(self) -> dict:
        cal: dict[str, str] = {}
        now_month = datetime.datetime.now().month
        for day, dsc in zip(range(self.fr, self.to + 1), self._lst_schedule):
            cal.update({f'{day}.{now_month}': dsc})
        return cal

    # Поллучаем строку для вывода расписания на неделю
    def get_sch_week(self) -> str:
        stroka = ''
        for day, sch in self.schedule().items():
            stroka += f'<b>{day}</b>:\n{sch}\n\n'
        return stroka


def parse_sptbx():
    url = 'https://news.sportbox.ru/Vidy_sporta/Futbol/KAMAZ-Naberezhnie-CHelni-Futbol'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
        'cookie': '__Secure-3PAPISID=4V_ZGU1jfy9vD7-a/Abrzaj8a3ru3lU-QO; __Secure-3PSID=g.a000pQg_e54VWcQL6N24LuLupte8fVjbiVtr9HN-PazPDM3fdNwAkOYMdAXE0Bol3_gqKVH5BQACgYKAQwSARYSFQHGX2MikgOXsdq0FzJ4uvjp2UGaMxoVAUF8yKrJsfN9GQBXMk3iwTNxGp4j0076; __Secure-3PSIDTS=sidts-CjEBQT4rX62q-6f7quuN6m9T8rLHfi6iCqXUrZgtXTz1rwmEhppazm3ciHuZ95Hx7fzVEAA; NID=519=n5GxEnOajLZbDKJotO20NBEtNOgWWQ3TEeh1lw_0EWFUGHBaJRSlTgeOm7DLj-hAbwLXk3N6m8UbYMtDqN0P_YsOj-QBVSpokVCC3FSKX4QerEXH9cgKswaVyTitFkrYDGtuva4MWuvhT28FRsazxU6xPJyXuo8Tcna59fIJ_haSTTumDapPePd7Xq8OHjGaA2Ea8tGXfAp4zNai7zASxP-IUC-jmmqbm-uoHwgDMk7qX_-iGsjFwMngyelf_1GX76olsjoGCpKEYr0jaCKtJH91lTKfCqWkhrjjylhbKxYIzDb3btjHNTPDlFxxFPlF1bu_eAeYywhz3q4x-_P77ijbMWXI-8E_-kGGRE7grAB8wGR7LvGSLVI; __Secure-3PSIDCC=AKEyXzVMbji5dUVpMo7uiE0Z_VeJsr-Bk22lMBN5dDUQ8YG_9HO9c2KZGoLvbuEluyIcgcVTZOc'
    }

    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    table = soup.find('div', class_='col-lg-4 col-md-4 col-sm-6 col-xs-12').find('div',
                                                                                 class_='grid-padding-20-15 _Sportbox_Spb2015_Components_FutureAndLastTeamGamesBlock_FutureAndLastTeamGamesBlock')
    dates = table.find_all('div', class_='games-date-group')
    games = table.find_all('a', class_='game-row')
    stroka_dates_games = ''
    for date, game in zip(dates, games):
        stroka_dates_games += f'<b>{date.text}</b>\n'
        lst_games = game.get('title').removesuffix(' МЕЛБЕТ-Первая Лига 2024-25').replace('-', ' ').split()
        for i in lst_games:
            if '(' in i:
                stroka_dates_games += f'{lst_games[0]} {lst_games[2][1]} - {lst_games[2][3]} {lst_games[1]}\n\n'
                break
        else:
           stroka_dates_games += f'{lst_games[0]} - {lst_games[1]}\n\n'
    return stroka_dates_games
