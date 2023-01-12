from bs4 import BeautifulSoup, Tag, SoupStrainer
import requests

def get_def(word):

    URL = f'https://dictionary.cambridge.org/dictionary/english/{word}'

    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'}
    page = requests.get(URL, headers=headers, allow_redirects=True)

    if page.url == 'https://dictionary.cambridge.org/dictionary/english/':
        return 'invalid word' 

    soup = BeautifulSoup(page.content, "lxml")

    if not soup.find(class_='pr dictionary'):
        return 'invalid word'


    my_str = ""

    if soup.find(class_='entry-body__el'):
        entry_bodies = soup.find(class_='pr dictionary').find_all('div', class_='entry-body__el') #to get individual'parts of speech' blocks (contains phrase-blocks as well)
        
        for entry_body in entry_bodies:
            my_str += f"🥊 <b>{entry_body.find(class_='headword').text.upper()}</b>"
            if entry_body.find('div', class_='posgram'):
                my_str += f" <i>({entry_body.find('div', class_='posgram').text})</i>\n"
            elif entry_body.find('span', class_='pos dpos'):
                my_str += f" <i>({entry_body.find('span', class_='pos dpos').text})</i>\n"
            else:
                my_str += '\n'
            for sense_body in entry_body.find_all('div', class_='sense-body'):
                for definition in sense_body.children: # one sense-body can have both phrase as well as regular definition
                    if isinstance(definition, Tag): 
                        if definition.has_attr('class') and 'phrase-block' in definition['class']:
                            phrase_title = definition.find(class_='phrase-title').text.strip(' ')
                            phrase_definition = definition.find(class_='def').text.strip(' ').capitalize()
                            my_str +=  f'🔶 <b>({phrase_title}) {phrase_definition}</b>\n'
                            if definition.find(class_='examp'):
                                my_str += f">>> <i>{definition.find(class_= 'examp').text}</i>\n"
                        elif definition.has_attr('class') and 'def-block' in definition['class']:
                            my_str += '🔶 <b>' + definition.find(class_='def').text.strip(' ').capitalize() + '</b>\n'
                            if definition.find(class_='examp'):
                                my_str += f">>> <i>{definition.find(class_= 'examp').text}</i>\n"
            my_str += '\n'

    if soup.find(class_='idiom-block'): # check for idioms and phrases as they don't have 'entry-body__el' class
        idiom_block = soup.find(class_='idiom-block')
        my_str += f"🥊 <b>{idiom_block.find(class_='headword').text.upper()}</b>"
        my_str += f" <i>({idiom_block.find('span', class_='pos dpos').text})</i>\n"
        for def_block in idiom_block.find_all(class_='def-block'):
            my_str += '🔶 <b>' + def_block.find(class_='def').text.strip(' ').capitalize() + '</b>\n'
            if def_block.find(class_='examp'):
                my_str += f">>> <i>{def_block.find(class_= 'examp').text}</i>\n"
    return my_str
