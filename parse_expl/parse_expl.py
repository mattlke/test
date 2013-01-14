# -*- coding: utf-8 -*-

import urllib

from bs4 import BeautifulSoup

import make_html

class Obj:
    def __init__(self):
        pass

html_file = 'explorimmo_2.html'

root_url = 'http://www.explorimmo.com'

#root_url = '/usr/bin/'

print 'root_url', root_url

def write_html_file():

    url = 'http://www.explorimmo.com/immobilier-vente-bien-paris+13eme+75013-5.html?areaMin=35&sort=6'

    f = urllib.urlopen(url)

    g = open(html_file, 'wb')

    g.write(f.read())

    g.close()

def get_recherche_result(idx_page):

    url = 'http://www.explorimmo.com/immobilier-vente-bien'
    url += '-paris+13eme+75013-%d.html?areaMin=35&sort=6'%idx_page

    f = urllib.urlopen(url)

    return f.read()

#write_html_file()

def parse_annonce_in_search_page(annonce_soup):
    '''renvoie un objet avec les champs :
    short_title, surface, type, nb_rooms, full_url, price, nb_pics'''

    res = Obj()
    1
    soup = annonce_soup

    def get_sub_str(loc_soup, key, class_name):

        l = loc_soup.find_all(key, class_name)
        assert len(l) == 1

        return l[0].string
        
    def get_info_bien(bien_soup):

        res.surface = get_sub_str(bien_soup, 'li', 'm2')
        res.type = get_sub_str(bien_soup, 'li', 'type')
        res.nb_rooms = get_sub_str(bien_soup, 'li', 'tn')        

    h2_list = soup.find_all('h2')
    assert len(h2_list) == 1

    a_list = h2_list[0].find_all('a')
    assert len(a_list) == 1
    a = a_list[0]

    res.short_title = a.string
    res.href = a['href']

    res.full_url = root_url + res.href

    total_list = soup.find_all('div', 'total')
    assert len(total_list) == 1
    a_list = total_list[0].find_all('a')
    assert len(a_list) == 1

    res.price = a_list[0].string.replace(u'\xa0', ' ')

    #print [res.total]        
    res.nb_pics_str = soup.find_all('div', 'sprEI legende')[0].string
    res.nb_pics = int(res.nb_pics_str.split(' ')[0])

    #print 'nb_photos', [res.nb_photos_str]

    bien_soup_list = soup.find_all('div', 'bien')
    assert len(bien_soup_list) == 1
    get_info_bien(bien_soup_list[0])

    return res

def parse_annonce_own_page(own_url):

    res = Obj()

    f = urllib.urlopen(own_url)
    html = f.read()
    soup = BeautifulSoup(html)

    l = soup.find_all('div', id='bloc-vue-detail')
    assert len(l) == 1
    l2 = l[0].find_all('h1')
    assert len(l2) == 1

    #1 : le titre

    res.full_title = l2[0].string.replace('\n', '').strip(' ').replace('  ', '')
    res.full_title = res.full_title.replace(u'\xa0', '')

    #2 : la description

    l = soup.find_all('div', id='detailDescriptionTxt')
    assert len(l) == 1

    l2 = l[0].find_all('p')
    assert len(l2) == 1

    desc = ''

    for x in l2[0].strings:
        y = x.replace(u'\n', u'')
        desc += y

    res.description = desc

    #3 : les liens vers les photos

    l = soup.find_all('div', id='detailSlideLinks')
    assert len(l) == 1
    l2 = l[0].find_all('img')

    res.image_src_list = [x['src'] for x in l2]

    #print 'img_src_list', res.image_src_list

    return res

def parse_annonce_full(annonce_soup):

    res = parse_annonce_in_search_page(annonce_soup)

    detailed_res = parse_annonce_own_page(res.full_url)

    res.full_title = detailed_res.full_title
    res.description = detailed_res.description

    return res

def parse_html_search_result(html):

    soup = BeautifulSoup(html)
    annonce_list = soup.find_all('div', class_='bloc-vue-in')

    res = []    

    for annonce in annonce_list:
        res_an = parse_annonce_full(annonce)

        res.append(res_an)

        #titre_annonce = '<a href="%s">%s</a>'%(res_an.full_url, res_an.full_title)
        #line = [titre_annonce, res_an.surface, res_an.price, res_an.description]

    return res

if __name__ == '__main__':
    parse_result_list()
