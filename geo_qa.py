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

def question_spaces_to_bottom_line(question):
    return question.replace(" ", "_")

def question_to_sparql_query(question):
    length_q = len(question)
    question = question_spaces_to_bottom_line(question)
    part_for_query = ""

    # question starting with Who
    if question.find("Who") != -1:
        # Who is the president of <country>?
        if question.find("president") != -1:
            part_for_query = question[24:length_q - 1]

            # query place

        # Who is the prime minister of <country>?
        if question.find("prime") != -1:
            part_for_query = question[29:length_q - 1]

            # query place

        # Who is <entity>?
        else:
            part_for_query = question[7:length_q - 1]

            # query place

    # question starting with What
    if question.find("What") != -1:
        # What is the area of <country>?
        if question.find("area") != -1:
            part_for_query = question[20:length_q - 1]

            # query place

        # What is the population of <country>?
        if question.find("population") != -1:
            part_for_query = question[26:length_q - 1]

             # query place

        # What is the capital of <country>?
        if question.find("capital") != -1:
            part_for_query = question[23:length_q - 1]

            # query place

        # What is the form of government in <country>?
        if question.find("government") != -1:
            part_for_query = question[34:length_q - 1]

            # query place

    # question starting with When
    if question.find("When") != -1:
        # When was the president of <country> born?
        if question.find("president") != -1:
            part_for_query = question[26:length_q - 6]

            # query place

        # When was the prime minister of <country> born?
        if question.find("prime") != -1:
            part_for_query = question[31:length_q - 6]

            # query place

    # question starting with where
    if question.find("Where") != -1:
        # Where was the president of <country> born?
        if question.find("president") != -1:
            part_for_query = question[27:length_q - 6]

            # query place

        # Where was the prime minister of <country> born?
        if question.find("prime") != -1:
            part_for_query = question[32:length_q - 6]

            # query place

    # How many presidents were born in <country>?
    if question.find("were_born_in") != -1:
        part_for_query = question[33:length_q-1]

        # query place

    # List all countries whose capital name contains the string <str>
    if question.find("List_all") != -1:
        part_for_query = question[58:length_q]

        # query place

    # How many <government_form1> are also <government_form2>?
    if question.find("are_also") != -1:
        # government form1
        part_for_query = question[9:length_q - 23]
        # government form2
        part_for_query2 = question[31:length_q - 1]

        # query place


