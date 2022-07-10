import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sqlite import Database


def get_html(url):
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    r = requests.get(url=url, headers=user_agent)
    if r.ok:
        return r.text
    else:
        return r.status_code


def parse_cbr(html):
    soup = BeautifulSoup(html, 'lxml')
    values = soup.find_all(class_='main-indicator_value')
    value = values[-1].text

    dollar = soup.find(class_='main-indicator_rate').find_all(class_='col-md-2')
    dollar = dollar[-1].text
    return value, dollar


def parse_hhru(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.find(class_='bloko-subheader').text
    text = text.strip().replace('Найдено ', '').replace('Найдена ', "") \
        .replace(' вакансии', '').replace('вакансий', '').replace('вакансия', '').replace('&nbsp;', '')
    text = text.replace('\xa0', '')
    return text


def parse_hhru_buers(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.find_all(class_='bloko-header-1')
    text = text[1].text
    text = text.strip().replace('«Менеджер по закупкам»', '') \
        .replace('вакансия', "").replace('вакансии', "").replace('вакансий', "")
    text = text.replace('\xa0', '').strip()
    return text


def parse_9999(html):
    soup = BeautifulSoup(html, 'lxml')
    wraper = soup.find(class_='bottom-wrapper-inner')
    elems = soup.find_all(class_='price_val')
    prices = []
    for elem in elems:
        prices.append(elem.text.strip())
    return prices


def benzin():
    pass


def parse_gold_coin():
    pass


def parse_gold_exchange():
    pass


def job_hhru():
    pass


def hhru():
    hh_link = 'https://hh.ru/vacancies/menedzher_po_prodazham'
    html = get_html(hh_link)
    sales = int(parse_hhru(html))

    hh_link = 'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=%D0%9C%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80+%D0%BF%D0%BE+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B0%D0%BC&from=suggest_post'
    html = get_html(hh_link)
    buers = int(parse_hhru_buers(html))
    mess = []
    print('Менеджер по закупкам {0:.0f}'.format(buers))
    print('Менеджер по продажам {0:.0f}'.format(sales))
    print('Коэф перекупленности {0:.2f}'.format(float(sales) / float(buers)))

    mess.append('Менеджер по закупкам {0:.0f}'.format(buers))
    mess.append('Менеджер по продажам {0:.0f}'.format(sales))
    mess.append('Коэф перекупленности {0:.2f}'.format(float(sales) / float(buers)))

    text = '\n'.join(mess)
    return text


def cbr():
    html = get_html('https://www.cbr.ru/')
    rate, dollar = parse_cbr(html)
    text = f'Ключевая ставка {rate}\n' \
           f'Курс доллара {dollar}'

    return text


def gold9999():
    url = 'https://9999d.ru/product/element/georgiy_pobedonosets_zoloto_mmd_2018_2019/'
    html = get_html_ph(url)
    result = parse_9999(html)
    prices = []
    for elem in result:
        prices.append(
            elem.strip().replace(' ₽', '').replace("Продаем: ", "").replace("Покупаем: ", "").replace(' ', ''))

    if len(prices) != 1:
        spred = (float(prices[0]) / (float(prices[1])) - 1) * 100
        spred = '{0:.2f}'.format(spred)
    else:
        spred = ''
    text = f'\n9999 Держава Золото {",".join(result)} \nСпред = {spred}%'
    date_time =datetime.datetime.now()
    db.add_history(dealer='9999 Держава Золото', datetime=str(date_time), buy=float(prices[0]), sell=float(prices[1]))
    return text


def parse_zolotoy_dvor(html):
    soup = BeautifulSoup(html, 'lxml')
    elems = soup.find_all(class_='textcen')
    pricies = []
    for index in elems[:2]:
        pricies.append(index.text.strip().replace("'", ''))
    spred = (float(pricies[0]) / (float(pricies[1])) - 1) * 100
    spred = '{0:.2f}'.format(spred)
    return pricies, spred


def zolotoy_dvor():
    url = 'https://www.zolotoydvor.ru/Zolotaya-moneta-Georgiy-Pobedonosets-MMD-50-rubley-2018-2022god_10300t.html'
    try:
        html = get_html_ph(url=url)
        result, spred = parse_zolotoy_dvor(html)
        text = f'\nЗолотой двор Покупка/продажа {"/".join(result)} \nСпред = {spred}%'
        date_time =datetime.datetime.now()
        db.add_history(dealer='Золотой двор', datetime=str(date_time), buy=float(result[0]), sell=float(result[1]))
    except:
        text = f'\nЗолотой двор сайт не дотупен'

    return text


def parse_zolotoy_zapas(html):
    soup = BeautifulSoup(html, 'lxml')
    pricies = []

    buy = soup.find(class_='card__table-purchase').find('tbody').find(class_='card__cell-cost').text.strip().replace(
        ' ', '')

    sale = soup.find(class_='card__table-sale').find('tbody').find(class_='card__cell-cost').text.strip().replace(' ',

                                                                                                                  '')
    pricies.append(buy)
    pricies.append(sale)
    if len(buy) > 1 and len(sale) > 1:
        spred = (float(buy) / (float(sale)) - 1) * 100
        spred = '{0:.2f}'.format(spred)
    else:
        spred = '0'
    return pricies, spred


def zolotoy_zapas():
    url = 'https://www.zolotoy-zapas.ru/coins-price/georgiy-pobedonosets-gold-coin-quarter-oz/'
    try:
        html = get_html_ph(url=url)

        result, spred = parse_zolotoy_zapas(html)
        text = f'\nЗолотой Запас Покупка/продажа {"/".join(result)} \nСпред = {spred}%'
        date_time =datetime.datetime.now()
        db.add_history(dealer='Золотой запас', datetime=str(date_time), buy=float(result[0]), sell=float(result[1]))

    except:
        text = f'\nЗолотой Запас Сайт не доступен'

    return text


def parse_zoloto_md(html):
    soup = BeautifulSoup(html, 'lxml')
    pricies = []

    buy = soup.find(class_='product_price').find('span').text.strip().replace('Руб.', '').replace(' ', '')

    sale = soup.find(class_='js-price-buyout').text.strip().replace('Руб.', '').replace(' ', '')
    pricies.append(buy)
    pricies.append(sale)
    if len(buy) > 1 and len(sale) > 1:
        spred = (float(buy) / (float(sale)) - 1) * 100
        spred = '{0:.2f}'.format(spred)
    else:
        spred = '0'
    return pricies, spred


def zoloto_md():
    url = 'https://zoloto-md.ru/bullion-coins/i-rossiya-i-sssr/zolotaya-investiczionnaya-moneta-georgij-pobedonosecz-2018-2021g.v.-mmd,-7,78-g-chistogo-zolota-proba-0,999'
    try:
        html = get_html_ph(url=url)
        result, spred = parse_zoloto_md(html)
        text = f'\nЗолотой монетный двор Покупка/продажа {"/".join(result)} \nСпред = {spred}%'
        date_time =datetime.datetime.now()
        db.add_history(dealer='Золотой монетный двор', datetime=str(date_time), buy=float(result[0]), sell=float(result[1]))
    except:
        text = f'\nЗолотой монетный двор - Сайт недоступен'

    return text


def parse_vtbbank(html):
    soup = BeautifulSoup(html, 'lxml')
    pricies = []

    elems = soup.find_all(class_='coin-price__item')
    for elem in elems[2:4]:
        # print(elem.text.strip().replace('Покупка:', '').replace('Продажа:', '').replace(' ₽', ''). replace(' ', '').strip())
        pricies.append(elem.text.strip().replace('Покупка:', '').replace('Продажа:', '').replace(' ₽', '').replace(' ',

                                                                                                                   '').strip())
    if len(pricies[0]) > 1 and len(pricies[1]) > 1:

        spred = (float(pricies[0]) / (float(pricies[1])) - 1) * 100
        spred = '{0:.2f}'.format(spred)
    else:
        spred = '0'
    return pricies, spred


def vtbbank():
    url = 'https://www.vfbank.ru/fizicheskim-licam/monety/'
    try:
        html = get_html_ph(url=url)
        result, spred = parse_vtbbank(html)
        text = f'\nВТБ банк Покупка/продажа {"/".join(result)} \nСпред = {spred}%'
        date_time =datetime.datetime.now()
        db.add_history(dealer='ВТБ Банк', datetime=str(date_time), buy=float(result[0]), sell=float(result[1]))
    except:
        text = f'\nВТБ банк - сайт недоступен'
    return text


def get_html_ph(url):
    # options = Options()
    # options.add_argument('--headless')
    browser = webdriver.Remote("http://localhost:4444/wd/hub", desired_capabilities={"browserName": "chrome"})
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.get(url)
    browser.implicitly_wait(10)
    # time.sleep(3)
    html = browser.page_source
    browser.quit()
    return html


def sber():
    url = 'https://www.sberbank.ru/ru/person/investments/values/mon#/coin/5216-0060?condition=1'
    html = get_html_ph(url=url)
    result, spred = parse_sber(html)
    text = f'\nВТБ банк Покупка/продажа {"/".join(result)} \nСпред = {spred}%'
    return text


def parse_sber(html):
    soup = BeautifulSoup(html, 'lxml')
    pricies = []

    elems = soup.find_all(class_='cc-coin-form__prices-price-price-block')
    for elem in elems[0]:
        text = elem.text
        # print(elem.text.strip().replace('Покупка:', '').replace('Продажа:', '').replace(' ₽', ''). replace(' ', '').strip())
        pricies.append(elem.text.strip().replace('Покупка:', '').replace('Продажа:', '').replace(' ₽', '').replace(' ',

                                                                                                                   '').strip())
    spred = None
    return pricies[0], spred


def main():
    # time.sleep(30)
    for i in range(1, 15):
        try:
            r = requests.get('http://localhost:4444/wd/hub')
        except:
            time.sleep(5)
    data = []
    data.append(gold9999())
    data.append(zolotoy_zapas())
    data.append(zolotoy_dvor())
    data.append((zoloto_md()))
    data.append(vtbbank())
    import logging
    # logging.info('\n'.join(data))
    # print('\n'.join(data))
    # time.sleep(5)


if __name__ == '__main__':
    db = Database()
    try:
        db.create_table()
    except Exception as e:
        print(e)
    main()
