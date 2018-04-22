from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask.ext.cache import Cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/bt?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

movie_status = ('downloading', 'done')

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taskid = db.Column(db.String(256), unique=True, nullable=False, server_default='')
    name = db.Column(db.String(500), nullable=False, server_default='')
    magnet = db.Column(db.String(500), nullable=False, server_default='')
    addtime = db.Column(db.DateTime)
    status = db.Column(db.INTEGER)

    def __init__(self, name, magnet, taskid, status):
        self.name = name
        self.magnet = magnet
        self.status = status
        self.taskid = taskid

    def __repr__(self):
        return '<Movie %r>' % self.name


def create_db():
    db.drop_all()
    test_data = [Movie('123',  'magnet:test', '',  0)]
    db.create_all()
    db.session.add_all(test_data)
    db.session.commit()



class Download():
    __tablename__ = 'download'
    def __init__(self, taskid, name, progress, speed, peer_nums):
        self.taskid = taskid
        self.name = name
        self.progress = progress
        self.speed = speed
        self.peer_nums = peer_nums

    def __repr__(self):
        return '<Download name %r status %r>' % self.name %self.status



if __name__ == '__main__':
    create_db()