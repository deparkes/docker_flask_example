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

@app.route("/api/v1/resources/books/json", methods=['GET'])
def api_filter2():
    # curl --header "Content-Type: application/json" -X POST -d ""{"""books""":[{"""id""":null,"""author""":"""Ann Leckie ""","""published""":2014},{"""id""":null,"""author""":"""John Scalzi""","""published""":2013}]}""  http://127.0.0.1:5000/api/v1/resources/books/json
    # Need to do several escapes (particularly in windows)
    books = request.get_json()

   

    results = []
    for book in books['books']:
        query = "SELECT * FROM books WHERE"
        to_filter = []
        try:
            id = book['id']
            published = book['published']
            author = book['author']
            print(book)

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
            
            results.append(cur.execute(query, to_filter).fetchall()[0])
        except:
            print(jsonify(book))


    
    return jsonify(results)

    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    




