# -*- coding: utf-8 -*-

import getmagnet
from flask import Flask, jsonify, render_template, request
import db
import download

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
cache = db.cache


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/movie/search', methods=['POST'])
def search_movies():
    movie_name = request.json['name']
    movies = getmagnet.search_movie(movie_name = movie_name)
    return jsonify({'movies':list(movies)})


@app.route('/movie/list', methods=['POST'])
def get_movies():
    task_ids = request.json['task_ids']
    tasks = []
    for task_id in task_ids:
        task = cache.get(task_id=task_id)
        tasks.append(task)

    return jsonify({"downloads" : tasks})

@app.route('/movie/download', methods=['POST'])
def download_movie():
    try:
        magnet = request.json['magnet']
        download.pool_download(magnet=magnet)
        return jsonify({"result" : "success"}), 200
    except Exception as e:
        print e.message
        return 400




if __name__ == '__main__':
    app.run(debug=True)


