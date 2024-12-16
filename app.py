from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


# login system 

# home page

@app.route('/')
def home():
	return render_template("home.html")


# registration page 

@app.route('/register', method=['GET', 'POST'])
def register():
	return render_template("register.html")


# login page 

@app.route('/login', method=['GET', 'POST'])
def login():
	return render_template("login.html")


# logout route

@app.route('/logout')
def logout():
	return redirect(url_for("home"))




# crud app to create, read, update, delete an ip address 

# create ip address

@app.route("/create_ip", method=['GET', 'POST'])
def create_ip():
	return render_template("create_ip.html")


# get a list of all ip address

@app.route('/all_ips')
def all_ips():
	return render_template("all_ips.html")



# get ip address by id

@app.route('/get_ip/<int:id>')
def get_ip(id):
	return render_template("get_ip.html")



@app.route('/update_ip/<int:id>')
def update_ip(id):
	return render_template("update_ip.html")



@app.route("/delete_ip/<int:id")
def delete_ip(id):
	pass





