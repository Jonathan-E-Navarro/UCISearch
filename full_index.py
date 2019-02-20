   #iterates over the keys which is the folder and file of its corresponding html file
    #TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
    #IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
   
    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:37:12 2018

@author: Jonathan
"""

import json 
from pprint import pprint
from bs4 import BeautifulSoup
import re
from sys import getsizeof
import math
from collections import Counter

#tokenization functions 
def useRegEx(string):
    return re.sub('[^0-9a-zA-Z]+',' ', string)
def tokenize(f):
        list_file = list()
        x =useRegEx(f)
        x = x.lower()
        x = x.split()
        if len(x) > 0:
            for item in x:
                list_file.append(item)
        return sorted(list_file)

if __name__ == '__main__':
    #This is where the bookkeeping file is
    #Turn bookkeeping file into directory 
    json_file = '/Users/jonathannavarro/Desktop/github/CS121/WEBPAGES_RAW/bookkeeping.json' 
    file_ = open(json_file)
    data = json.load(file_)
    
    #This is where the Webpages are
    html_start = '/Users/jonathannavarro/Desktop/github/CS121/WEBPAGES_RAW/'


    key = 0
    i=0
    token_dict = {}
    num_docs = len(data)
    
    #iterates over the keys which is the folder and file of its corresponding html file
    #TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
    #IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
    bad_links = ['39/373', '29/494', '35/269','0/438','12/318','14/488','15/245',
    '15/79','18/340','19/336','2/274','20/131','26/494','27/151','34/172','38/25',
    '39/244','39/98','40/459','41/494','44/424','48/345','52/132','55/433','60/201',
    '62/434','65/38','66/124','69/87','7/320','7/367','7/410','71/109','74/309','35/397',
    '47/118','48/121','48/246','49/410','5/338','6/45','63/142','66/300']
    doc_list = []
    for d in data:
        if d != None and d not in bad_links:
            key = d
            print(key)
            #link = data[key]
            #print(link)
            html_string = html_start+key
            #open the file and use beautiful soup to parse the Html
            text_file = open(html_string)
            soup = BeautifulSoup(text_file,'html.parser')
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.decompose()    # rip it out

            #Get all text from the parsed html 
            text = soup.get_text()
            #get Tokens
            tokens = tokenize(text)
    
            doc_list.append((key,tokens))


            i+=1
    #number of documents with term t in it = length of dict[term]
    #number of documents = len of doc_list 
    #number of times term t appears in a document = doc[1].count(token)
    #total number of terms in document = len(doc[1]) 
    #TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
    #IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
    num_of_docs = len(doc_list)
    for doc in doc_list:
        #print(doc)
        print("indexing: ",doc[0])
        for token in doc[1]:
            dict1 = {}
            if token not in token_dict:
                # term_in_docs = 0
                # for doc in doc_list:
                #     if token in doc[1]:
                #         term_in_docs+=1
                # TF = doc[1].count(token)/len(doc[1])
                # IDF = math.log(num_of_docs/term_in_docs)
                # TFIDF = TF*IDF

                dict1[doc[0]] = (doc[1].count(token),len(doc[1])) 
                #dict1[doc[0]] = TFIDF
                token_dict[token] = dict1
            else:
                # term_in_docs = 0
                # for doc in doc_list:
                #     if token in doc[1]:
                #         term_in_docs+=1
                # TF = doc[1].count(token)/len(doc[1])
                # IDF = math.log(num_of_docs/term_in_docs)
                # TFIDF = TF*IDF
                dict1[doc[0]] = (doc[1].count(token),len(doc[1])) 
                #dict1[doc[0]] = TFIDF
                token_dict[token].update(dict1)


    #TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
    #IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

    # pprint(token_dict)
    for term in token_dict:
        # print(term,token_dict[term])
        # print('length of:',term,' ',len(token_dict[term]))
        for doc in token_dict[term]:
            # print(token_dict[term][doc])
            TF = token_dict[term][doc][0]/token_dict[term][doc][1]
            IDF = math.log(num_of_docs/len(token_dict[term]))
            # print('TF =',TF)
            # print('IDF =',IDF)
            token_dict[term][doc] = TF*IDF
            # print('\n')

    # pprint(token_dict)


    print(len(doc_list))
    print(len(token_dict))
    print(getsizeof(token_dict))

    # pprint(token_dict)
    print('lenght of when:',len(token_dict['when']))

    with open('index.txt', 'w') as file:
        file.write(json.dumps(token_dict)) # use `json.loads` to do the reverse
  
    text = 0        
    while text != 'exit()':
        text = input("Search: ")
        query = text.split()
        if len(query) > 0:
            final_dict = Counter()
            for term in query:
                if term in token_dict:
                    # print(term)
                    # pprint(token_dict[term])
                    partial = Counter(token_dict[term])
                    final_dict+=partial

            # pprint(final_dict)
            # sorted_final = sorted(final_dict, key=final_dict.get,reverse = True)
            # print(sorted_final)

            sorted_results = sorted( ((k,v) for v,k in final_dict.items()), reverse=True)
            for i in range(10):
                try:
                    # print(sorted_results[i])
                    print(data[sorted_results[i][1]])
                    print('\n')
                except:
                    pass


            
            
            
            
            
            