from flask import Flask
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


if __name__ == "__main__":
    app.run(debug=True)
