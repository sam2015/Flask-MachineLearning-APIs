#importing library
from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

# initiating flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/CSV_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'issecret'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# define our models

class User(UserMixin, db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	password = db.Column(db.String(30))


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class GameTable(db.Model):
	__tablename__ = 'game_table'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(30))
	score = db.Column(db.Float())
	genre = db.Column(db.String(30))
	editors_choice = db.Column(db.String(1))
	platform = db.Column(db.String(20))

# APIs for login, register, games info

@app.route('/signup/<string:username>/<string:password>')
def sign_up(username, password):
	user = User(username=username, password=password)
	db.session.add(user)
	db.session.commit()
	return 'registered!!!!!'


@app.route('/signin/<string:username>/<string:password>',methods=['POST'])
def index(username, password):
	user = User.query.filter_by(username=username, password=password).first()
	login_user(user)
	return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
	game = GameTable.query.all()
	return jsonify(games=[{'title': g.title, 'platform': g.platform, 'score': g.score, 'genre': g.genre, 'editors_choice': g.editors_choice} for g in game])

# route to pages

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('signin.html')

@app.route('/game_page')
def page():
	return render_template('home.html')



if __name__ == '__main__':
	app.run(debug=True)


