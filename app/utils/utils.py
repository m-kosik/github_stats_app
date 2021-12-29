
import re
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request, json


def get_all_data(username):
    repos = requests.get('https://github.com/' + username + '?tab=repositories') 
    if not repos.ok:
        raise NoUserError
    soup = BeautifulSoup(repos.content,'html5lib')
    repository_list, number_of_stars, total_stars = find_repositories_and_stars(soup)
    language_dict = list_languages(repository_list)
    return number_of_stars, total_stars, language_dict


def find_repositories_and_stars(soup):
    repository_list = []
    number_of_stars = {}

    for repo in soup.find_all(class_='wb-break-all'):
        repository_list.append(repo.find('a')['href'])
        repo_name = repo.find('a').text.strip(' \n')
        number_of_stars[repo_name] = 0

    total_stars = 0
    for element in soup.find_all('svg', {'aria-label': 'star'}):
        repo_name = element.parent['href'].split('/')[-2]
        stars = int(element.parent.text.strip('\n '))
        number_of_stars[repo_name] = stars
        total_stars += stars

    for k,v in number_of_stars.items():
        print(f'{k} : {v}')

    return repository_list, number_of_stars, total_stars


def list_languages(repository_list):  

    is_limit = False
    total_language_use_in_bytes = {}

    for repo in repository_list:
        try:
            with urllib.request.urlopen('https://api.github.com/repos' + repo) as url:
                data = json.loads(url.read().decode())
                repo_size = float(data['size'])
        except urllib.error.HTTPError as exception:
            is_limit = True
            repo_size = 0
            print(exception)
            print('Languages found in all repositories will be printed alphabetically.')

        temp_repo = requests.get('https://github.com/' + repo) 
        soup = BeautifulSoup(temp_repo.content,'html5lib')
        try:
            languages_in_percent = find_used_languages_by_percent(soup)
        except AttributeError:
            print('There are no languages specified for repository ' + repo)

        languages_in_bytes = {k: v*repo_size for k, v in languages_in_percent.items()}

        for language, size in languages_in_bytes.items():
            try:
                total_language_use_in_bytes[language] += size
            except KeyError:
                total_language_use_in_bytes[language] = size
    
    if is_limit:
        return total_language_use_in_bytes
    else:
        return total_language_use_in_bytes
    

def find_used_languages_by_percent(soup):
    languages_dict = {}

    header = soup.find(lambda elm: elm.name == "h2" and "Languages" in elm.text)
    child = header.find_next_siblings()[0].find('span')
    for element in child.find_all('span'):
        language = element['aria-label'].rsplit(' ', 1)[0]
        percent_usage = float(element['aria-label'].rsplit(' ', 1)[1])
        languages_dict[language] = percent_usage
    return languages_dict


class NoUserError(Exception):
    pass