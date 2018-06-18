#!/bin/python3
from urllib.request import urlopen,Request,urlretrieve
from bs4 import BeautifulSoup as BS
import sys
import argparse

def get_web_page(url):
    req=Request(url,headers=headers)
    try:
        html=urlopen(req).read()
    except:
        print("There was an Error!")
        sys.exit(1)
    return html

def main(url,ssl):
    print("Scraping {}".format(url))
    web_page=get_web_page(url)
    
    soup=BS(web_page,"html.parser")
    links=soup.find_all("img")

    img_links=[i.get('src') for i in links]
    if (ssl):
        proto="https"
    else:
        proto="http"
    img_links=[proto +":"+ i for i in img_links if i[:2]=='//']
    n=len(img_links)
    print("Found {} images".format(n))
    count=1
    for i in img_links:
        #print(i)
        sys.stdout.write('\r')
        sys.stdout.write("Retrieving..." + str(count) + "/" + str(n) )
        sys.stdout.flush()
        try:
            urlretrieve(i,i[i.rfind('/')+1:])
        except:
            pass
        count+=1
    print("\nDone!")

if __name__ == '__main__':
    headers={"User-Agent": "Mozilla/5.0"}
    parser = argparse.ArgumentParser(description="Scrape images of web pages")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-u','--url',help="URL of the webpage",required=True)
    optional.add_argument('-s','--ssl',action="store_true",default=False,help="Use this option to fetch images over https")
    args=parser.parse_args()
    main(args.url,args.ssl)