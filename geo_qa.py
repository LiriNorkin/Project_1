import queue
import time
import sys
import requests
import re
import traceback
import lxml.html
import rdflib

### PART 1: Crawler & Extraction from infobox to ontology


start = time.time()

visited = set()
url_queue = queue.Queue() # queue of urls: (Type, URL), Type = Country / President / Prime_Minister

prefix = "http://en.wikipedia.org"
ontology_prefix = "http://example.org/"
url_source = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"

data_labels_to_extract_1 = ["president of", "prime minister of", "population of", "area of", "government", "capital of"]
#unwanted_data = ["\n" , " " , "by " , '"' , ", ", "(" , ")", ": " , "Executive Producer" , " (p.g.a.)"]
g = rdflib.Graph()
count_based_on = 0