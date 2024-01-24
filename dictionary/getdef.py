import requests
from bs4 import BeautifulSoup

def main():
        word   = input("Input a word.")
        print(getdef(word))

if __name__ == "__main__":
    try:
        main()
    except:
        pass

def getdef(word):
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
    else:
        dif.append("No result")
        
    #Devide contents
    entry[0] = bs.find('div', id = 'dictionary-entry-1')
    entry[1] = bs.find('div', id = 'dictionary-entry-2')
    entry[2] = bs.find('div', id = 'dictionary-entry-3')

    if entry[0] is None:
        dif.append("No result")


    for j in range(3):
        count_e = 0
        count_s = 0
        count_sy = 0
        print(type(entry[j]))
        if entry[j] is not None:
            #Extract a part of speedh
            parts_of_speech = entry[j].find('h2', class_ = 'parts-of-speech')
            #Extract definitions
            span_tags = entry[j].find_all('span', class_ = 'dtText')
            #Extract example sentences
            ex_usages = entry[j].find_all('div', class_ = 'sub-content-thread')

            print("order" + str(j))

            a = word

            for part in parts_of_speech:
                a_part_of_speech = part.get_text()
                if j == 0:
                    dif.append("Part")
                    dif.append(a_part_of_speech)
                else:
                    dif.append("Part")
                    dif.append(a_part_of_speech)

                
            for span in span_tags:
                if count_s == 0:
                    dif.append("Definition")
                    dif.append(str(count_s + 1) + span.get_text())
                else:
                    dif.append(str(count_s + 1) + span.get_text())
                count_s += 1
                if count_s == 3:
                    break

            for ex in ex_usages:
                if count_e == 0:
                    dif.append("Example")
                    dif.append("・" + ex.get_text())            
                else:
                    dif.append("・" + ex.get_text())            
                count_e += 1
                if count_e == 3:
                    break

            for syn in synonyms:
                count_a = 0
                a_s = syn.find_all('a')
                for a in a_s:
                    if count_sy == j and count_a < 5:
                        if count_a == 0:
                            dif.append("Synonym")
                            dif.append("・" + a.get_text()) 
                        else:
                            dif.append("・" + a.get_text()) 
                        print("a = " + a.get_text())
                        print(str(count_sy) + ":" + str(j))
                        count_a += 1
                count_sy += 1

        # print(count_e)
        # print(count_s)
        # print(a_part_of_speech)

    # print(dif)
    return dif

#単語のデータだけ登録、
# 後の、例文や、類義語などの情報は、適宜スクレイピング




























