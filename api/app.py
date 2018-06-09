from flask import Flask, request, jsonify, Response
import json
import sqlite3 as sqlite
app = Flask(__name__)



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
@app.route('/', methods=['GET'])
def home():
    return """<h1>Distant Reading Archive</h1>
    <p>A prototype API for distant reading of science fiction novels</p>
    """

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite.connect('../data/books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute("SELECT * FROM books;").fetchall()
    return jsonify(all_books)

@app.route("/api/v1/resources/books", methods=['GET'])
def api_filter():
    query_parameters = request.args
    
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    
    
    query = "SELECT * FROM books WHERE"
    to_filter = []
    
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    
    query = query[:-4] + ';'
    
    conn = sqlite.connect('../data/books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])

def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

@app.route('/api/add_message', methods=['GET', 'POST'])
def add_message():
    #curl --header "Content-Type: application/json" -X POST -d "{"""age""":"""10""","""password""":"""xyz"""}"  http://127.0.0.1:5000/api/add_message
    
    print (request.is_json)
    content = request.get_json()
    print (content['age'])
    if int(content['age'])>20:
        return "1"
    else:
        return "0"

@app.route("/api/v1/resources/books/json", methods=['POST'])
def api_filter2():
    
    content = request.get_json()

   
    query = "SELECT * FROM books WHERE"
    to_filter = []
    
    try:
        print('!!!!!')
        id = content['id']
        published = content['published']
        author = content['author']
        print(content)
    except:
        print(jsonify(content))

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    
    query = query[:-4] + ';'
    
    conn = sqlite.connect('../data/books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    




