from flask import Flask
from flask import render_template
import pickle
import csv


app = Flask(__name__, static_url_path='/static')


#afisare informatii in functie de codul entitatii
@app.route("/muzee/<code>")
def get_museum_by_code(code):
    #load dictionary
    dict_file = open('data.pkl', 'rb')
    dictionar = pickle.load(dict_file)
    dict_file.close()
    #load headers
    head_file = open('headers.hd', 'rb')
    header = pickle.load(head_file)
    head_file.close()
    #cautare cod
    try:
        index = dictionar[header[0]].index(code)
        new_d = {'judet': dictionar[header[2]][index].decode(encoding="UTF-8"),
                 'de_ro': dictionar[header[3]][index].decode(encoding="UTF-8"),
                 'de_en': dictionar[header[4]][index].decode(encoding="UTF-8"),
                 'loc': dictionar[header[5]][index].decode(encoding="UTF-8"),
                 'adr': dictionar[header[7]][index].decode(encoding="UTF-8"),
                 'tel': dictionar[header[9]][index].decode(encoding="UTF-8"),
                 'p_ro': dictionar[header[12]][index].decode(encoding="UTF-8"),
                 'p_en': dictionar[header[13]][index].decode(encoding="UTF-8")}
        return render_template('muzeu.html', info=new_d)
    except:
        return "Nu s-au gasit potriviri"


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/csv')
def getCSV():
    content = ""
    dictionar = {}
    header = []
    with open('static/date_muzee.csv', 'r') as csvfile:
        count = 0
        total = ""
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            content = ' '.join(row)
            content_list = content.split('|')
            if count == 0:
                count += 1
                header += content_list
                print header
                for head in content_list:
                    dictionar[head] = []
            else:
                for i in range(len(content_list)):
                    dictionar[header[i]].append(content_list[i])
            total += content
    output = open('data.pkl', 'wb')
    pickle.dump(dictionar, output)
    output.close()
    headers = open('headers.hd', 'wb')
    pickle.dump(header, headers)
    headers.close()
    return "|".join(dictionar[header[3]])


@app.route('/muzee')
def toateMuzeele():
    # @codul entitatii muzeale pos = 0
    # @judetul pos = 2
    # @numirea (romana) pos = 3
    header = pickle.load(open('headers.hd', 'rb'))
    data = pickle.load(open('data.pkl', 'rb'))
    muzee = []
    for i in range(len(data[header[0]])):
        muzee.append({'cod': data[header[0]][i],
                     'judet': data[header[2]][i].decode(encoding="UTF-8"),
                     'nume': data[header[3]][i].decode(encoding="UTF-8")})
    return render_template('lista_muzee.html', muzee=muzee)

if __name__ == "__main__":
    app.run(debug=True)
