from collections import defaultdict
import csv
import string
import os
import pandas as pd


class LIWC_Index(): 
    def __init__(self):
        self.number = None
    def category_matches(self, doc, categories):
        all_words = []
        ''' Returns a mapping of LIWC category -> number of occurrences in the given doc '''
        num_matches = defaultdict(int)
        words = doc.lower().split(' ')
        words_no_punct = [''.join(ch for ch in token if not ch in string.punctuation) for token in words] 
        for w in words_no_punct:
            all_words.append(w)
            for category in categories:
                category_stems = self.LIWC_cat_to_stems[category]
                for stem in category_stems:
                    matches_cat = w.startswith(stem.replace("*","")) if stem.endswith("*") else (stem==w)
                    if matches_cat:
                        num_matches[category]+=1
                        break # done with this category so move to the next        
        # now check text (unprocessed text that includes punctuation) for emoticons
        # for emoti_stem in self.emoticons:
        #     if emoti_stem in words:
        #         cats = self.emoticons[emoti_stem]
        #         for cat in cats:
        #             num_matches[cat]+=1
        return num_matches
    
    def __init__(self):
        (self.LIWC_stem_to_cats, self.LIWC_cat_to_stems, self.emoticons) = self.__init_LIWC_dict__()
    def __init_LIWC_dict__(self):    
        cat_col_map = {
            'Funct':[0,1,2],
            'Pronoun':[3],
           'Ppron':[4],
           'I':[5],
           'We':[6],
           'You':[7],
           'SheHe':[8],
           'They':[9],
           'Ipron':[10],
           'Article':[11],
           'Verbs':[12, 13, 14],
           'AuxVb':[15],
           'Past':[16],
           'Present':[17, 18],
           'Future':[19],
           'Adverbs':[20],
           'Prep':[21],
           'Conj':[22],
           'Negate':[23],
           'Quant':[24],
           'Numbers':[25],
           'Swear':[26],
           'Social':[27, 28, 29],
           'Family':[30],
           'Friends':[31],
           'Humans':[32],
           'Affect':[33, 34, 35, 36, 37, 38],
           'Posemo':[39, 40, 41],
           'Negemo':[42, 43, 44, 45],
           'Anx':[46],
           'Anger':[47, 48],
           'Sad':[49],
           'CogMech':[50, 51, 52, 53, 54],
           'Insight':[55, 56],
           'Cause':[57],
           'Discrep':[58],
           'Tentat':[59],
           'Certain':[60],
           'Inhib':[61],
           'Incl':[62],
           'Excl':[63],
           'Percept':[64, 65],
           'See':[66],
           'Hear':[67],
           'Feel':[68],
           'Bio':[69, 70, 71, 72],
           'Body':[73, 74],
           'Health':[75, 76],
           'Sexual':[77],
           'Ingest':[78],
           'Relativ':[79, 80, 81, 82, 83],
           'Motion':[84],
           'Space':[85, 86],
           'Time':[87, 88],
           'Work':[89, 90, 91],
           'Achiev':[92, 93],
           'Leisure':[94, 95],
           'Home':[96],
           'Money':[97, 98],
           'Relig':[99, 100],
           'Death':[101],
           'Assent':[102],
           'Nonflu':[103],
           'Filler':[104]
           }
        LIWC_stem_to_cats = defaultdict(list)
        LIWC_cat_to_stems = defaultdict(list)
        LIWC_dictionary = os.path.join(os.path.dirname(__file__), "LIWC2007dictionary.csv")
      
        row_count = -1
        for row in csv.reader(open(LIWC_dictionary, "rU")):
            row_count+=1
            if row_count<3 or row_count>171:
                continue # header rows or past any content
            for cat in cat_col_map:
                cols = cat_col_map[cat]
                for col in cols:
                    wp = row[col]
                    if wp == "":
                        continue
                    LIWC_stem_to_cats[wp].append(cat)
                    LIWC_cat_to_stems[cat].append(wp)
                    
        # add emoticons to appropriate categories
        emoticons = defaultdict(list) # emoticon -> categories
        # for pos_emoti in [':)', ':-)', ':o)', ':]', '=)', '=o)',':D', ':-D', 
        #                   ';)', ';-)', '^_-', '-_^', ':P', ':-P', '^_^', '^.^', 
        #                   ':^)', ':}', ':-}', '=-D','=D', '\o/']:
        #     emoticons[pos_emoti].append('Posemo')
        # for sad_emoti in [':(', ':-(', '):', ')-:', ':-[', ':[', ":'-(", ":'(", 
        #                   ':|', ':-|', '-_-', '._.']:
        #     emoticons[sad_emoti].extend(['Negemo', 'Sad'])
        # for scared_emoti in [":\\", ":-\\", ":/", ":-/", ':X', ':-X',
        #                      ':O', ':-O', '=/','=\\', 
        #                      '0_0', 'O_O', 'o_O', 'O_o', 'o.O']:
        #     emoticons[scared_emoti].extend(['Negemo', 'Anx'])
        # for anger_emoti in [">:(", ">:-(", ">:O", ">:-O", ">:0", ">:-0", "D:<", 
        #                      "D-:<", "O:<", "O-:<", "0-:<", "0:<", '>_<', '>:[']:
        #     emoticons[anger_emoti].extend(['Negemo', 'Anger'])
        # emoticons['$'].append('Money')
        return (LIWC_stem_to_cats, LIWC_cat_to_stems, emoticons)
    