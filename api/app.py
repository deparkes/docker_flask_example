from flask import Flask, request, jsonify, render_template
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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

    to_filter = []
    query = build_select_books_query(author, id, published, to_filter)
    conn = sqlite.connect('../data/books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

@app.route("/api/v1/resources/books/json", methods=['GET'])
def api_filter_json():
    books = request.get_json()
    results = []
    for book in books['books']:
        to_filter = []

        id = book['id']
        published = book['published']
        author = book['author']
        query = build_select_books_query(author, id, published, to_filter)

        conn = sqlite.connect('../data/books.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()

        results.append(cur.execute(query, to_filter).fetchall()[0])

    return jsonify(results)


def build_select_books_query(author, id, published, to_filter):
    query = "SELECT * FROM books WHERE"
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
        pass
        # return page_not_found(404)
    query = query[:-4] + ';'
    return query


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    




