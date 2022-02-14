from flask import Flask , render_template , request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc =  db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        title = (request.form["title"])
        desc = (request.form["desc"])
        todo = Todo(title = title,desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html",allTodo=allTodo)


@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo   )
    return 'This is products page!'


@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method == "POST":
        title = (request.form["title"])
        desc = (request.form["desc"])
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)
    



@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# Flask assingment 1

@app.route("/assingment")
def hello_world_assingment():
    smap = {
        1:"st",
        2:"nd",
        3:"rd",
        4:"th"
    }
    smonth = {
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "April",
        5 : "May",
        6 : "Jun",
        7 : "Jul",
        8 : "Aug",
        9 : "Sep",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec"
    }
    curr_date = datetime.now().date()
    suffix = smap[1]
    dd = curr_date.day
    mm = curr_date.month
    yy = curr_date.year

    # Handles the suffix of date part
    last_digit = dd%10
    tmpdd = dd/10
    second_lastdigit = tmpdd%10

    if second_lastdigit == 1:
        suffix = "th"
    else:
        if last_digit > 3:
            last_digit = 4
        suffix = smap[last_digit]

    mm = smonth[mm]

    return render_template("index_a1.html",dd=dd,suffix = suffix,mm=mm,yy=yy) 



if __name__ == "__main__":
    app.run(debug=True)