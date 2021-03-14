import requests
from bs4 import BeautifulSoup
from datetime import datetime

class OfficeNotFoundError(Exception):
    pass

def _get_office_id(office_city):
    first_city = second_city = ''
    page = requests.get('https://www.spc.noaa.gov/misc/NWS_WFO_ID.txt').text
    page = page.split('=')
    while("" in page):
        page.remove("")
    page = page[1].splitlines()
    for office in page:
        city = office.split(',')[0].lower()
        if '/' in city:
            first_city = city.split('/')[0]
            second_city = city.split('/')[1]
        if (city == office_city or 
            first_city == office_city or second_city == office_city):
            return office.split('\t')[-1].upper()

    raise OfficeNotFoundError

def _generate_url(office_city):
    return 'https://forecast.weather.gov/product.php?site={}&issuedby={}&product=AFD&glossary=0'.format(office_city, office_city)

def _get_page_text(office_city):
    office_id = _get_office_id(office_city)
    page = requests.get(_generate_url(office_id))
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup.find(class_='glossaryProduct').text

def _get_timestamp(text):
    #Sample 900 PM PST Tue Nov 24 2020
    dt = text.split('\n\n')[1].splitlines()[2]
    try: 
        # Get just the hour from the string
        hour = dt.split(' ')[0].strip('0')
        dt = ' '.join([hour] + dt.split(' ')[1:])
        dt_obj = datetime.strptime(dt, "%H %p %Z %a %b %d %Y")
        return dt_obj.strftime("%A, %B %d, %H %p")
    except:
        return dt

def _get_section(text, delim):
    section = 'Last updated: ' + _get_timestamp(text) + '.\n'

    body = text.split('.'+delim)[1].split('\n\n')[0]
    timeframe = body.split('...')[0]
    if (timeframe.find('/') == 1):
        timeframe = timeframe.strip().strip('/') + ': '
    body = body.split('...')[1]
    section += timeframe + body

    return section

def get_short_term_discussion(office_city):
    text = _get_page_text(office_city)

    return _get_section(text, 'SHORT TERM')

def get_long_term_discussion(office_city):
    text = _get_page_text(office_city)

    return _get_section(text, 'LONG TERM')

def get_synopsis(office_city):
    text = _get_page_text(office_city)

    return _get_section(text, 'SYNOPSIS')

def get_forecast_update(office_city):
    text = _get_page_text(office_city)

    return _get_section(text, 'UPDATE')

def get_forecast_discussion(office_city):
    text = _get_page_text(office_city)
    discussion = ''

    stripped_text = text.split('.AVIATION')[0].replace('&&\n\n', '')
    sections = stripped_text.split('\n\n')[2:-1]
    for section in sections:
        split_text = section.split('...')
        section_name = split_text[0].strip('.')
        section_content = "".join(split_text[1:])
        discussion += section_name + '. ' + section_content + '\n\n'

    return discussion
