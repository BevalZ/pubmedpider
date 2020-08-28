#! /usr/bin/env python
#-*- coding:utf-8 -*-

# import packages
import entrezpy.esearch.esearcher
import requests,sys,os,re,time
from bs4 import BeautifulSoup as bs
## Self defined
# noinspection PyUnresolvedReferences
import IF_request
# noinspection PyUnresolvedReferences
import Paper_download as ppdn


# get pmid list

def inquire(term):
        
    es = entrezpy.esearch.esearcher.Esearcher('esearcher', '987622272@qq.com')
    pmid_inquire = es.inquire({'db':'pubmed','term':term,'retmax': 10000})
    pmid_num = pmid_inquire.get_result().count
    pmid = pmid_inquire.get_result().uids
    pmid.insert(0,str(pmid_num))
    return pmid

# get paper info
class paperinfo():
    
    def __init__(self,pmid):
        url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?email=iuxjo%40hi2.in&tool=entrezpyConduit&db=pubmed&retmode=xml&id='
        self.pmid = pmid
        res = requests.get(url_base+str(pmid))
        self.soup = bs(res.text,'xml')
    
    def pubtype(self):
        if self.soup.find('PublicationType') == None:
            return ''
        else:
            pubtypesoup = self.soup.find_all('PublicationType')
            pubtype = []
            for i in pubtypesoup:
                pubtype.append(i.text)
            if self.soup.find('BookDocument') != None:
                pubtype.insert(0,'Book')
            return pubtype

    def author(self):
        if self.soup.find('AuthorList') == None:
            return ''
        else:
            author_firstname = self.soup.find_all('ForeName')
            author_lastname = self.soup.find_all('LastName')
            author = []
            for i in range(0,len(author_firstname)):
                author.append(author_firstname[i].text+' '+ author_lastname[i].text)
            return author
    
    def journal(self):
        if self.soup.find('Title') == None:
            return ''
        else:
            title = self.soup.find('Title')
            journal = title.text
            if journal.find('(') != None:
                num = journal.find('(')
                journal = journal[:num-1]
            return journal

    def journal_short(self):
        if self.soup.find('ISOAbbreviation') == None:
            return ''
        else:
            title_short = self.soup.find('ISOAbbreviation')
            return title_short.text

    def publisher(self):
        if self.soup.find('PublisherName') == None:
            return ''
        else:
            publisher = self.soup.find('PublisherName')
            return publisher.text

    def title(self):
        if self.soup.find('ArticleTitle') == None:
            return ''
        else:
            author = self.soup.find('ArticleTitle')
            return author.text

    def abstract(self):
        if self.soup.find('AbstractText') == None:
            return ''
        else:
            abstract = self.soup.find('AbstractText')
            return abstract.text

    def pubdate(self):
        if self.soup.find('PubDate') == None:
            return ''
        else:
            pubsoup = list(self.soup.find('PubDate').children)
            pubdate = pubsoup[1].text
            return pubdate

    def keywords(self):
        if self.soup.find('KeywordList') == None:
            return ''
        else:
            keysoup = list(self.soup.find('KeywordList').children)
            length = len(keysoup) // 2
            keywords = []
            for i in range(1, length+1):
                keywords.append(keysoup[i*2-1].text)    
            return keywords

    def doi(self):
        if self.soup.find(name='ArticleId',attrs={'IdType':'doi'}) == None:
            return ''
        else:
            doisoup = self.soup.find(name='ArticleId',attrs={'IdType':'doi'})
            return doisoup.text

    def pii(self):
        if self.soup.find(name='ArticleId',attrs={'IdType':'pii'})  == None:
            return ''
        else:
            piisoup = self.soup.find(name='ArticleId',attrs={'IdType':'pii'}) 
            return piisoup.text

    def pmc(self):
        if self.soup.find(name='ArticleId',attrs={'IdType':'pmc'}) == None:
            return ''
        else:
            pmcsoup = self.soup.find(name='ArticleId',attrs={'IdType':'pmc'})
            return pmcsoup.text
    
    def references(self):
        if self.soup.find(name='Reference') == None:
            return ''
        else:
            referencessoup = self.soup.find_all(name='Reference')
            refnum = len(referencessoup)
            references = 'We found ' + str(refnum) + ' citations of this paper as follow:'
            for i in range(0, refnum):
                subsoup = referencessoup[i].contents
                ref = 'Citation = ' + subsoup[1].text.strip('\n')+' ; PMID = '+subsoup[3].text.strip('\n')+';'
                references = references + ref
            return references

