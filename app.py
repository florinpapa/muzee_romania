from flask import Flask
import csv
app = Flask(__name__,static_url_path='/static')

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/csv')
def getCSV():
    content = ""
    with open('static/date_muzee.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            content += ', '.join(row)
    return content

if __name__ == "__main__":
    app.run(debug=True)
