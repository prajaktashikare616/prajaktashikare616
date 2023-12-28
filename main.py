from flask import Flask, render_template, url_for, request, flash, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///student.db"
app.app_context().push()
db = SQLAlchemy(app)

class student(db.Model):
	id         = db.Column(db.Integer, primary_key=True)
	name       = db.Column(db.String(100))
	course     = db.Column(db.String(50))
	year       = db.Column(db.String(200))
	percentage = db.Column(db.String(10)) 

	def __init__(self, name, course, year, percentage):
		self.name=name
		self.course=course
		self.year=year
		self.percentage=percentage

@app.route("/")
def home():
    return render_template("index.html", students=student.query.all())

@app.route("/student")
def index():
	return render_template("index.html", students=student.query.all())

@app.route("/insert", methods=['GET', 'POST'])
def insert():
	if request.method=='POST':
		std=student(request.form['name'], request.form['course'], request.form['year'], request.form['percentage'])
		db.session.add(std)
		db.session.commit()
		return redirect(url_for("index"))

	return render_template("insert.html")

@app.route("/update/<int:sid>", methods=['GET','POST'])
def update(sid):
	std=student.query.get(sid)
	#std=student.query.get_or_404(sid)

	if request.method=="POST":
		std.name=request.form['name'] 
		std.course=request.form['course']
		std.year=request.form['year']
		std.percentage=request.form['percentage']
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("update.html",student=std)


@app.route("/delete/<int:sid>", methods=['GET','POST'])
def delete(sid):
	std=student.query.get(sid)
	
	if request.method=="POST":
		db.session.delete(std)
		db.session.commit()
		return redirect(url_for("index"))
	
	return render_template("delete.html",student=std)

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = student.query.filter(student.name.ilike(f"%{query}%")).all()
    return render_template("index.html", students=results, query=query)


	

if __name__=="__main__":

	app.run(debug=True)
db.create_all()