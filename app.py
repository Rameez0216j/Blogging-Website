from email.policy import default
from flask import request
from flask import Flask, render_template,redirect
# Using database
from flask_sqlalchemy import SQLAlchemy
#for message displaying
from flask import flash
#for login
from flask_login import LoginManager,login_user,UserMixin,logout_user
#for Blog post date and time capture
from datetime import datetime


app=Flask(__name__)

#*****************************************************************
# for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'RameezAhmad' # This is same as csrf token in django
db = SQLAlchemy(app)


#for login
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # id ---> default field in our database (return None if id not found)
#*****************************************************************

#********************* Model Creation  *************************

class User(UserMixin,db.Model): # is_active error is avoided using UserMixin
    # Even you change anything in this class and want it to reflect in database then delete existing database and do as done in terminal
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<User {self.user_name}>'
    
# Blog model
class Blog(db.Model):
    blog_id=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(80),nullable=False)
    Content=db.Column(db.Text(),nullable=False)
    Author=db.Column(db.String(50),nullable=False)
    pub_date=db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return f'<Blog {self.Title}>'

#*****************************************************************


# print(app)
### Routing 
@app.route("/") # -----> / implies blank url
def index():
    data=Blog.query.all()
    return render_template("index.html",data=data)


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('pass')
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        user_id=request.form.get('id')
        # print(email,password,first_name,last_name,user_id)
        user=User(email=email,password=password,firstname=first_name,lastname=last_name,user_name=user_id)
        db.session.add(user)
        db.session.commit()
        # return ("User registered successfully")
        flash("User is registered Successfully!",'success') # flash(Message,category)
        return redirect('/login')

    return render_template("register.html")





@app.route("/login",methods=["GET","POST"]) # This line is to be used as it is everytime 
def login():
    if request.method=="POST":
        userName=request.form.get('username')
        password=request.form.get('password')
        # user=User.query.filter_by(user_name=userName) # returns an alchemy Object
        # use terminal to check what is in user above
        user=User.query.filter_by(user_name=userName).first()  # returns user object
        if user and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid Credentials','danger')
            return redirect('/login')
    return render_template("login.html")
# at return we actually return html templates



@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')




@app.route("/blogpost",methods=["GET","POST"])
def blogpost():
    if request.method=="POST":
        tit=request.form.get("title")
        con=request.form.get("content")
        auth=request.form.get("author")
        blog=Blog(Title=tit,Content=con,Author=auth)
        db.session.add(blog)
        db.session.commit()
        flash("Your post has been submitted successfully","success")
        return redirect('/')
    return render_template('blog.html')



@app.route("/blog_detail/<int:id>",methods=["GET","POST"])
def blog_details(id):
    item=Blog.query.get(id)
    return render_template('blog_detail.html',blog=item)




@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_blog(id):
    blog=Blog.query.get(id)
    if request.method=="POST":
        blog.Title=request.form.get('title')
        blog.Content=request.form.get('content')
        blog.Author=request.form.get('author')
        db.session.commit()
        flash("Post has been  updated",'success')
        return redirect('/')
    return render_template('Edit_blog.html',blog=blog) # it can also be item=blog what name you use here you need to use it in template the same




@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete_post(id):
    item=Blog.query.get(id)
    db.session.delete(item)  # To delete the item from database
    db.session.commit()
    flash("Your Post has been Deleted",'success')
    return redirect('/')



if(__name__=="__main__"):
    app.run(debug=True)  # debug = True is used to show error on browser if something happens
 