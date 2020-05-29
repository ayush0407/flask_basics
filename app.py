from datetime import datetime

from flask import Flask, request, render_template
# import pymongo as pm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:test@localhost/catalog_db'
#app.config.update(
    #SECRET_KEY='test',
    #SQLALCHEMY_DATABASE_URI='postgresql://postgres:test@localhost/catalog_db',
#SQLALCHEMY_TRACK_MODIFICATIONS=False
#)
db=SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/new/')
def query_string(greeting = 'hello'):
    query_val=request.args.get('greeting', greeting)
    return '<h1> the greeting is :{0}</h1>'.format(query_val)

@app.route('/user/')
@app.route('/user/<name>')
def no_query_strings(name='John'):
    return '<h1> hello there ! {} </h1>'.format(name)

@app.route('/numbers/<int:num>')
def numbers(num):
    return '<h1> the number you picked is:' +str(num)+'</h1>'

@app.route('/add/<float:n1>/<float:n2>')
def adding(n1,n2):
    return str(n1+n2)

@app.route('/temp')
def temp():
    return render_template('hello.html')
@app.route('/watch')
def top_movies():
    movie_list=['ts1','Taken','TopGun','cooliyo']
    return render_template('movies.html',movies=movie_list,name='Taken')

@app.route('/tables')
def movies_plus():
    movies_dict={'Topgun':5,'Harry':4,'Mi5':4.5,'MIB':3.5}
    return render_template('table_data.html',movies=movies_dict,name='Harry')

class Publication(db.Model):
    __tablename__ = 'publication'
    id=db.Column(db.INTEGER,primary_key=True)
    name=db.Column(db.String(80),nullable=False)

    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __repr__(self):
        return 'The id is {}, Name is {}'.format(self.id,self.name)

class Books(db.Model):
    __tablename__ = 'book'
    id=db.Column(db.INTEGER,primary_key=True)
    title=db.Column(db.String,nullable=False,index=True)
    author=db.Column(db.String(350))
    avg_rating=db.Column(db.Float)
    format=db.Column(db.String(50))
    image=db.Column(db.String(100),unique=True)
    num_pages=db.Column(db.Integer)
    pub_date=db.Column(db.DateTime,default=datetime.utcnow())

    pub_id=db.Column(db.INTEGER,db.ForeignKey('publication.id'))

    def __init__(self,title,author,avg_rating,format,image,num_pages):
        self.title=title
        self.author=author
        self.avg_rating=avg_rating
        self.format=format
        self.image=image
        self.num_pages=num_pages
    def __repr__(self):
        return 'The title is {}'.format(self.title)






if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
