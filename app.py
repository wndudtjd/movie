from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.3lyvfuj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta



@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    comment_list = list(db.homework2.find({}, {'_id': False}))
    count = len(comment_list) + 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'star':star_receive,
        'comment':comment_receive,
        'num': count
    }
    db.movies.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies':movie_list})

#삭제버튼 구현!
@app.route("/movie/delete", methods=["POST"])
def movie_delete():
    num_receive = request.form['num_give']
    db.movies.delete_one({'num': int(num_receive)})
    return jsonify({'msg':'삭제 완료!'})

#수정버튼 구현!
@app.route("/movie/modify", methods=["POST"])
def movie_modify():
    num_receive = request.form['num_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    print(num_receive,comment_receive,star_receive)
    db.movies.update_one({'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    db.movies.update_one({'num': int(num_receive)}, {'$set': {'star': star_receive}})

    return jsonify({'msg':'수정 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)