from flask import Flask, render_template, request, redirect
import os
from datetime import datetime

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "moviedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(60), unique=False)
    location = db.Column(db.String(60), unique=False)
    time = db.Column(db.Time(60), unique=False)

    # def __repr__(self):
    #     return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        time_v = datetime.strptime(request.form.get("time"),"%H:%M").time()
        movie = Movie(movie_name=request.form.get("movie_name"), location=request.form.get("location"), time=time_v)
        db.session.add(movie)
        db.session.commit()

        return redirect('/movies')
    
    return render_template("home.html")

@app.route("/movies", methods=["GET"])
def movie_list():
    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)

    movies = Movie.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template("movie_list.html", movies=movies)

@app.route("/movies/update/<int:id>", methods=["GET", "POST"])
def movie_update(id):
    movie = Movie.query.get_or_404(ident=id)
    
    if request.form:
        time_v = datetime.strptime(request.form.get("time"),"%H:%M:%S").time()
        movie.movie_name = request.form.get("movie_name")
        movie.location = request.form.get("location")
        movie.time = time_v
        db.session.commit()

        return redirect('/movies')
    
    return render_template("update.html", movie=movie)

@app.route("/delete", methods=["POST"])
def movie_delete():
    if request.form:
        movie_id = request.form.get("id")
        movie = Movie.query.get_or_404(ident=movie_id)
        db.session.delete(movie)
        db.session.commit()
    
    return redirect("/movies")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

