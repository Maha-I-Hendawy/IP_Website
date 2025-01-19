from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ipaddress import ip_address, ip_network

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd85394dabea342b67953ddf95294'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips.db'
app.config['SQLALCHEMY_DATABASE_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), unique=True, nullable=False)
	email = db.Column(db.String(200), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	ip_addresses = db.relationship('IPAddress', backref='user')

	def __str__(self):
		return f"{self.username}, {self.email}"




class IPAddress(db.Model):
	ip_id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(200), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	def __str__(self):
		return f"{self.ip}"





class IPNetwork(db.Model):
	net_id = db.Column(db.Integer, primary_key=True)
	net = db.Column(db.String(200), nullable=False)

	def __str__(self):
		return f"{self.net}"



		

# login system 

# home page

@app.route('/')
def home():
	return render_template("home.html")


# registration page 

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		if password == confirm_password:
			hashed_password = generate_password_hash(password)
			user = User(username=username, email=email, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			flash("Your account has been created")
			return redirect(url_for('login'))
	return render_template("register.html")


# login page 

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = User.query.filter_by(username=username).first()
		if user and check_password_hash(user.password, password):
			session['username'] = username
			session['user_id'] = user.user_id
			flash("Hello " + user.username)
			return redirect(url_for('dashboard'))
			
	return render_template("login.html")


# logout route

@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username', default=None)
		return redirect(url_for('home'))




# crud app to create, read, update, delete an ip address 

# create ip address

@app.route("/create_ip", methods=['GET', 'POST'])
def create_ip():
	if 'username' and 'user_id' in session:
		if request.method == 'POST':
			ip = request.form['ip']
			ipaddr = ip_address(ip)

			if ipaddr:
				ip_format = format(ipaddr)
				ipaddress = IPAddress(ip=ip_format, user_id=session['user_id'])
				db.session.add(ipaddress)
				db.session.commit()
				return redirect(url_for('home'))
			else:
				flash("invalid ip address")
				return redirect(url_for('create_ip'))
		return render_template("create_ip.html")

	else:
		return redirect(url_for('login'))

	


# get a list of all ip address

@app.route('/dashboard')
def dashboard():
	if 'username' in session:

		ips = IPAddress.query.all()
		return render_template("dashboard.html", ips=ips)
	else:
		return redirect(url_for('login'))


# get ip address by id

@app.route('/get_ip/<int:id>')
def get_ip(id):
	if 'username' in session:

		ip_address = IPAddress.query.filter_by(id=id).first()
		return render_template("get_ip.html", ip_address=ip_address)

	else:
		return redirect(url_for('login'))

# update one ip address

@app.route('/update_ip/<int:id>', methods=['GET', 'POST'])
def update_ip(id):
	if 'username' in session:

		ip_address = IPAddress.query.filter_by(id=id).first()
		if request.method == 'POST':
			ip = request.form['ip']
			ip_addr = ip_address(ip)
			if ip_addr:
				ip_address.ip = ip_addr 
				db.session.commit()
				return redirect(url_for("home"))
			else:
				flash("Invalid IP Address")

		return render_template("update_ip.html")

	else:
		return redirect(url_for('login'))


# delete one ip address

@app.route("/delete_ip/<int:id>")
def delete_ip(id):
	if 'username' in session:

		ip_address = IPAddress.query.filter_by(id=id).first()
		db.session.delete(ip_address)
		db.session.commit()
		return redirect(url_for("home"))

	else:
		return redirect(url_for('login'))






