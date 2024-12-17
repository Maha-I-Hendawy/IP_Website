from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy 
from ipaddress import ip_address, ip_network

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd85394dabea342b67953ddf95294'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips.db'
app.config['SQLALCHEMY_DATABASE_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


class IPAddress(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(200), nullable=False)

	def __str__(self):
		return f"{self.ip}"



class IPNetwork(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	net = db.Column(db.String(200), nullable=False)

	def __str__(self):
		return f"{self.net}"

# login system 

# home page

@app.route('/')
def home():
	return render_template("home.html")


# registration page 

@app.route('/register')
def register():
	return render_template("register.html")


# login page 

@app.route('/login')
def login():
	return render_template("login.html")


# logout route

@app.route('/logout')
def logout():
	return redirect(url_for("home"))




# crud app to create, read, update, delete an ip address 

# create ip address

@app.route("/create_ip", methods=['GET', 'POST'])
def create_ip():
	if request.method == 'POST':
		ip = request.form['ip']
		ip_address = ipaddress.ip_address(ip)

		if ip_address:
			db.session.add(ip_address)
			db.session.commit()
			return redirect(url_for(home))
		else:
			flash("invalid ip address")

	return render_template("create_ip.html")


# get a list of all ip address

@app.route('/dashboard')
def dashboard():
	ips = IPAddress.query.all()
	return render_template("dashboard.html", ips=ips)



# get ip address by id

@app.route('/get_ip/<int:id>')
def get_ip(id):
	ip_address = IPAddress.query.filter_by(id).first()
	return render_template("get_ip.html", ip_address=ip_address)

# update one ip address

@app.route('/update_ip/<int:id>', methods=['GET', 'POST'])
def update_ip(id):
	ip_address = IPAddress.query.filter_by(id).first()
	if request.method == 'POST':
		ip = request.form['ip']
		ip_addr = ipaddress.ip_address(ip)
		if ip_addr:
			ip_address.ip = ip_addr 
			db.session.commit()
			return redirect(url_for("home"))
		else:
			flash("Invalid IP Address")

	return render_template("update_ip.html")


# delete one ip address

@app.route("/delete_ip/<int:id>")
def delete_ip(id):
	ip_address = IPAddress.query.filter_by(id).first()
	db.session.delete(ip_address)
	db.session.commit()
	return redirect(url_for("home"))








