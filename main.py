#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Import packages

## General packages
# noinspection PyUnresolvedReferences
import requests, re, urllib, sys, datetime, wget
import pyperclip
from time import sleep
## UI Related
# noinspection PyUnresolvedReferences
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QFile
# noinspection PyUnresolvedReferences
from PySide2.QtGui import QIcon

## Self defined
import IF_request
import Paper_download as ppdn
import query

# global var

domain = ''


# Load the UI


# Windows class
class Stats:
    def __init__(self):
        # default settings
        qfile = QFile('UI/pubmed_spider.ui')
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # local vars
        self.IF_list = 'Full Name of Journal,IF\n'
        self.Paper_list = 'Author,Year,Title,Journal,Abstract,Citations,keywords,Pubtype,PMID,DOI,IF,Download link\n'
        self.ifpv = 0

        # connetcions
        self.ui = QUiLoader().load(qfile)
        ## Journal IF Query tag
        self.ui.if_check_process.setValue(self.ifpv)
        self.ui.check_if.clicked.connect(self.if_check)
        self.ui.check_if2.clicked.connect(self.if_check2)
        self.ui.if_clean.clicked.connect(self.if_clean)
        self.ui.if_save.clicked.connect(self.if_save)
        self.ui.if_batch.clicked.connect(self.if_batch)

        # Scihub downloader tag
        self.download_link = ''
        self.ui.link_process.setValue(self.ifpv)
        self.ui.transfer.clicked.connect(self.pmid2doi)
        self.ui.hosts.addItems(ppdn.getdomain())
        self.ui.hosts.currentIndexChanged.connect(self.handleSelectionChange)
        self.ui.single.clicked.connect(self.singlerun)
        self.ui.download.clicked.connect(self.download)
        self.ui.scihub_batch.clicked.connect(self.scihub_batch)
        self.ui.download_clean.clicked.connect(self.download_clean)

        # single paper spider function
        self.ui.paper_info_query.clicked.connect(self.paper_single)
        self.ui.paper_info_clean.clicked.connect(self.paper_info_clean)
        self.ui.paper_infio_save.clicked.connect(self.paper_infio_save)

        # batch paper spider function
        self.ui.query.clicked.connect(self.query)

        # log
        self.ui.log_clean.clicked.connect(self.log_clean)
        self.ui.log_save.clicked.connect(self.log_save)
        self.ui.save_query.clicked.connect(self.save_query)

        # qrcode
        self.pix = QPixmap('qr.jpg')
        self.ui.qrcode.setPixmap(self.pix)

    # self.ui.qrcode.setScaledContents(True)

    # IF Query Functions
    # Query via journal name
    def if_check(self):
        self.ui.log_display.append(str(
            datetime.datetime.now()) + '\tStart IF querying...\n----------------------------------------------------------')
        jname = self.ui.jname_input.text().upper()
        self.IF_list += str(IF_request.main(jname)[0]) + ',' + IF_request.main(jname)[2] + '\n'
        self.ui.fjn.append(IF_request.main(jname)[0])
        self.ui.if_2.append(IF_request.main(jname)[2])
        self.ui.fjn.ensureCursorVisible()
        self.ui.if_2.ensureCursorVisible()
        self.ui.if_check_process.setValue(100)
        self.ui.log_display.append(self.IF_list + '----------------------------------------------------------\n')
        sleep(0.2)
        self.ui.if_check_process.setValue(0)

    # Query via PMID/DOI
    def if_check2(self):
        self.ui.log_display.append(str(
            datetime.datetime.now()) + '\tStart IF querying...\n----------------------------------------------------------')
        id = self.ui.id_input.text()

        if len(id) == 8:
            pmid = id
        else:
            pmid = IF_request.pmid(id)
        self.ui.if_check_process.setValue(20)

        jname = query.paperinfo(str(pmid)).journal().upper()
        # print(jname)

        self.ui.if_check_process.setValue(40)
        # print(IF_request.main(jname))
        self.IF_list += str(IF_request.main(jname)[0]) + ',' + IF_request.main(jname)[2] + '\n'
        self.ui.if_check_process.setValue(45)
        self.ui.fjn.append(IF_request.main(jname)[0])
        self.ui.if_check_process.setValue(50)
        self.ui.if_2.append(IF_request.main(jname)[2])
        self.ui.if_check_process.setValue(60)
        self.ui.fjn.ensureCursorVisible()
        self.ui.if_check_process.setValue(70)
        self.ui.if_2.ensureCursorVisible()
        self.ui.if_check_process.setValue(100)
        self.ui.log_display.append(self.IF_list + '----------------------------------------------------------\n')
        sleep(0.2)
        self.ui.if_check_process.setValue(0)

    # Batch Query
    def if_batch(self):
        QMessageBox.information(
            self.ui,
            'Notification',
            '''Before we move on,please recheck the message:\n1.Save the Journal names or PMIDs/DOIs in a .txt file and keep them in separate lines\n2.This can be a long process, quit if you have a quick temper '''
        )
        fd = QFileDialog.getOpenFileName(
            self.ui,
            "Please select the file to open",
            r"./",
            "plain text(*.txt)"
        )
        self.ui.log_display.append(str(
            datetime.datetime.now()) + '\tStart IF querying...\n----------------------------------------------------------')
        filename = str(fd[0])
        idfile = open(filename, 'r')
        idlist = idfile.readlines()
        idfile.close()
        idlen = len(idlist)
        tmp_num = 1
        for i in idlist:
            self.ui.log_display.append(str(tmp_num) + '/' + str(idlen) + '\t-----------------------------')
            if i != ''.join(i.split()):
                self.IF_list += str(IF_request.main(i)[0]) + ',' + IF_request.main(i)[2] + '\n'
                self.ui.fjn.append(IF_request.main(i)[0])
                self.ui.if_2.append(IF_request.main(i)[2])
            else:
                if len(i) == 8:
                    pmid = i
                else:
                    pmid = IF_request.pmid(i)
                    jname = query.paperinfo(str(pmid)).journal()
                if IF_request.main(jname)[2] != None:
                    self.IF_list += str(IF_request.main(jname)[0]) + ',' + IF_request.main(jname)[2] + '\n'
                    fjn = self.ui.fjn.append(IF_request.main(jname)[0])
                    if_2 = self.ui.if_2.append(IF_request.main(jname)[2])
                else:
                    self.IF_list += str(jname) + ',not avaliable\n'
                    fjn = self.ui.fjn.append(str(jname))
                    if_2 = self.ui.if_2.append('not avaliable')
            self.ui.fjn.ensureCursorVisible()
            self.ui.if_2.ensureCursorVisible()
            self.pv = int(tmp_num / idlen * 100)
            self.ui.if_check_process.setValue(self.pv)
            sleep(1)
            tmp_num += 1
            if tmp_num > idlen:
                sleep(2)
                self.ui.if_check_process.setValue(0)
        self.ui.log_display.append(self.IF_list)
        self.ui.log_display.append(str(
            datetime.datetime.now()) + '\tEnd of IF querying...\n----------------------------------------------------------')

    # Batch download link generate
    def scihub_batch(self):
        QMessageBox.information(
            self.ui,
            'Notification',
            '''Before we move on,please recheck the message:\n1.Save the Journal names or DOIs in a .txt file and keep them in separate lines\n2.This can be a long process, quit if you have a quick temper\n3.This process can only generate download links '''
        )
        fd = QFileDialog.getOpenFileName(
            self.ui,
            "Please select the file to open",
            r"./",
            "plain text(*.txt)"
        )
        self.ui.log_display.append(str(
            datetime.datetime.now()) + '\tStart download links generation...\n----------------------------------------------------------')
        filename = str(fd[0])
        doifile = open(filename, 'r')
        doilist = doifile.readlines()
        doifile.close()
        doilen = len(doilist)
        tmp_num = 1
        linklist = []
        self.ui.downloadlink.append('-------------------start recording-------------------\n')
        for i in doilist:
            self.ui.log_display.append(str(tmp_num) + '/' + str(doilen) + '\t-----------------------------\n')
            link = ppdn.link(i, self.ui.hosts.currentText())
            linklist.append(link)
            self.ui.downloadlink.append(link)
            self.ui.log_display.append('The donwload link of ' + i + link)
            self.pv = int(tmp_num / doilen * 100)
            self.ui.link_process.setValue(self.pv)
            tmp_num += 1
            if tmp_num > doilen:
                sleep(2)
                self.ui.link_process.setValue(0)
        self.ui.log_display.append('\n' + str(
            datetime.datetime.now()) + '\tEnd download links generation...\n----------------------------------------------------------')

    # Clean history
    def if_clean(self):
        self.ui.fjn.clear()
        self.ui.if_2.clear()
        self.ui.log_display.append(
            '-------------IF Query File Cleaned at ' + str(datetime.datetime.now()) + '-------------\n')

    # Clean log file
    def log_clean(self):
        self.ui.log_display.clear()
        self.ui.log_display.append(
            '-------------Log File Cleaned at ' + str(datetime.datetime.now()) + '-------------\n')

    # Clean downloadlink
    def download_clean(self):
        self.ui.downloadlink.clear()
        self.ui.log_display.append(
            '-------------Download Links Cleaned at ' + str(datetime.datetime.now()) + '-------------\n')

    # Clean paper info
    def paper_info_clean(self):
        self.ui.paper_info.clear()
        self.ui.log_display.append(
            '-------------Paper info Cleaned at ' + str(datetime.datetime.now()) + '-------------\n')

    # Save IF query history to file
    def if_save(self):
        fp = QFileDialog.getSaveFileName(
            self.ui,
            "Please select the file to save",
            r"./",
            "csv file(*.csv);;plain text(*.txt)"
        )
        filename = str(fp[0]) + str(fp[1])[-5:-1]
        f = open(filename, 'w')
        f.write(str(self.IF_list))
        f.close
        self.ui.log_display.append(
            '\n-------------IF Query File saved at ' + str(datetime.datetime.now()) + '-------------\n')

    # Save log file
    def log_save(self):
        fp = QFileDialog.getSaveFileName(
            self.ui,
            "Please select the file to save",
            r"./",
            "plain text(*.txt)"
        )
        filename = str(fp[0]) + str(fp[1])[-5:-1]
        f = open(filename, 'w')
        f.write(self.ui.log_display.toPlainText())
        f.close
        self.ui.log_display.append('-------------Log File Saved at ' + str(datetime.datetime.now()) + '-------------\n')

    # Save single query
    def paper_infio_save(self):
        fp = QFileDialog.getSaveFileName(
            self.ui,
            "Please select the file to save",
            r"./",
            "plain text(*.txt)"
        )
        filename = str(fp[0]) + str(fp[1])[-5:-1]
        f = open(filename, 'w')
        f.write(self.ui.paper_info.toPlainText())
        f.close
        self.ui.log_display.append(
            '-------------Single Query File Saved at ' + str(datetime.datetime.now()) + '-------------\n')

    #  Save query
    def save_query(self):
        fp = QFileDialog.getSaveFileName(
            self.ui,
            "Please select the file to save",
            r"./",
            "csv file(*.csv);;plain text(*.txt)"
        )
        filename = str(fp[0]) + str(fp[1])[-5:-1]
        f = open(filename, 'w')
        f.write(str(self.Paper_list))
        f.close
        self.ui.log_display.append(
            '\n-------------IF Query File saved at ' + str(datetime.datetime.now()) + '-------------\n')

    # Scihub download functions
    def pmid2doi(self):
        self.ui.log_display.append(
            '-------------PMID to DOI started at ' + str(datetime.datetime.now()) + '-------------\n')
        pmid = self.ui.pmid2doi.text()
        self.ui.link_process.setValue(50)
        doi = query.paperinfo(pmid).doi()
        self.ui.link_process.setValue(70)
        self.ui.log_display.append(pmid + '\t....................\t' + doi)
        self.ui.pmid2doi.setText(doi)
        self.ui.link_process.setValue(80)
        pyperclip.copy(doi)
        self.ui.link_process.setValue(90)
        self.ui.log_display.append('DOI has been copied to clipboard')
        self.ui.link_process.setValue(100)
        self.ui.log_display.append(
            '-------------PMID to DOI ended at ' + str(datetime.datetime.now()) + '-------------\n')
        sleep(0.2)
        self.ui.link_process.setValue(0)
        sleep(2)
        self.ui.pmid2doi.clear()

    def handleSelectionChange(self):
        domain = self.ui.hosts.currentText()
        return domain

    def singlerun(self):
        self.ui.log_display.append(
            '-------------Single link query started at ' + str(datetime.datetime.now()) + '-------------\n')
        doi = self.ui.doi_input.text()
        self.ui.link_process.setValue(20)
        link = ppdn.link(doi, self.ui.hosts.currentText())
        self.ui.link_process.setValue(50)
        self.ui.downloadlink.append('-----------------------------------------------')
        self.ui.downloadlink.append(link)
        self.ui.link_process.setValue(60)
        self.download_link = link
        self.ui.link_process.setValue(70)
        self.ui.log_display.append('The download link of ' + doi + ' is:\n' + link)
        pyperclip.copy(link)
        self.ui.link_process.setValue(85)
        self.ui.log_display.append('Download link has been copied to clipboard')
        self.ui.downloadlink.append('-----------------------------------------------\n')
        self.ui.downloadlink.ensureCursorVisible()
        self.ui.link_process.setValue(100)
        self.ui.log_display.append(
            '-------------Single link query ended at ' + str(datetime.datetime.now()) + '-------------\n')
        sleep(0.2)
        self.ui.link_process.setValue(0)

    def download(self):
        if self.download_link == '':
            QMessageBox.critical(
                self.ui,
                'How dare you!',
                'click run to get download link first!'
            )
            self.ui.log_display.append(
                'Error: Download without a link ....................... ' + str(datetime.datetime.now()) + '\n')
        else:
            QMessageBox.warning(
                self.ui,
                'Strongly no recommend',
                'If you have any other download tools, please consider using it.\nNo kidding, I did\'t optimize the download function, still a pile of shit or even worse.'
            )
            fp = QFileDialog.getSaveFileName(
                self.ui,
                "Please select the file to save",
                r"./",
                "Portable Document Format(*.pdf)"
            )
            self.ui.log_display.append(
                '-------------Download started at ' + str(datetime.datetime.now()) + '-------------\n')
            filename = str(fp[0]) + str(fp[1])[-5:-1]
            self.ui.link_process.setValue(2)
            self.ui.log_display.append(
                '-------------Good luck, close the windows if you wait too long. And I\'ve told you so.emmm-------------\n')
            self.ui.link_process.setValue(20)
            self.ui.log_display.append('File will be downloaded and saved to ' + filename)
            self.ui.link_process.setValue(30)
            wget.download(self.download_link, filename)
            self.ui.link_process.setValue(100)
            self.ui.log_display.append('.........You are so lucky.........')
            self.ui.log_display.append(
                '-------------Download ended at ' + str(datetime.datetime.now()) + '-------------\n')
            sleep(0.2)
            self.ui.link_process.setValue(0)

    # paper spider
    def query(self):
        # get terms
        main_term = self.ui.query_term.text()
        begin_year = self.ui.begin_year.text()
        end_year = self.ui.end_year.text()
        self.ui.log_display.append(
            '-------------Paper spider started at ' + str(datetime.datetime.now()) + '-------------\n')

        # merge term
        if begin_year == '' and end_year == '':
            term = main_term
            self.ui.progressBar.setValue(10)
        elif begin_year == '':
            time_term = ''' AND ("1900"[Date - Publication] : ''' + '\"' + str(
                end_year) + '\"' + '''[Date - Publication])'''
            term = main_term + time_term
            self.ui.progressBar.setValue(10)
        elif end_year == '':
            time_term = ' AND (' + '\"' + str(
                begin_year) + '\"' + '''[Date - Publication] : "3000"[Date - Publication])'''
            term = main_term + time_term
        else:
            time_term = ''' AND ("''' + str(begin_year) + '''"[Date - Publication] : "''' + str(
                end_year) + '''"[Date - Publication])'''
            term = main_term + time_term
            self.ui.progressBar.setValue(10)

        # get pmid list
        pmid_list = query.inquire(term)
        self.ui.progressBar.setValue(10)
        self.ui.log_display.append('------------- We found ' + str(pmid_list[0]) + ' papers in total-------------\n')
        self.ui.log_display.append(str(pmid_list[1:]))
        self.ui.progressBar.setValue(20)
        self.ui.log_display.append('------------- The End of PIMD List -------------\n')
        self.ui.log_display.append('------------- Begin Query---------------\n')
        self.ui.log_display.append(
            'Author,Year,Title,Journal,Abstract,Citations,keywords,Pubtype,PMID,DOI,IF,Download link\n')

        # Batch query
        tmp_num = 1
        pmid_list_len = int(len(pmid_list) - 1)

        for i in pmid_list[1:]:
            self.ui.log_display.append(
                '---------------The ' + str(tmp_num) + '/' + str(pmid_list_len) + ' paper---------------\n')
            info = query.paperinfo(i)
            pubtype = info.pubtype()
            if "Book" in pubtype:
                new_line = str(' / '.join(info.author())) + ',' + str(info.pubdate()) + ',' + str(info.title()) + ',' + str(
                    info.publisher()) + ',' + str(info.abstract()) + \
                           ',' + str(info.references()) + ',' + str(
                    '/ '.join(info.pubtype())) + ',' + '' + ',' + '' + ',' + '' + ',' + '' + ',' + ''
            else:
                IF = IF_request.main(info.journal_short())
                dlink = ppdn.link(info.doi(), self.ui.hosts.currentText())
                new_line = str(' / '.join(info.author())) + ',' + str(info.pubdate()) + ',' + str(info.title()) + ',' + str(
                    info.journal()) + \
                           ',' + str(info.abstract()) + ',' + str(info.references()) + ',' + str(
                    '/ '.join(info.keywords())) + ',' + str('/ '.join(info.pubtype())) + \
                           ',' + str(i) + ',' + str(info.doi()) + ',' + str(' | IF='.join(IF)) + ',' + str(dlink)
                self.ui.log_display.append(new_line)
                self.pv = tmp_num * 70 / int(pmid_list_len) + 20
                self.ui.progressBar.setValue(self.pv)
                tmp_num += 1
            self.Paper_list += new_line + '\n'

    # single query
    def paper_single(self):
        id = self.ui.id_iput.text()
        if len(id) == 8:
            pmid = id
        else:
            pmid = IF_request.pmid(id)
        self.ui.paper_info_process.setValue(10)
        self.ui.log_display.append('---------------Single paper info query start---------------\n')
        self.ui.log_display.append('Author,Year,Title,Journal,Abstract,Citations,keywords,Pubtype,PMID,DOI,IF,Download link\n')
        self.ui.paper_info_process.setValue(20)
        self.ui.paper_info.append('---------------Query for PMID: ' + str(pmid) + '---------------\n')
        self.ui.paper_info.append('Author,Year,Title,Journal,Abstract,Citations,keywords,Pubtype,PMID,DOI,IF,Download link\n')
        self.ui.paper_info_process.setValue(25)
        info = query.paperinfo(pmid)
        self.ui.paper_info_process.setValue(30)
        pubtype = info.pubtype()
        self.ui.paper_info_process.setValue(35)
        if "Book" in pubtype:
            self.ui.paper_info_process.setValue(50)
            result = str(' / '.join(info.author())) + ',' + str(info.pubdate()) + ',' + str(info.title()) + ',' + str(
                info.publisher()) + ',' + str(info.abstract()) + \
                     ',' + str(info.references()) + ',' + str(
                '/ '.join(info.pubtype())) + ',' + '' + ',' + '' + ',' + '' + ',' + '' + ',' + ''
            self.ui.paper_info_process.setValue(80)
        else:   
            self.ui.paper_info_process.setValue(40)
            IF = IF_request.main(info.journal_short())
            self.ui.paper_info_process.setValue(70)
            dlink = ppdn.link(info.doi(), self.ui.hosts.currentText())
            self.ui.paper_info_process.setValue(75)
            result = str(' / '.join(info.author())) + ',' + str(info.pubdate()) + ',' + str(info.title()) + ',' + str(
                info.journal()) + \
                     ',' + str(info.abstract()) + ',' + str(info.references()) + ',' + str(
                '/ '.join(info.keywords())) + ',' + str('/ '.join(info.pubtype())) + \
                     ',' + str(pmid) + ',' + str(info.doi()) + ',' + str(' | IF='.join(IF)) + ',' + str(dlink)
            self.ui.paper_info_process.setValue(80)
        self.ui.paper_info.append(result)
        self.ui.log_display.append(result+'\n')
        self.ui.log_display.append('-------------Single query ended at ' + str(datetime.datetime.now()) + '-------------\n')
        self.ui.paper_info_process.setValue(100)
        sleep(0.2)
        self.ui.paper_info_process.setValue(0)


# main
if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()
