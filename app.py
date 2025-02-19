from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ipaddress import ip_address, ip_network
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd85394dabea342b67953ddf95294'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips.db'
app.config['SQLALCHEMY_DATABASE_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


# User Model 


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), unique=True, nullable=False)
	email = db.Column(db.String(200), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	ip_addresses = db.relationship('IPAddress', backref='user')

	def __str__(self):
		return f"{self.username}, {self.email}"



# IPAddress Model

class IPAddress(db.Model):
	ip_id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.Date, default=datetime.utcnow)
	date_updated = db.Column(db.Date)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	def __str__(self):
		return f"{self.ip}"



# IPNetwork Model

class IPNetwork(db.Model):
	net_id = db.Column(db.Integer, primary_key=True)
	net = db.Column(db.String(200), nullable=False)

	def __str__(self):
		return f"{self.net}"



		

# login system 

# home page



# registration page 

@app.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		data = request.get_json()
		username = data['username']
		email = data['email']
		password = data['password']
		confirm_password = data['confirm_password']
		if password == confirm_password:
			hashed_password = generate_password_hash(password)
			user = User(username=username, email=email, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			return jsonify({"user": user})
	return jsonify({"method": "Please, register"})


# login page 

@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		data = request.get_json()
		username = data['username']
		password = data['password']

		user = User.query.filter_by(username=username).first()
		if user and check_password_hash(user.password, password):
			session['username'] = username
			session['user_id'] = user.user_id
		
			return jsonify({"message": "Hello, " + user})
			
	return jsonify({"message": "Please, log in"})


# logout route

@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username', default=None)
		return jsonify({"message": "You are logged out"})




# crud app to create, read, update, delete an ip address 

# create ip address

@app.route("/ips", methods=['POST'])
def add_ip():
	if 'username' and 'user_id' in session:
		if request.method == 'POST':
			data = request.get_json()
			ip = data['ip']
			ipaddr = ip_address(ip)

			if ipaddr:
				ip_format = format(ipaddr)
				ipaddress = IPAddress(ip=ip_format, user_id=session['user_id'])
				db.session.add(ipaddress)
				db.session.commit()
				return jsonify({"ip": ipaddress})
			else:
				return jsonify("message": "invalid ip address")
		return jsonify("message": "Add Ip Address")

	else:
		return jsonify({"message": "Please, log in"})

	


# get a list of all ip address

@app.route('/ips', methods=['GET'])
def get_ips():
	if 'username' in session:

		ips = IPAddress.query.all()
		return jsonify({"ips": ips})
	else:
		return jsonify({"message": "Please, login"})


# get ip address by id

@app.route('/ips/<int:ip_id>', methods=['GET'])
def get_ip(ip_id):
	if 'username' in session:

		ip_address = IPAddress.query.filter_by(id=ip_id).first()
		return jsonify({"ip_address": "ip_address" })

	else:
		return jsonify({"message": "Please, log in"})

# update one ip address

@app.route('/ips/<int:ip_id>/update', methods=['PUT'])
def update_ip(ip_id):
	if 'username' in session:

		ip_address = IPAddress.query.filter_by(id=id).first()
		if request.method == 'PUT':
			data = request.get_json()
			ip = data['ip']
			ip_addr = ip_address(ip)
			if ip_addr:
				ip_address.ip = ip_addr 
				db.session.commit()
				return jsonify({"ip_addr": ip_addr})
			else:
				return jsonify({"message": "invalid ip address "})

		return jsonify({"message": "update ip address"})

	else:
		return jsonify({"message": "Please, log in"})


# delete one ip address

@app.route("/ips/<int:ip_id>/delete", methods=['DELETE'])
def delete_ip(id):
	if 'username' in session:
		if request.method == 'DELETE':
			ip_address = IPAddress.query.filter_by(id=id).first()
			db.session.delete(ip_address)
			db.session.commit()
			return jsonify({"ip_address": "ip_address"})
		else:
			return jsonify({"message": "Delete ip address"})

	else:
		return jsonify({"message": "Please, log in"})







