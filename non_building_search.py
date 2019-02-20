import json 
from pprint import pprint
from bs4 import BeautifulSoup
import re
from sys import getsizeof
import math
from collections import Counter



if __name__ == '__main__':
	json_file1= 'index.txt'
	file_ = open(json_file1)
	token_dict = json.load(file_)

	json_file = '/Users/jonathannavarro/Desktop/github/CS121/WEBPAGES_RAW/bookkeeping.json' 
	file_2 = open(json_file)
	data = json.load(file_2)

	text = 0 
	# pprint(token_dict)
	while text != 'exit()':
		text = input("Search: ")
		query = text.split()
		if len(query) > 0:
			final_dict = Counter()
			for term in query:
				if term in token_dict:
					partial = Counter(token_dict[term])
					final_dict+=partial

			sorted_results = sorted( ((k,v) for v,k in final_dict.items()), reverse=True) 
			for i in range(10):
				try:
					print(data[sorted_results[i][1]])
					print('\n')
				except:
					pass      
            
