from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template, redirect
import pymysql
from searcher import *
import time

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    title = 'researcher search engine'
    return render_template('search_index.html', title=title)


@app.route('/search/')
def search():
    time_start = time.time()
    flag = True
    search_instance = SearchModule()
    while flag:
        global query
        global search_results
        global lens

        query = request.args.get('query')
        search_instance.get_search_query(query)
        search_results, lens = search_instance.conduct_search()
        time_end = time.time()
        if not search_results:
            return render_template('no_result.html', title='No results found', message=query)
        print(query)
        login_url = '/search/page/1/'
        return redirect(login_url)


@app.route('/search/page/<int:page>/', methods=['GET', 'POST'])
def next(page):
    perpage = 10
    startat = (page - 1) * perpage
    pages = []

    for i in range(1, lens // 10 + 1):
        pages.append(i)
    search_results2 = search_results[startat:startat + perpage]
    db = pymysql.connect("127.0.0.1", "root", "password", "RESEARCHERS")
    cursor = db.cursor()
    target = []
    for i in search_results2:
        select_str = 'SELECT * FROM PROFILE WHERE ID = %s'
        cursor.execute(select_str, i)
        persons = cursor.fetchone()
        target.append(persons)
    target = tuple(target)
    db.close()
    return render_template('search_results.html', persons=target, pages=pages, ID=search_results, query=query,
                           lens=lens, error=True)


@app.route('/search/persons/<id>/', methods=['GET', 'POST'])
def content(id):
    db = pymysql.connect("127.0.0.1", "root", "password", "RESEARCHERS")
    cursor = db.cursor()
    select_str = 'SELECT * FROM PROFILE WHERE ID = %s'
    cursor.execute(select_str, id)
    person_detail = cursor.fetchall()
    person_detail = person_detail[0]
    return render_template('persons_content.html', id=id, persons=person_detail)

if __name__ == '__main__':
    app.run(debug=True)
