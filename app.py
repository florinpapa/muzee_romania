from flask import Flask
from flask import render_template
import pickle
import csv


app = Flask(__name__,static_url_path='/static')


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
        muzee.append({'cod': data[header[0]][i], 'judet': data[header[2]][i].decode(encoding="UTF-8"), 'nume': data[header[3]][i].decode(encoding="UTF-8")})
    return render_template('lista_muzee.html', muzee=muzee)

if __name__ == "__main__":
    app.run(debug=True)
