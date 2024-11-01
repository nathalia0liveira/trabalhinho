import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,
"bookdatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Atv(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False,
    primary_key=True)
    descricao = db.Column(db.String(80), unique=False, nullable=False,
    primary_key=False)
    data_inicio = db.Column(db.Date(), unique=False, nullable=False,
    primary_key=False)
    data_fim = db.Column(db.Date(), unique=False, nullable=False,
    primary_key=False)
    def __repr__(self):
        return "<Title: {}>".format(self.title)
    
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Convert string dates to date objects
            data_inicio = datetime.strptime(request.form.get("data_inicio"), '%Y-%m-%d').date()
            data_fim = datetime.strptime(request.form.get("data_fim"), '%Y-%m-%d').date()
            
            book = Atv(
                title=request.form.get("title"),
                descricao=request.form.get("descricao"),
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)

    # Query all books
    books = Atv.query.all()
    
    # Prepare a list of dictionaries for rendering
    bookss = []
    for book in books:
        book_data = {
            'title': book.title,
            'descricao': book.descricao,
            'data_inicio': book.data_inicio,
            'data_fim': book.data_fim
        }
        bookss.append(book_data)

    return render_template("index.html", books=bookss)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        newdescricao = request.form.get("newdescricao")
        newdata_inicio = datetime.strptime(request.form.get("newdata_inicio"), '%Y-%m-%d').date()
        newdata_fim = datetime.strptime(request.form.get("newdata_fim"), '%Y-%m-%d').date()
        
        book = Atv.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        book.descricao = newdescricao
        book.data_inicio = newdata_inicio
        book.data_fim = newdata_fim
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Atv.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)