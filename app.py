from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import requests
from movieapi import MovieApi, MovieList, MovieId


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fav-movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)




class Movie(db.Model):
    """Create a Movie table"""  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String(1000), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)


class myform(FlaskForm):
    """Create a Movie form"""
    title = StringField('Movie Title', validators=[DataRequired()])
    year = StringField('Movie Year', validators=[DataRequired()])
    description = StringField('Movie Description', validators=[DataRequired()])
    rating = StringField('Movie Rating(out of 10)', validators=[DataRequired()])
    ranking = StringField('Movie Ranking', validators=[DataRequired()])
    review = StringField('Movie Review', validators=[DataRequired()])
    img_url = StringField('Movie Image URL', validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.route("/", methods=["GET", "POST"])
def home():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)



@app.route("/add", methods=["GET", "POST"])
def add():
    form = myform()
    if request.method == "POST":
        movie3444 = form.title.data
        print(f"The movie you tried to add is: {movie3444}")
        return redirect(url_for('select', movie3444=movie3444))
    return render_template('add.html', form=form)



@app.route("/confirm_delete/<int:m_id>", methods=["GET", "POST"])
def confirm_delete(m_id):
    #movie_to_delete = Movie.query.get(m_id)
    movie_to_delete = db.session.get(Movie, m_id)
    return render_template("confirm-delete.html", movie=movie_to_delete)


# This route will allow you to delete a movie from the database
@app.route("/delete/<int:m_id>", methods=["GET", "POST"])
def delete(m_id):
    #movie_to_delete = Movie.query.get(m_id)
    movie_to_delete = db.session.get(Movie, m_id)
    if request.method == "GET":
        db.session.delete(movie_to_delete)
        db.session.commit()
    return render_template("delete.html", movie=movie_to_delete)


#edit movie
@app.route("/edit/<int:m_id>", methods=["GET", "POST"])
def edit(m_id):
    #movie_to_edit = Movie.query.get(m_id)
    form = myform()
    movie_to_add = MovieId(m_id)
    
    movie_edit = Movie.query.get_or_404(m_id)

    #print(f"the movie title is {movie_to_add.title}")
    if request.method == "POST":
        try:
            title = movie_to_add.title
            year = movie_to_add.release_date
            description = movie_to_add.overview
            img_url = f" https://image.tmdb.org/t/p/w500/{movie_to_add.poster_path}"
            rating = form.rating.data
            review = form.review.data
            print(title, year, description, rating, review, img_url)
            movie_to_edit = Movie(
                title=title,
                year=year,
                description=description,
                rating=rating,
                review=review,
                img_url=img_url
            )
            db.session.add(movie_to_edit)
            db.session.commit()
            return redirect(url_for('home'))
        
        except Exception as e:
            return f"An error occurred: {e}. We can't add {title} to the database."
    return render_template("edit.html", movie=movie_to_add, movie_edit=movie_edit, form=myform())




@app.route("/select", methods=["GET", "POST"])
def select():
    moveee = request.args.get('movie3444')
    print(moveee)
    movies = MovieList(movie=moveee)
    print(movies)
    return render_template("select.html",movies=movies.movie_list)









with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
