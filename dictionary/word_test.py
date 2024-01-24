import requests
from bs4 import BeautifulSoup
# from .models import words
import random


# for i in range(5):
#     a = random.randint(1, 101)
#     a_word = words.objects.get(id = a)
#     # print(a_word.name)

def get_example(word):
    dif = []
    entry = [""] * 3
    url = "https://www.merriam-webster.com/dictionary/" + word
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    #Find contents in below url
    con = bs.find('div', class_ = 'left-content')
    if con is not None:
        labels_get = con.find_all('p', class_ = 'function-label')
        synonyms = con.find_all('ul', class_ = 'mw-grid-table-list synonyms-antonyms-grid-list')

    #Devide contents
    entry[0] = bs.find('div', id = 'dictionary-entry-1')
    entry[1] = bs.find('div', id = 'dictionary-entry-2')
    entry[2] = bs.find('div', id = 'dictionary-entry-3')

    for j in range(3):
        count_e = 0
        count_s = 0
        count_sy = 0
        if entry[j] is not None:
            #Extract a part of speedh
            parts_of_speech = entry[j].find('h2', class_ = 'parts-of-speech')
            #Extract definitions
            span_tags = entry[j].find_all('span', class_ = 'dtText')
            #Extract example sentences
            ex_usages = entry[j].find_all('div', class_ = 'sub-content-thread')


            a = word

            try:
                for part in parts_of_speech:
                    a_part_of_speech = part.get_text()
                    if j == 0:
                        dif.append("Part")
                        dif.append(a_part_of_speech.replace(a, "_" * len(word)))
                    else:
                        dif.append("Part")
                        dif.append(a_part_of_speech.replace(a, "_" * len(word)))
            except:
                pass

            try:
                for span in span_tags:
                    a_span = span.get_text()
                    if count_s == 0:
                        dif.append("Definition")
                        dif.append(str(count_s + 1) + a_span.replace(a, "_" * len(word)))
                    else:
                        dif.append(str(count_s + 1) + a_span.replace(a, "_" * len(word)))
                    count_s += 1
                    if count_s == 3:
                        break
            except:
                pass

            try:
                for ex in ex_usages:
                    a_ex = ex.get_text()
                    if count_e == 0:
                        dif.append("Example")
                        dif.append("・" + a_ex.replace(a, "_" * len(word)))            
                    else:
                        dif.append("・" + a_ex.replace(a, "_" * len(word)))            
                    count_e += 1
                    if count_e == 3:
                        break
            except:
                pass

            try:
                for syn in synonyms:
                    count_a = 0
                    a_s = syn.find_all('a')
                    for a in a_s:
                        a_a = a.get_text()
                        if count_sy == j and count_a < 5:
                            if count_a == 0:
                                dif.append("Synonym")
                                dif.append("・" + a_a) 
                            else:
                                dif.append("・" + a_a) 
                            count_a += 1
                    count_sy += 1
            except:
                pass

            # print("Synonym-----------------")

    # print(type(dif))


    return dif











