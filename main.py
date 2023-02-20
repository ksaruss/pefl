from bs4 import BeautifulSoup
import requests
import sys
import time
import dataBase
import pandas as pd


arrows = {'system/img/g/a0n.png': 'П+'
          }




http = 'http://pefl.ru/auth.php?m=login&a=check'
data = {'rusername': 'saurus',
        'rpassword': '100100IN'}
hed = {'PHPSESSID': '39966ca078ebc82eb7a5ae29c172dc53',
       'rfl': 'amVmOl86NDY4MjI6XzpkNGU3NWNhYTY5MjI3NDBjZjgwYmQwODk3YTNiN2FmZQ',
       'last_visit': '1640247393633::1640265393633',
       'user-id_1.0.5_lr_lruid': 'pQ8AACxXvmG%2BXMMQASvRE',
       't1_sid_480437': 's1.854621349.1640260838119.1640265419203.14.288.2388'}
session = requests.Session()


def get_page(href):
    href = 'http://pefl.ru/' + href
    html = session.post(href)
    html.encoding = 'windows-1251'
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


def authorization():
    session.cookies.update(hed)
    soup = get_page('plug.php?p=tr&t=free&s=a&n=1&z=bc4c14bdc0053a64f64b1101b542ca51')
    if soup.text.find('saurus') == -1:
        print('Не удалось авторизироваться')
        sys.exit()
    print('Авторизация прошла успешно')


def get_list_links_free_players():
    list_page_players = []
    x = True
    href = 'plug.php?p=tr&t=nlist&s=w2&n=1&z=f6f76d8b6836a93cae6b26c47fc773aa'

    while x:
        time.sleep(0.2)
        soup = get_page(href)
        for j in soup.find_all('td', align="right")[1:]:
            if j.text != '':
                list_page_players.append(href)
                href = j.find('a').get('href')
            else:
                list_page_players.append(href)
                x = False
    return list_page_players


def chcxj(list_page_players):
    list_link_players = []

    for page in list_page_players:
        soup = get_page(page)

        for j in soup.find_all('tr', align="left")[1:]:
            # print(i.find('a').get('href'))
            list_link_players.append(j.find('a').get('href'))
    # print(list_link_players)
    return list_link_players


def parsing_players(list_players, write=False):
    time.sleep(0.2)
    for url in list_players:
        try:
            soup = get_page(url)
            player_char = {}
            list_position = []
            list_skills = []
            list_stats = []

            # Блок для записи в таблицу Player (имя, возраст)
            player_char['id'] = href.split('j=')[1].split('&z=')[0]
            player_char['name'] = soup.find('font', face='verdana').text
            player_id = player_char['id']
            n = soup.find(True, id='maininfo').findAll('td')
            player_char['age'] = int(n[1].text.split(' ')[0])


            # if write:
            #     dataBase.add_in_database(dataBase.Player, player_char)

            # Блок для записи в таблицу Position
            if len(n[3].text.split(' ')) == 2:
                for i in list(n[3].text.split(' ')[0]):
                    position = {}
                    position['id_player'] = player_id
                    position['position'] = i
                    list_position.append(position)
                for i in list(n[3].text.split(' ')[1].split('/')):
                    position = {}
                    position['id_player'] = player_id
                    position['position'] = i
                    list_position.append(position)
            else:
                position = {}
                position['id_player'] = player_id
                position['position'] = n[3].text
                list_position.append(position)

            for number, i in enumerate(soup.findAll('tr', class_='back2')):
                f = i.findAll('td')

                # Блок для записи скиллов
                if number < 9:
                    skills = {}
                    skills['id_player'] = player_id
                    skills['skill'] = f[0].text.lower()
                    skills['value'] = int(f[1].text.split(' ')[0])
                    try:
                        skills['arrow'] = f[1].find(class_='arrow').find('img').get('src')
                    except:
                        skills['arrow'] = ['None']
                    list_skills.append(skills)
                    skills = {}
                    skills['id_player'] = player_id
                    skills['skill'] = f[2].text.lower()
                    skills['value'] = int(f[3].text.split(' ')[0])
                    try:
                        skills['arrow'] = f[3].find(class_='arrow').find('img').get('src')
                    except:
                        skills['arrow'] = ['None']
                    list_skills.append(skills)
                if number == 10:
                    pass

                # Блок для записи статистики
                if number > 10:
                    stats = {}
                    stats['id_player'] = player_id
                    stats['tournament'] = f[0].text.lower()
                    stats['games'] = int(f[1].text)
                    stats['goals'] = int(f[2].text)
                    stats['passing'] = int(f[3].text)
                    stats['rating'] = float(f[5].text.replace(',', '.'))
                    list_stats.append(stats)

            if write == False:
                print(player_char)
                print(list_position)
                print(list_skills)
                print(list_stats)
            else:
                dataBase.add_in_database(dataBase.Player, player_char)
                dataBase.add_in_database(dataBase.Position, list_position)
                dataBase.add_in_database(dataBase.Skills, list_skills)
                dataBase.add_in_database(dataBase.Statistics, list_stats)
        except:
            pass


authorization()
# listpl = get_list_links_free_players()
# f = chcxj(listpl)

# parsing_players(['plug.php?p=refl&t=p&j=69815&z=aed8cf6b49414783f60cb7694c28b254'], write=False)

#
# s = dataBase.Player.select(dataBase.Player.name,
#                            dataBase.Player.age,
#                            dataBase.Position.position,
#                            dataBase.Skills.skill,
#                            dataBase.Skills.value) \
#     .join(dataBase.Skills, on=(dataBase.Skills.id_player == dataBase.Player.id)) \
#     .join(dataBase.Position, on=(dataBase.Position.id_player == dataBase.Skills.id_player)) \
#     .where((dataBase.Position.position.in_(['GK', 'DF', 'MF', 'FW', 'AM']))) \
#
# d = pd.DataFrame(list(s.dicts()))
#
# piv = d.pivot_table(index=['name', 'age', 'position'],
#                      columns='skill',
#                      values='value',
#                      aggfunc='mean')
#
# piv.to_excel('excel1.xlsx')

href = 'http://pefl.ru/plug.php?p=refl&t=p&j=69815&z=aed8cf6b49414783f60cb7694c28b254'

params = {'n': 'p',
          'j': 69815,
          't': 'pstat',
          'r': 15715,
          'z': '217d5f5148c09688e695ad1b1936d29b'}

# html = session.get(url=href)
# html.encoding = 'windows-1251'
# print(html.text)

# f = get_page('plug.php?p=refl&t=p&j=69815&z=aed8cf6b49414783f60cb7694c28b254')
# print(str(f.find('td', id='td6')['onmousedown']).split('&'))
parsing_players(['plug.php?p=refl&t=p&j=69815&z=aed8cf6b49414783f60cb7694c28b254'])

