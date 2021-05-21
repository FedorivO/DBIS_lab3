from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lnjmefvkshluwp:71617a7e25a670c39a8208dbced78b6e23822d2645c4fba4c5e3aa08cfa10367@ec2-54-74-35-87.eu-west-1.compute.amazonaws.com:5432/d3ok4qpdejtavb'
db = SQLAlchemy(app)

class Country(db.Model):
	__tablename__ = 'country'
	name = db.Column(db.String(50), primary_key=True, nullable=False)
	country = db.relationship('Series')

class Series(db.Model):
	__tablename__ = 'series'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(50), unique=True, nullable=False)
	rating = db.Column(db.Integer)
	country = db.Column(db.String(50),db.ForeignKey('country.name'))


db.create_all()

@app.route('/<table>/', methods=['post'])
def add(table):
	if table == "Series":
		new_id = request.form.get('new_id')
		name = request.form.get('name')
		rating = request.form.get('rating')
		country = request.form.get('country')
		new = Series(id = new_id, name = name, rating = rating, country = country)
	elif table == "Country":
		name = request.form.get('name')
		new = Country(name = name)
	try:
		db.session.add(new)
		db.session.commit()
	except Exception:
		if table == "Series":
			return redirect(url_for('show_series'))
		elif table == "Country":
			return redirect(url_for('show_country'))
	if table == "Series":
		return redirect(url_for('show_series'))
	elif table == "Country":
		return redirect(url_for('show_country'))

@app.route('/<table>/Update', methods=['post'])
def update(table):
	if table == "Series":
		name = request.form.get('Name')
		rating = request.form.get('Rating')
		country = request.form.get('Country')
		new_id = request.form.get('Id')
		new = db.session.query(Series).get(new_id)
		new.name = name
		new.rating = rating
		new.country = country
	try:
		db.session.commit()
	except Exception:
		if table == "Series":
			return redirect(url_for('show_series'))
		elif table == "Country":
			return redirect(url_for('show_country'))
	if table == "Series":
		return redirect(url_for('show_series'))
	elif table == "Country":
		return redirect(url_for('show_country'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)

@app.route('/Series')
def show_series():
	data = Series.query.all()
	return render_template('index.html', data=data,table="Series")

@app.route('/Country')
def show_country():
	data = Country.query.all()
	return render_template('index_country.html', data=data,table="Country")

@app.route('/<table>/delete/<name>')
def delete(table,name):
	if table == "Series":
		data = Series.query.all()
	elif table == "Country":
		data = Country.query.all()
	else:
		return redirect(url_for('index'))
	for d in data:
		if d.name == name:
			db.session.delete(d)
			db.session.commit()
	if table == "Series":
		return redirect(url_for('show_series'))
	elif table == "Country":
		return redirect(url_for('show_country'))
	else:
		return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
