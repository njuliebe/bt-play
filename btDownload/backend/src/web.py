# -*- coding: utf-8 -*-

import getmagnet
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


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
    return "test"

if __name__ == '__main__':
    app.run(debug=True)


