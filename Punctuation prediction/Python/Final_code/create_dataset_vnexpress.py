#!/usr/bin/python
# -*- coding: utf8 -*-
import urllib2
import csv
import traceback
import sys
#import bson
from datetime import *
import os
from collections import OrderedDict
from collections import Counter
from datetime import datetime, timedelta
from time import strftime, gmtime
from optparse import OptionParser
import re
import shutil
import getopt
import gzip
import ast
import os.path
import datetime
import StringIO
import cStringIO
import gzip
import traceback
import sys
import codecs
import lxml.html

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def find(string,list):
    return [i for i, ltr in enumerate(string) if ltr in list]

def find_substring(string, subs):
    return [m.start() for m in re.finditer(subs, string)]
def translate(ch):
    t = ''
    if ch == ',':
        t = 'COMMA'
    elif ch == ';':
        t = 'SEMICOLON'
    elif ch == '.':
        t = 'PERIOD'
    elif ch == '!':
        t = 'EXCLAM'
    elif ch == '?':
        t = 'QMARK'
    elif ch == ':':
        t = 'COLON'
    else:
        t = 'ELLIPSIS'

    return t

def splitBrackets(doc):
    #doc = doc.encode('utf-8')
    delimiters1 = ['[','(','{']
    delimiters2 = [']',')','}']
    delimiters3 = ['"',"'"]
    doc = ' ' + doc + ' '
    new_doc = ''
      
    for j in range(0,len(doc)-1):
        if doc[j] in delimiters1:
            new_doc = new_doc + doc[j] + ' '
        if doc[j] in delimiters2:
            new_doc = new_doc + ' ' + doc[j]
        if doc[j] in delimiters3:
            new_doc = new_doc + ' ' + doc[j] + ' '
        if doc[j] not in delimiters1 + delimiters2 + delimiters3:
            new_doc = new_doc + doc[j]
    return new_doc[1:]

if __name__ == "__main__":
    f=open("url","rb")
    #f = open('urls.txt','rb')
    urls=f.readlines()
    f.close()
    #u'\u2026' la dau '...', nhieu cau ket thuc = dau ba cham
    punction=[".",",",";",":","!","?",u"\u2026"]
    end_punction = [".","!","?",u"\u2026"]
    
    g = codecs.open('train','wb',encoding = 'utf-8')
    print len(urls)
    for j in range(0, len(urls)):
        print (j+1)
        #filename = strftime("%Y-%m-%d") +"-vnexpress-{}-" +str(j+1)
        #filename = filename.format(s)

        #get url from file, remove tags: \r\n
        url = urls[j]
        if url == "#####\n":
            g.close()
            g = codecs.open('test.txt','wb',encoding = 'utf-8')
            continue
        
        url = url[:url.find('html')+4]
        #parse url
        try:
            tree = lxml.html.parse(url)
        except IOError:
            tree = lxml.html.parse(urllib2.urlopen(url))
                        
        #get plain text
        p_tags = tree.xpath('//div[@class = "fck_detail width_common"]')
        #p_tags = tree.xpath('//div[contains(concat(" ", @class, " "), " article-content")]')
        data = [p.text_content() for p in p_tags]

        #data = ' '.join(data)
        f = codecs.open('temp','wb',encoding = 'utf-8')
        f.truncate()
        for s in data:
            f.write(s)
            f.write(" ")
        f.close()

        #load data
        f = codecs.open('temp','rb')        
        data = f.read()
        f.close()

        data=data.decode("utf-8")

        #lower, remove non-breaking space \xa0, quotations, remove tabs:\n \r \t
        data=data.lower()
        e = data
        data = data.replace('...',u'\u2026')
        data = data.replace(u'\xa0',u' ')
        data = data.replace(u'\u201d',u'"')
        data = data.replace(u'\u201c',u'"')
        data = data.replace(u'\u2018',u"'")
        data = data.replace(u'\u2019',u"'")

        data = re.sub('\r',' ',data)
        data = re.sub('\t',' ',data)
        #remove external links at the end
        index = data.find('if (typeof')
        data = data[:index]
        if len(data) < 1500:
            continue
        #remove authors' name:
        #find all punctuation, remove everything after the last index
        indexes = find(data,end_punction)
        #find true index (authors name:Q.Thi)
        l = len(indexes)
        if l < 3:
            continue
        d = int(indexes[l-1]) - int(indexes[l-2])
        if d <= 7: #abbreviation
            index = indexes[l-2]
        else: #not
            index = indexes[l-1]
        data = data[1:index+1]

        #split '/' , '-', '\'
        l = ['\\', '/', '-','\n']
        idx = find(data,l)
        count = 0;
        for m in idx:
            m = m + count
            data = data[:m] + ' ' + data[m] + ' ' + data[m+1:]
            count = count + 2

        #split brackets
        data = splitBrackets(data)

        #split to words
        array= re.split(' ',data)
        array = filter(None, array)
        dataset=""
        ######################################################################
        #                           Bug fix                                  #
        #   1) double punctuation at the end                                 #
        #   2) no " " between two words                                      #
        ######################################################################
        for i in range(0,len(array)):
            word = array[i]
            #fix 1
            if (word[len(word)-1] in punction) and (word[len(word)-2] in punction) and len(word) > 1:
                word = word[:len(word)-1]
                array[i] = word
            #fix 2
            for ch in range(0,len(word)-2):
                if word[ch] in punction:
                    #print word
                    word_1 = word[:ch+1]
                    word_2 = word[ch+1:]
                    if (word_1[len(word_1)-1] in punction) and (word_1[len(word_1)-2] in punction) and len(word_1) > 1:
                        word_1 = word_1[:len(word_1)-1]
                    array = array[:i] + [word_1,word_2] + array[i+2:]       
        
        for i in range(0,len(array)):
            word=array[i]
            if len(word) > 1: 
                char = word[len(word) -1]
                if char not in punction: #key + ' ' +' '
                    word = word + ' ' +'O'
                else: #key + ' ' +punctuation
                    word = word[:len(word)- 1] + ' ' + translate(char)
                dataset = dataset +(word) +"\n" 
            elif len(word) > 0:
                if word in punction:
                    dataset = dataset[:len(dataset)-2]
                    dataset = dataset + translate(word) + '\n'
                elif word == '\n' and array[i-1] != '\n':
                    dataset = dataset +word
                elif word == ' ' or (word == '\n' and array[i-1] == '\n'):
                    continue
                else:
                    dataset = dataset + word +' ' + 'O' + '\n'
        #post processing
##        dataset += '\n'
##        capcha = find_substring(dataset,u'\u1ea3nh COLON')
##        new_lines = find_substring(dataset,'\n\n')
##        for c in capcha:
##            for nl in range(0,len(new_lines)-1):
##                if new_lines[nl] < c and new_lines[nl+1] > c:
##                    rr = new_lines[nl+1] - new_lines[nl]
##                    dataset = dataset[:new_lines[nl]]+ dataset[new_lines[nl+1]:]
##                    for cc in capcha:
##                        cc -= rr
##                    for nll in new_lines:
##                        nll -= rr
##                    break
##
##        dataset = dataset[:len(dataset)-1]            
        #f=open(filename,"wb")
        #f.truncate()
        #f.write(dataset.encode('utf-8'))
        #f.close()
        g.write(dataset)
        #g.write('\n')

g.close()
        
    
