import os

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.debug = True
BASE_DIR = os.path.dirname(app.instance_path)
db_path = os.path.join(os.path.dirname(__file__), 'table.db')
app.config.update(
    FLASK_DEBUG=1,
    SECRET_KEY='...',
    FLASK_ENV="development",
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}'
)

db = SQLAlchemy(app)


class GameTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, default=0, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(512), default='', nullable=False)
    image_link = db.Column(db.String(512), default='', nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Game: %r>' % self.name


db.create_all()


def get_game_values(games) -> list:
    games_values = list()
    for game in games:
        games_values.append([
            game.id,
            game.created.strftime("%d/%m/%Y, %H:%M:%S"),
            game.name,
            game.rate,
            game.description,
            game.image_link
        ])
    return games_values


@app.route('/', methods=['GET'])
def index():
    search_name = request.args.get('s', None)
    if search_name:
        games = GameTable.query.filter(GameTable.name.like(f'%{search_name}%')).order_by(desc(GameTable.created)).all()
    else:
        games = GameTable.query.order_by(desc(GameTable.created)).all()
    games_values = get_game_values(games)

    return render_template('index.html', games=games_values)


@app.route('/add_row', methods=['POST'])
def add_row():
    name = request.form.get('name', '<None>')
    rate = request.form.get('rate', 0)
    description = request.form.get('description', '')
    image_link = request.form.get('image_link', '')

    games = GameTable.query.filter_by(name=name).all()
    if not games:
        game = GameTable(name=name, rate=int(rate), description=description,
                         image_link=image_link)
        db.session.add(game)
        db.session.commit()
    else:
        return f'\"{name}\" - Already exist'

    return redirect(url_for('index'))


@app.route('/search_by_name', methods=['POST'])
def search_by_name():
    search_name = request.form.get('search_name', '')
    return redirect(url_for('index') + f'?s={search_name}')


@app.route('/edit', methods=['GET', 'POST'])
def edit_game():
    if request.method == 'POST':
        game_id = request.form.get('game_id', None)
        name = request.form.get('name', '<None>')
        rate = request.form.get('rate', 0)
        description = request.form.get('description', '')
        image_link = request.form.get('image_link', '')

        game = GameTable.query.filter_by(id=game_id).first()
        game.name = name
        game.rate = int(rate)
        game.description = description
        game.image_link = image_link

        db.session.commit()
        return redirect(url_for('index'))

    game_id = request.args.get('id', None)
    game = GameTable.query.filter_by(id=game_id).first()
    game_values = dict()
    if game:
        game_values = {
            'id': game.id,
            'name': game.name,
            'rate': game.rate,
            'description': game.description,
            'image_link': game.image_link
        }
    return render_template('edit.html', game=game_values)


@app.route('/delete', methods=['GET'])
def delete_game():
    game_id = request.args.get('id', None)
    GameTable.query.filter_by(id=game_id).delete()
    db.session.commit()
    return redirect(url_for('index'))