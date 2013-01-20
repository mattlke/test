
import parse_expl

import make_html

import os

cache_path = os.path.join(os.path.split(__file__)[0], 'cache')

if not os.path.exists(cache_path):
    raise Exception('pb !!')

class UrlBuilder:

    def __init__(self):

        self.on_sale = True
        self.for_renting = False
        self.area_min = 35
        self.location = 'paris+13eme+75013'

    def build_url(self, idx_page):
        url = 'http://www.explorimmo.com/immobilier-vente-bien'
        url += '-paris+13eme+75013-%d.html?areaMin=35&sort=6'%idx_page

        return url

class ExplSearch:

    def __init__(self):
        self.url_builder = UrlBuilder()

        self.url = self.url_builder.build_url(1)

    def produce_html(self):

        self.annonce_list = parse_expl.parse_html_search_result(open('explorimmo_2.html').read())

        html = make_html.make_result_list_html(self.annonce_list)
        print 'html', html


def main():

    annonce_list = parse_expl.parse_html_search_result(open('explorimmo_2.html').read())
    print 'data parsed, generating'
    html = make_html.make_result_list_html(annonce_list)
    f = open('res.html', 'wb')
    f.write(html)
    f.close()

if __name__ == '__main__':

    
    main()