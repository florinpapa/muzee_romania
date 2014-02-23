import os
from flask import Flask, request, redirect
from flask import render_template
from re import sub, search
from os import listdir
from os.path import isfile, join
import pickle
import csv


UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def search_key(index, keyword):
    """ search museum dictionary """
    #load dictionary
    dict_file = open('data.pkl', 'rb')
    dictionar = pickle.load(dict_file)
    dict_file.close()
    #load headers
    head_file = open('headers.hd', 'rb')
    header = pickle.load(head_file)
    head_file.close()
    #find keyword
    muzee = []
    if keyword == "":
        for i in range(len(dictionar[header[0]])):
            muzee.append({'cod': dictionar[header[0]][i],
                         'judet': dictionar[header[2]][i].decode(encoding="UTF-8"),
                         'nume': dictionar[header[3]][i].decode(encoding="UTF-8"),
                         'lat': sub(',', '.', dictionar[header[35]][i]),
                         'lng': sub(',', '.', dictionar[header[36]][i])})
    else:
        for i in range(len(dictionar[header[index]])):
            new_word = dictionar[header[index]][i].decode(encoding='UTF-8').lower()
            keyword = keyword.lower()
            if keyword in new_word:
                muzee.append({'cod': dictionar[header[0]][i],
                              'judet': dictionar[header[2]][i].decode(encoding="UTF-8"),
                              'nume': dictionar[header[3]][i].decode(encoding="UTF-8"),
                              'lat': sub(',', '.', dictionar[header[35]][i]),
                              'lng': sub(',', '.', dictionar[header[36]][i])})
    return muzee


@app.route('/muzee/judet/<jud>')
def get_countys(jud):
    """intoarce toate muzeele dintr-un anumit judet"""
    muzee = search_key(2, jud)
    return render_template('lista_muzee_judet.html', muzee=muzee)


@app.route('/search')
def get_matches_void():
    """ intoarce potrivirile gasite in numele muzeelor """
    muzee = search_key(3, "")
    return render_template('search_result.html', muzee=muzee)


@app.route('/search/<keyword>')
def get_matches(keyword):
    """ intoarce potrivirile gasite in numele muzeelor """
    muzee = search_key(3, keyword)
    return render_template('search_result.html', muzee=muzee)


#metoda care intoarce indexul fisierului curent
def get_current_index(all_files, filename):
    max_index = 0
    for f_name in all_files:
        print f_name
        if len(f_name) > len(filename):
            if f_name[0:len(filename)] == filename:
                index = int(f_name[len(filename):len(f_name)])
                if index > max_index:
                    max_index = index
    return str(max_index + 1)


#metoda de upload imagini
@app.route('/upload/<cod>', methods=['POST', 'GET'])
def upload_file(cod):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = cod + "_"
            all_files = listdir('./static/images')
            index = get_current_index(all_files, filename)
            print index + "###"
            filename = filename + str(index)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/muzee/" + cod)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def getImages(code):
    """ get all images from /static/images associated with a code """
    onlyfiles = [f for f in listdir(UPLOAD_FOLDER) if str(code) in f]
    return onlyfiles


#afisare informatii in functie de codul entitatii
@app.route("/muzee/<int:code>")
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
        index = dictionar[header[0]].index(str(code))
        nume = dictionar[header[3]][index].decode(encoding="UTF-8")
        photo_query = search(r'".*"', nume)
        if photo_query is None:
            photo_query = ""
        else:
            photo_query = photo_query.group(0)[1:len(photo_query.group(0)) - 1]
        new_d = {'judet': dictionar[header[2]][index].decode(encoding="UTF-8"),
                 'de_ro': nume,
                 'de_en': dictionar[header[4]][index].decode(encoding="UTF-8"),
                 'loc': dictionar[header[5]][index].decode(encoding="UTF-8"),
                 'adr': dictionar[header[7]][index].decode(encoding="UTF-8"),
                 'tel': dictionar[header[9]][index].decode(encoding="UTF-8"),
                 'p_ro': dictionar[header[12]][index].decode(encoding="UTF-8"),
                 'p_en': dictionar[header[13]][index].decode(encoding="UTF-8"),
                 'desc_ro': dictionar[header[17]][index].decode(encoding="UTF-8"),
                 'desc_en': dictionar[header[18]][index].decode(encoding="UTF-8"),
                 'lat': sub(',', '.', dictionar[header[35]][index]),
                 'lng': sub(',', '.', dictionar[header[36]][index]),
                 'coord': dictionar[header[38]][index],
                 'photo_query': '+'.join(photo_query.split(' ')),
                 'program': dictionar[header[13]][index].decode(encoding="UTF-8"),
                 'code': code,
                 'pictures': getImages(code)}
        return render_template('muzeu.html', muzeu=new_d)
    except:
        return "Nu s-au gasit potriviri"


@app.route('/adauga')
def muzeu_nou():
    return render_template('adauga_muzeu.html')


def get_next_code(dictionar, header):
    maxi = 0
    for w in dictionar[header[0]]:
        if len(w) > 0 and int(w) > maxi:
            maxi = int(w)
    return str(maxi + 1)


@app.route('/adauga/<path:muzeu>', methods=['POST', 'GET'])
def adauga_muzeu(muzeu):
    """adauga intrare noua in dictionar"""
    #load dictionary
    dict_file = open('data.pkl', 'rb')
    dictionar = pickle.load(dict_file)
    dict_file.close()
    #load headers
    head_file = open('headers.hd', 'rb')
    header = pickle.load(head_file)
    head_file.close()
    request.args.get('nume')
    #read info from form
    if request.method == 'GET':
        target_fields = {3: 'nume', 2: 'judet', 17: 'descriere', 35: 'lat', 36: 'lng'}
        for i in range(len(header)):
            if i in target_fields.keys():
                dictionar[header[i]].append(request.args.get(target_fields[i]))
            elif i == 0:
                dictionar[header[i]].append(get_next_code(dictionar, header))
            else:
                dictionar[header[i]].append("")
    output = open('data.pkl', 'wb')
    pickle.dump(dictionar, output)
    output.close()
    return redirect("/")

# @app.route('/csv')
# def getCSV():
#     content = ""
#     dictionar = {}
#     header = []
#     with open('static/date_muzee.csv', 'r') as csvfile:
#         count = 0
#         total = ""
#         reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in reader:
#             content = ' '.join(row)
#             content_list = content.split('|')
#             if count == 0:
#                 count += 1
#                 header += content_list
#                 print header
#                 for head in content_list:
#                     dictionar[head] = []
#             else:
#                 for i in range(len(content_list)):
#                     dictionar[header[i]].append(content_list[i])
#             total += content
#     output = open('data.pkl', 'wb')
#     pickle.dump(dictionar, output)
#     output.close()
#     headers = open('headers.hd', 'wb')
#     pickle.dump(header, headers)
#     headers.close()
#     return "|".join(dictionar[header[3]])


@app.route('/')
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
