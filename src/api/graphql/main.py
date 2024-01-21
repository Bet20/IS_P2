import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import magql
from flask_magql import MagqlExtension

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database_name'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    geom = db.Column(db.Geometry)
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    company_name = db.Column(db.String(250))
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    status = db.Column(db.String(250))
    year = db.Column(db.String(250))
    genre = db.Column(db.String(250))
    style = db.Column(db.String(250))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    notes = db.Column(db.Text)
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_on = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

    country = db.relationship('Country', backref=db.backref('releases', lazy=True))
    label = db.relationship('Label', backref=db.backref('releases', lazy=True))
    artist = db.relationship('Artist', backref=db.backref('releases', lazy=True))

schema = magql.Schema()

@schema.query.field("greet", "String!", args={"name": magql.Argument("String!", default="World")})
def resolve_greet(parent, info, **kwargs):
    name = kwargs.pop("name")
    return f"Hello, {name}!"

@schema.query.field("countries", "[Country]")
def resolve_countries(parent, info):
    return Country.query.all()

@schema.query.field("artists", "[Artist]")
def resolve_artists(parent, info):
    return Artist.query.all()

@schema.query.field("labels", "[Label]")
def resolve_labels(parent, info):
    return Label.query.all()

@schema.query.field("releases", "[Release]")
def resolve_releases(parent, info):
    return Release.query.all()

@schema.query.field("releasesByArtist", "[Release]", args={"artistId": magql.Argument("Int!")})
def resolve_releases_by_artist(parent, info, artistId):
    return Release.query.filter_by(artist_id=artistId).all()

@schema.query.field("releasesByLabel", "[Release]", args={"labelId": magql.Argument("Int!")})
def resolve_releases_by_label(parent, info, labelId):
    return Release.query.filter_by(label_id=labelId).all()

magql_ext = MagqlExtension(schema)
magql_ext.init_app(app)

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=sys.argv[1])
