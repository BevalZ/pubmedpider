# import packages
import requests,sys,os,re,time
import urllib.request as req
from bs4 import BeautifulSoup as bs

def getdomain():
    # Check the available domain
    ## get the web page source
    yovisun = 'http://tool.yovisun.com/scihub/'
    res = requests.get(yovisun)
    res.encoding = res.apparent_encoding
    soup = bs(res.text,"html.parser")

    ## find the content we need
    link_tag = soup.find_all(class_ = 'domain')
    domain = []
    for item in link_tag:
    	domain.append(item.find('a').text[7:])

    domain_str=[]
    for i in domain:
        link='https://'+str(i)+'/'
        domain_str.append(link)

    return domain_str    

# generate download link
def link(doi,dom):
    url = str(dom)+str(doi)
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    tag = soup.find_all('iframe')
    if tag != []:
        src = tag[0].get('src')
        pdf_url = src.replace('#view=FitH','')
        if pdf_url.find('https:') != -1:
            pdf_url = pdf_url
        else:
            pdf_url = 'https:' + pdf_url
        return pdf_url

    else:
        url_base = 'https://cn.bing.com/academic?q='
        doi_encode = req.pathname2url(doi)
        url_full = url_base + doi_encode
        notify = 'Download link not available but you may check this :) \n'+str(url_full)
        return notify

