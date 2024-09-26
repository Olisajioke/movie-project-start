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
import time


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
    rating = db.Column(db.Float, unique=False, nullable=True)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String(1000), unique=False, nullable=True)
    img_url = db.Column(db.String(250), unique=False, nullable=False)


class myform(FlaskForm):
    """Create a Movie form"""
    rating = StringField('Movie Rating(out of 10)', validators=[DataRequired()])
    #ranking = StringField('Movie Ranking', validators=[DataRequired()])
    review = StringField('Movie Review', validators=[DataRequired()])
    submit = SubmitField('Submit')



class AddMovies(FlaskForm):
    """Create a Movie form"""
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')   



@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()  # Clean up the session at the end of the request


@app.route("/", methods=["GET", "POST"])
def home():
    movies = Movie.query.all()
    sorted_movies = sorted(movies, key=lambda movie: movie.rating if movie.rating is not None else 0, reverse=True)

    #Sort movies by rating in descending order (highest rating first)
    for index, movie in enumerate(sorted_movies, start=1):
        movie.ranking = index  # Assign rank starting from 1 based on rating
        
    db.session.commit()
        
    mymovies = Movie.query.all()

    mysorted_movies = sorted(mymovies, key=lambda movie: movie.ranking, reverse=True)

    return render_template("index.html", movies=mysorted_movies)



@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovies()
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


@app.route('/edit/<int:num>', methods=['GET', 'POST'])
def edit(num):
    form = myform()

    # First, check if a query parameter 'num' was passed via the URL
    num_from_query = request.args.get('num', None)
    # Use the query parameter if it's present, otherwise fall back to the URL parameter
    if num_from_query:
        num = int(num_from_query)
    else:
        num = num
    # Fetch the movie object based on the final 'num' value
    movie_to_update = db.session.get(Movie, num)

    if request.method == "POST" and form.validate_on_submit():
        # Update the movie's rating and review from the form
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=form, movie=movie_to_update)


#get movie path
@app.route("/get_movie/<int:m_id>", methods=["GET", "POST"])
def get_movie(m_id):
    #form = myform()
    movie_to_add = MovieId(m_id)
    print(f"the movie title is {movie_to_add.title}")
    #existing_movie = db.session.get(Movie, m_id)
    #time.sleep(5)
    #existing_movie_title   = existing_movie.title
    #print(f"the existing movie title is {existing_movie_title}")
    if  request.method == "GET": 
        #if existing_movie_title != None: 
        title = movie_to_add.title
        year = movie_to_add.release_date
        description = movie_to_add.overview
        img_url = f" https://image.tmdb.org/t/p/w500/{movie_to_add.poster_path}"
        print(title, year, description, img_url)
        movie_to_edit = Movie(
            title=title,
            year=year,
            description=description,
            img_url=img_url
        )
        db.session.add(movie_to_edit)
        db.session.commit()
        return redirect(url_for('edit', num=movie_to_edit.id))
    print(f"Name: {movie_to_add.title}, ID: {movie_to_add.myid}")
    return render_template("edit.html", movie=movie_to_add, form=myform())



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
