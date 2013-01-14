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

def parse_annonce_in_recherche(soup):

    res = Obj()

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
    res.nb_photos_str = soup.find_all('div', 'sprEI legende')[0].string
    res.nb_photos = int(res.nb_photos_str.split(' ')[0])

    print 'nb_photos', [res.nb_photos_str]

    bien_soup_list = soup.find_all('div', 'bien')
    assert len(bien_soup_list) == 1
    get_info_bien(bien_soup_list[0])

    return res

def parse_annonce_page(full_url):

    res = Obj()

    #full_url = os.path.join(root_url, sub_url)   

    #print 'full_url', full_url    

    f = urllib.urlopen(full_url)    

    #html = open('explorimmo_annonce.html', 'rb').read()
    html = f.read()

    soup = BeautifulSoup(html)

    l = soup.find_all('div', id='bloc-vue-detail')
    assert len(l) == 1
    l2 = l[0].find_all('h1')
    assert len(l2) == 1

    res.full_title = l2[0].string.replace('\n', '').strip(' ').replace('  ', '')
    res.full_title = res.full_title.replace(u'\xa0', '')
    
    #print 'full title', res.full_title.encode('utf-8'), [res.full_title]

    #maintenant la description

    l = soup.find_all('div', id='detailDescriptionTxt')
    assert len(l) == 1

    l2 = l[0].find_all('p')
    assert len(l2) == 1

    #print l2[0].prettify()

    desc = ''

    for x in l2[0].strings:
        y = x.replace(u'\n', u'')
        desc += y

    res.description = desc

    #les liens vers les photos
    l = soup.find_all('div', id='detailSlideLinks')
    assert len(l) == 1
    l2 = l[0].find_all('img')

    res.image_src_list = [x['src'] for x in l2]

    #print res.image_src_list

    #print res.description.encode('utf-8')

    return res

def parse_annonce_full(annonce):

    res = parse_annonce_in_recherche(annonce)

    detailed_res = parse_annonce_page(res.full_url)

    res.full_title = detailed_res.full_title
    res.description = detailed_res.description

    return res

def parse_result_list():

    html = open(html_file, 'rb').read()

    #html = get_recherche_result(2)

    soup = BeautifulSoup(html)
    annonce_list = soup.find_all('div', class_='bloc-vue-in')

    print len(annonce_list)

    annonce = annonce_list[0]

    #print [annonce.prettify()]

    title = ['titre', 'surface', 'prix', 'description']
    table = []

    #annonce_list = annonce_list[:2]

    for annonce in annonce_list:
        res_an = parse_annonce_full(annonce)

        #print res_an.full_title.encode('utf-8'), res_an.price.encode('utf-8')
        #print res_an.description.encode('utf-8')

        titre_annonce = '<a href="%s">%s</a>'%(res_an.full_url, res_an.full_title)

        line = [titre_annonce, res_an.surface, res_an.price, res_an.description]
        table.append(line)

    #print [soup.prettify()]

    html = make_html.make_table(title, table)
    f = open('result.html', 'wb')
    f.write(html.encode('utf-8'))
    f.close()

parse_result_list()

#write_html_file()

#parse_annonce_page()

#print y

#print u'\u2026'.decode('utf-8', 'replace')
