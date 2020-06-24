from flask import Flask, render_template, url_for, flash, redirect, session, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from werkzeug.utils import secure_filename 
import os, random, string, json, re
from datetime import datetime as dtm
from json.decoder import JSONDecoder
import matplotlib.pyplot as plt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'U4kXLz4WLzkrAdyTBYwi5A'
'''
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'db_autosched'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
'''
userpass = 'mysql+pymysql://root:@'
basedir = '127.0.0.1'
dbname = '/db_autosched'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'autoschedulingsystem@gmail.com'
app.config['MAIL_PASSWORD'] = 'sistempenjadwalanft'

db = SQLAlchemy(app)
mail = Mail(app)



@app.route("/",methods=['POST','GET'])
def main():
	error=None
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		r = db.engine.execute("SELECT * FROM user WHERE username=%s AND password=%s",(username,password))
		data_user =''
		for i in r:
			data_user = i
		if data_user != '':
			# print(data_user.id_user)
			if data_user.id_user == 1:
				session['username']=data_user.username
				flash('Selamat datang '+data_user.nama, 'success')
				r = db.engine.execute("SELECT * FROM User WHERE id_user=1")
				data_user=''
				for i in r:
					data_user=i
					foto=data_user.foto
				rv = db.engine.execute("SELECT jadwal.id_kgn,kegiatan.nama_kgn,jadwal.tanggal,jadwal.id_org FROM jadwal INNER JOIN kegiatan ON jadwal.id_kgn=kegiatan.id_kgn")
				dataJson = []
				for result in rv:
					id_kgn = result[0]
					nama = result[1]
					tanggal = result[2]
					harike = tanggal.strftime('%j')
					
					tglstr = dtm.strftime(tanggal,'%d')
					blnstr = dtm.strftime(tanggal,'%m')
					thstr = dtm.strftime(tanggal,'%Y')
					tgl = int(tglstr)
					bln = int(blnstr)
					th = int(thstr)
					date = str(th) +','+ str(bln) +','+ str(tgl)

					id_user=result[3]
					if id_user == 2:
						warna = "blue"
					elif id_user == 3:
						warna = "darkblue"
					elif id_user == 4:
						warna = "black"
					elif id_user == 5:
						warna = "green"
					elif id_user == 6:
						warna = "darkred"
					elif id_user == 7:
						warna = "red"
					elif id_user == 8:
						warna = "chocolate"
					elif id_user == 9:
						warna = "orange"
					elif id_user == 10:
						warna = "brown"
					elif id_user == 11:
						warna = "darkgreen"
					elif id_user == 12:
						warna = "dodgerblue"
					else:
						warna = "gray"
					
					content = {
						"title":nama,
						"id_kgn":id_kgn,
						"start":date,
						"backgroundColor":warna,
						"borderColor":warna
					}
					
					dataJson.append(content)
					#content = {}
				return render_template('admin_dashboard.html', foto=foto, dataJson=dataJson)
			else:
				session['username']=data_user.username
				flash('Selamat datang '+data_user.nama, 'success')
				s = db.engine.execute("SELECT * FROM user WHERE username=%s",data_user.username)
				data_org = ''
				for i in s:
					data_org = i
					id_org=data_org.id_user
					foto_org=data_org.foto
					nama_org=data_org.nama
					username=data_org.username
				rv = db.engine.execute("SELECT jadwal.id_kgn,kegiatan.nama_kgn,jadwal.tanggal,jadwal.id_org FROM jadwal INNER JOIN kegiatan ON jadwal.id_kgn=kegiatan.id_kgn")
				dataJson = []
				for result in rv:
					id_kgn = result[0]
					nama = result[1]
					tanggal = result[2]
					harike = tanggal.strftime('%j')
					
					tglstr = dtm.strftime(tanggal,'%d')
					blnstr = dtm.strftime(tanggal,'%m')
					thstr = dtm.strftime(tanggal,'%Y')
					tgl = int(tglstr)
					bln = int(blnstr)
					th = int(thstr)
					date = str(th) +','+ str(bln) +','+ str(tgl)

					id_user=result[3]
					if id_user == 2:
						warna = "blue"
					elif id_user == 3:
						warna = "darkblue"
					elif id_user == 4:
						warna = "black"
					elif id_user == 5:
						warna = "green"
					elif id_user == 6:
						warna = "darkred"
					elif id_user == 7:
						warna = "red"
					elif id_user == 8:
						warna = "chocolate"
					elif id_user == 9:
						warna = "orange"
					elif id_user == 10:
						warna = "brown"
					elif id_user == 11:
						warna = "darkgreen"
					elif id_user == 12:
						warna = "dodgerblue"
					else:
						warna = "gray"
					content = {
						"title":nama,
						"id_kgn":id_kgn,
						"start":date,
						"backgroundColor":warna,
						"borderColor":warna
					}
					dataJson.append(content)
					#content = {}
				return render_template('org_dashboard.html',s=s,id_org=id_org, username=username, foto=foto_org, nama=nama_org, dataJson=dataJson)
		else:
			flash('Username atau Password yang anda masukkan salah. Silahkan Periksa Kembali Username dan Password Anda','warning')
			r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
			data_user =''
			for i in r:
				data_user = i
				kontak=data_user.nomor
				email=data_user.email
				return render_template('index.html',kontak=kontak, email=email)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)
			error=error

@app.route('/login')
def login():
	r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
	data_user =''
	for i in r:
		data_user = i
		kontak=data_user.nomor
		email=data_user.email
		return render_template('index.html',kontak=kontak, email=email)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route("/lupapassword")
def lupapassword():
	r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
	data_user =''
	for i in r:
		data_user = i
		kontak=data_user.nomor
		email=data_user.email
		return render_template('lupapassword.html',kontak=kontak, email=email)	

@app.route("/reset", methods=['POST'])
def reset():
	if request.method == 'POST':
		details = request.form
		email = details['email']
		r = db.engine.execute("SELECT * FROM User WHERE email=%s",(email))
		data_user = ''
		for i in r:
			data_user = i
		if data_user != '':
			res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
			newpass = str(res)
			r = db.engine.execute("UPDATE User SET password=%s WHERE id_user=%s",(newpass,data_user.id_user))
			msg = Message('Password anda berhasil direset', sender='Autoscheduling System', recipients=[data_user.email])
			msg.body = """Berikut adalah password baru anda = %s""" % newpass
			mail.send(msg)
			#email terdaftar
			return render_template('lupapassword.html', status = 1)
		else:
			#email tidak ditemukan
			return render_template('lupapassword.html', status = 2)
	else:
		return render_template('lupapassword.html')

@app.route("/dashboardadmin")
def dashboardadmin():
	if 'username' in session:
		r = db.engine.execute("SELECT * FROM User WHERE id_user=1")
		data_user=''
		for i in r:
			data_user=i
			foto=data_user.foto
		rv = db.engine.execute("SELECT jadwal.id_kgn,kegiatan.nama_kgn,jadwal.tanggal,jadwal.id_org FROM jadwal INNER JOIN kegiatan ON jadwal.id_kgn=kegiatan.id_kgn")
		dataJson = []
		for result in rv:
			id_kgn = result[0]
			nama = result[1]
			tanggal = result[2]
			harike = tanggal.strftime('%j')
			
			tglstr = dtm.strftime(tanggal,'%d')
			blnstr = dtm.strftime(tanggal,'%m')
			thstr = dtm.strftime(tanggal,'%Y')
			tgl = int(tglstr)
			bln = int(blnstr)
			th = int(thstr)
			date = str(th) +','+ str(bln) +','+ str(tgl)

			id_user=result[3]
			if id_user == 2:
				warna = "blue"
			elif id_user == 3:
				warna = "darkblue"
			elif id_user == 4:
				warna = "black"
			elif id_user == 5:
				warna = "green"
			elif id_user == 6:
				warna = "darkred"
			elif id_user == 7:
				warna = "red"
			elif id_user == 8:
				warna = "chocolate"
			elif id_user == 9:
				warna = "orange"
			elif id_user == 10:
				warna = "brown"
			elif id_user == 11:
				warna = "darkgreen"
			elif id_user == 12:
				warna = "dodgerblue"
			else:
				warna = "gray"
			
			content = {
				"title":nama,
				"id_kgn":id_kgn,
				"start":date,
				"backgroundColor":warna,
				"borderColor":warna
			}
			dataJson.append(content)
			#content = {}
			
		#return json.dumps(dataJson)
		return render_template('admin_dashboard.html', foto=foto, dataJson=dataJson)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/profileadmin")
def profileadmin():
	if 'username' in session:
		r = db.engine.execute("SELECT * FROM User WHERE id_user=1")
		data_user=''
		for i in r:
			data_user=i
			nama=data_user.nama
			nomor=data_user.nomor
			email=data_user.email
			foto=data_user.foto
			username=data_user.username
			password=data_user.password
			return render_template('admin_profile.html',nama=nama,nomor=nomor,email=email,foto=foto,username=username,password=password)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

ALLOWED_EXTENSION = set(['png', 'jpeg', 'jpg'])
app.config['UPLOAD_FOLDER'] = 'static/img/profile'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
@app.route("/editprofileadmin",methods=['POST','GET'])
def editprofileadmin():
	if 'username' in session:
		if request.method == 'POST':
			r = db.engine.execute("SELECT * FROM User WHERE id_user=1")
			data_user=''
			for i in r:
				data_user=i
				passwd=data_user.password
			nama = request.form['nama']
			nomor = request.form['nomor']
			L = list(nomor)
			if L[0] == '0':
				L[0]='62'
				nomor = "".join(L)
			email = request.form['email']
			foto = request.files['foto']
			username = request.form['username']
			newpassword = request.form['newpassword']
			newpass = request.form['newpass']
			passw = request.form['password']
			if passw == passwd:
				if newpassword !='':
					if newpass == newpassword:
						passw = newpass
						if foto and allowed_file(foto.filename):
							filename = secure_filename(foto.filename)
							foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
							r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, foto=%s, username=%s, password=%s WHERE id_user=1",(nama,nomor,email,foto.filename,username,passw))
							flash('Profil berhasil diubah', 'success')
							return redirect(url_for('profileadmin'))
						else:
							r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s,  username=%s, password=%s WHERE id_user=1",(nama,nomor,email,username,passw))
							flash('Profil berhasil diubah', 'success')
							return redirect(url_for('profileadmin'))
					else:
						flash('Password baru yang anda masukkan tidak sesuai','warning')
						return redirect(url_for('editprofileadmin'))
				else:
					if foto and allowed_file(foto.filename):
						filename = secure_filename(foto.filename)
						foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, foto=%s, username=%s WHERE id_user=1",(nama,nomor,email,foto.filename,username))
						flash('Profil berhasil diubah', 'success')
						return redirect(url_for('profileadmin'))
					else:
						r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, username=%s WHERE id_user=1",(nama,nomor,email,username))
						flash('Profil berhasil diubah', 'success')
						return redirect(url_for('profileadmin'))
			else:
				flash('Profil tidak dapat diubah karena password yang anda masukkan salah', 'warning')
				return redirect(url_for('profileadmin'))
		else:
			r = db.engine.execute("SELECT * FROM User WHERE id_user=1")
			data_user=''
			for i in r:
				data_user=i
				kode=data_user.id_user
				nama=data_user.nama
				nomor=data_user.nomor
				email=data_user.email
				foto=data_user.foto
				username=data_user.username
				password=data_user.password
				return render_template('edit_profileadmin.html',kode=kode,nama=nama,nomor=nomor,email=email,foto=foto,username=username,password=password)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/lihatorg")
def lihatorg():
	if 'username' in session:
		r = db.engine.execute("SELECT * FROM user WHERE id_user!=1")
		s = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in s:
			data_user = i
			id_user = data_user.id_user
			foto_adm=data_user.foto
		return render_template('lihat_dataorg.html',id_user=id_user,foto=foto_adm,r=r)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/editorg/<int:id_org>", methods=['POST','GET'])
def editorg(id_org):
	if'username' in session:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			foto=data_user.foto
		s = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
		data_org=''
		for x in s:
			data_org = x
			id_org = data_org.id_user
			nama = data_org.nama
			nomor = data_org.nomor
			email = data_org.email
			foto_org = data_org.foto
			username = data_org.username
			password = data_org.password
		if request.method == 'POST':
			nama = request.form['nama']
			nomor = request.form['nomor']
			email = request.form['email']
			foto_org = request.files['foto']
			username = request.form['username']
			password = request.form['password']
			if foto_org and allowed_file(foto_org.filename):
				filename = secure_filename(foto_org.filename)
				foto_org.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, foto=%s, username=%s, password=%s WHERE id_user=%s",(nama,nomor,email,foto_org.filename,username,password,id_org))
				flash('Data berhasil diubah', 'success')
				return redirect(url_for('lihatorg'))
			else:
				r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, username=%s, password=%s WHERE id_user=%s",(nama,nomor,email,username,password,id_org))
				flash('Data berhasil diubah', 'success')
				return redirect(url_for('lihatorg'))
		else:			
			return render_template('edit_dataorg.html',s=s,foto=foto,id_org=id_org,nama=nama,nomor=nomor,email=email,foto_org=foto_org,username=username,password=password)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/hapusorg/<int:id_org>", methods=['GET'])
def hapusorg(id_org):
	if'username' in session:
		s = db.engine.execute("DELETE FROM user WHERE id_user=%s",id_org)
		flash('Data berhasil dihapus', 'success')
		return redirect(url_for('lihatorg'))
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/tambahorg", methods=['POST','GET'])
def tambahorg():
	if'username' in session:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			foto=data_user.foto
		if request.method == 'POST':
			nama = request.form['nama']
			nomor = request.form['nomor']
			L = list(nomor)
			if L[0] == '0':
				L[0]='62'
				nomor = "".join(L)
			email = request.form['email']
			foto_org = request.files['foto']
			username = request.form['username']
			passw = request.form['password']
			password = request.form['repassword']
			if passw == password:
				if foto_org and allowed_file(foto_org.filename):
					filename = secure_filename(foto_org.filename)
					foto_org.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					s = db.engine.execute("INSERT INTO user (nama, nomor, email, foto, username, password) VALUES (%s,%s,%s,%s,%s,%s)",(nama,nomor,email,foto_org.filename,username,password))
					flash('Data berhasil ditambahkan','success')
					return redirect(url_for('lihatorg'))
			else:
				flash('Data masukkan Anda salah, silahkan coba lagi','warning')
				return redirect(url_for('tambahorg'))
		return render_template('tambahorg.html',foto=foto)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/editjadwal")
def editjadwal():
	if'username' in session:
		s = db.engine.execute("SELECT jadwal.id_kgn,user.nama,kegiatan.nama_kgn,jadwal.tanggal,jadwal.waktu,jadwal.target,kegiatan.deskripsi,kegiatan.prioritas FROM kegiatan INNER JOIN user ON kegiatan.id_user=user.id_user INNER JOIN jadwal ON jadwal.id_org=kegiatan.id_user WHERE jadwal.id_kgn=kegiatan.id_kgn")
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			foto=data_user.foto
			return render_template('edit_jadwal.html', foto=foto, s=s)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/algen")
def algen():
	if'username' in session:
		t = db.engine.execute("SELECT * FROM user")
		s = db.engine.execute("SELECT kegiatan.id_kgn,user.nama,kegiatan.nama_kgn,kegiatan.tanggal,kegiatan.waktu,kegiatan.target,kegiatan.deskripsi,kegiatan.prioritas FROM kegiatan INNER JOIN user ON kegiatan.id_user=user.id_user")
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			foto=data_user.foto
			return render_template('generate.html',foto=foto,s=s,t=t)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/editkegiatan/<string:id_kgn>", methods=['POST','GET'])
def editkegiatan(id_kgn):
	if 'username' in session:
		if request.method == 'POST':
			nama_kgn = request.form['nama']
			tanggal = request.form['tanggal']
			waktu = request.form['waktu']
			target = request.form['target']
			deskripsi = request.form['deskripsi']
			x = db.engine.execute("UPDATE jadwal SET tanggal=%s, waktu=%s, target=%s WHERE id_kgn=%s",(tanggal,waktu,target,id_kgn))
			y = db.engine.execute("UPDATE kegiatan SET nama_kgn=%s, deskripsi=%s WHERE id_kgn=%s",(nama_kgn,deskripsi,id_kgn))
			flash('Data berhasil diubah','success')
			return redirect(url_for('editjadwal'))
		else:
			s = db.engine.execute("SELECT jadwal.id_org,user.nama,kegiatan.nama_kgn,jadwal.tanggal,jadwal.waktu,jadwal.target,kegiatan.deskripsi FROM kegiatan INNER JOIN jadwal ON jadwal.id_kgn=kegiatan.id_kgn INNER JOIN user ON jadwal.id_org=user.id_user WHERE jadwal.id_kgn=%s",id_kgn)
			for i in s:
				id_user=i[0]
				nama=i[1]
				nama_kgn=i[2]
				tanggal=i[3]
				waktu=i[4]
				target=i[5]
				deskripsi=i[6]

			r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
			data_user =''
			for i in r:
				data_user = i
				foto=data_user.foto
				return render_template('editkegiatan.html', foto=foto,nama=nama,nama_kgn=nama_kgn,tanggal=tanggal,waktu=waktu,target=target,deskripsi=deskripsi,id_user=id_user)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/editkegiatansgen/<string:id_kgn>", methods=['POST','GET'])
def editkegiatansgen(id_kgn):
	if 'username' in session:
		if request.method == 'POST':
			nama_kgn = request.form['nama']
			tanggal = request.form['tanggal']
			waktu = request.form['waktu']
			target = request.form['target']
			deskripsi = request.form['deskripsi']
			y = db.engine.execute("UPDATE kegiatan SET nama_kgn=%s,tanggal=%s, waktu=%s,target=%s, deskripsi=%s WHERE id_kgn=%s",(nama_kgn,tanggal,waktu,target,deskripsi,id_kgn))
			flash('Data berhasil diubah','success')
			return redirect(url_for('algen'))
		else:
			s = db.engine.execute("SELECT kegiatan.id_user,user.nama,kegiatan.nama_kgn,kegiatan.tanggal,kegiatan.waktu,kegiatan.target,kegiatan.deskripsi FROM kegiatan INNER JOIN user ON kegiatan.id_user=user.id_user WHERE kegiatan.id_kgn=%s",id_kgn)
			for i in s:
				id_user=i[0]
				nama=i[1]
				nama_kgn=i[2]
				tanggal=i[3]
				waktu=i[4]
				target=i[5]
				deskripsi=i[6]

			r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
			data_user =''
			for i in r:
				data_user = i
				foto=data_user.foto
				return render_template('editkegiatansgen.html', foto=foto,nama=nama,nama_kgn=nama_kgn,tanggal=tanggal,waktu=waktu,target=target,deskripsi=deskripsi,id_user=id_user)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/hapuskgn/<string:id_kgn>", methods=['GET'])
def hapuskgn(id_kgn):
	if'username' in session:
		r = db.engine.execute("DELETE FROM jadwal WHERE id_kgn=%s",id_kgn)
		s = db.engine.execute("DELETE FROM kegiatan WHERE id_kgn=%s",id_kgn)
		flash('Data berhasil dihapus', 'success')
		return redirect(url_for('algen'))
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/loading")
def loading():
	if'username' in session:
		s = db.engine.execute("SELECT * FROM kegiatan")
		jumlah_individu = 5
		jumlah_proker = sum([1 for row in s])-1
		#print(jumlah_proker)
		jumlah_generasi = 5
		mutasion_rate = 0.3
		#inisialisasi populasi
		populasi=[]
		for i in range(jumlah_individu):
			individu=[]
			s = db.engine.execute("SELECT * FROM kegiatan")
			for j in s:
				kegiatan=[]
				idkegiatan = j.id_kgn 
				organisasi=j.id_user
				tanggal=j.tanggal
				strharike = tanggal.strftime('%y%j')
				harike = int(strharike)
				waktu=j.waktu
				target=j.target
				prioritas=j.prioritas
				
				kegiatan=[idkegiatan,organisasi,harike,waktu,target,prioritas]
				
				#print("organisasi ",kegiatan[0],"pada hari ke ",kegiatan[1],"waktu:",kegiatan[2],"target",kegiatan[3],"prioritas",kegiatan[4],"id kegiatan",kegiatan[5])
				individu.append(kegiatan)
			#print(individu[i][0])
			populasi.append(individu)
		#evaluasi
		for generasi_ini in range(jumlah_generasi):
			simpan_fitness=[]
			for i in range(jumlah_individu):
				fitness = 0
				skor = 0
				for j in range(jumlah_proker):   
					for k in range(j+1, jumlah_proker-1):
						#print("indeks ",j,"dibanding dengan indeks ", k)
						#cek tanggal
						if populasi[i][j][2] == populasi[i][k][2]:
							#print("populasi j : ", populasi[i][j][1]," dibanding populasi k : ",populasi[i][k][1])
							#cek target
							if populasi[i][j][4]==3 and populasi[i][k][4]==3: 
								#cek waktu       
								if populasi[i][j][3] == populasi[i][k][3]:                            
									fitness+=0
								elif populasi[i][j][3]==4 and (populasi[i][k][3]==1 or populasi[i][k][3]==2):
									fitness+=0
								elif populasi[i][j][3]==5 and (populasi[i][k][3]==2 or populasi[i][k][3]==3):
									fitness+=0
								elif populasi[i][j][3]==6:
									fitness+=0
								#elif (populasi[i][j][3]==1 or populasi[i][j][3]==2) and (populasi[i][k][3]==4 or populasi[i][k][3]==6):
								#	fitness+=0
								#elif (populasi[i][j][3]==2 or populasi[i][j][3]==3) and (populasi[i][k][3]==5 or populasi[i][k][3]==6):
								#	fitness+=0
								#elif populasi[i][j][3]==4 and (populasi[i][k][3]==1 or populasi[i][k][3]==2 or populasi[i][k][3]==6):
								#	fitness+=0
								#elif populasi[i][j][3]==5 and (populasi[i][k][3]==2 or populasi[i][k][3]==3 or populasi[i][k][3]==4 or populasi[i][k][3]==6):
								#	fitness+=0
								#elif populasi[i][j][3]==6 and (populasi[i][k][3]==1 or populasi[i][k][3]==2 or populasi[i][k][3]==3 or populasi[i][k][3]==4 or populasi[i][k][3]==5):
								#	fitness+=0
								else:
									fitness+=1
							else:
    								fitness+=1
						else:
							fitness+=1
				
				simpan_fitness.append(fitness)
				#print("individu ", i," skor fitness =", fitness)
			
			offspring=[]
			while len(offspring)<jumlah_individu:     
				#seleksi
				total_fitness=sum(simpan_fitness)
				#print(total_fitness)
				bagi_presentasi=[]
				for i in range(jumlah_individu):
					presentasi=simpan_fitness[i]/total_fitness*100
					bagi_presentasi.append(presentasi)

				for i in range(jumlah_individu):
					if i!=0:
						bagi_presentasi[i]+=bagi_presentasi[i-1]
					#print("individu ", i," skor presentasi =", bagi_presentasi[i])
				parent=[]
				for x in range(2):
					pilih=random.randint(0,100)
					#print("pilih =", pilih)
					for i in range(jumlah_individu):
						if pilih<bagi_presentasi[i]:
							parent.append(i)
							#print("Parent ", x," terpilih. Individu", i)
							break
					#print("Parent ", x," terpilih.")
				for i in range(jumlah_proker):
					#crossover
					temp_id 				= populasi[parent[0]][i][0]
					temp_org				= populasi[parent[0]][i][1]
					temp_waktu				= populasi[parent[0]][i][3]
					temp_target				= populasi[parent[0]][i][4]
					#print("populasi parent 0",temp_org,temp_waktu,temp_target,temp_id)
					#print("populasi parent 1",populasi[parent[1]][i][0],populasi[parent[1]][i][2],populasi[parent[1]][i][3],populasi[parent[1]][i][5])
					populasi[parent[0]][i][0]	= populasi[parent[1]][i][0]
					populasi[parent[0]][i][1]	= populasi[parent[1]][i][1]
					populasi[parent[0]][i][3] 	= populasi[parent[1]][i][3]
					populasi[parent[0]][i][4]	= populasi[parent[1]][i][4]

					populasi[parent[1]][i][0]	= temp_id
					populasi[parent[1]][i][1] 	= temp_org
					populasi[parent[1]][i][3] 	= temp_waktu
					populasi[parent[1]][i][4] 	= temp_target

					offspring.append(populasi[parent[0]])
					offspring.append(populasi[parent[1]])
					
					#print("sesudah\n",populasi[parent[0]])
					#print(populasi[parent[1]])
			
			#mutasi
			for i in range(jumlah_individu):
				if random.random()<mutasion_rate:
					#print("sebelum termutasi\n")
					#print(offspring[i])
					for j in range(jumlah_proker):
						for k in range(j+1, jumlah_proker):
							#print(populasi[i][j][4])
							#print(populasi[i][k][4])
							#cek tanggal
							if populasi[i][j][2] == populasi[i][k][2]:
								#cek target
								if populasi[i][j][4]==3 and populasi[i][k][4]==3:
									#cek waktu
									if populasi[i][j][3] == populasi[i][k][3]:
										#cek prioritas
										if populasi[i][j][5] > populasi[i][k][5]:
											populasi[i][k][2] = random.randint(populasi[i][k][2]-30,populasi[i][k][2]+30)
										else:
											populasi[i][j][2] = random.randint(populasi[i][j][2]-30,populasi[i][j][2]+30)
									elif populasi[i][j][3]==4 and (populasi[i][k][3]==1 or populasi[i][k][3]==2):
										#cek prioritas
										if populasi[i][j][5] > populasi[i][k][5]:
											populasi[i][k][2] = random.randint(populasi[i][k][2]-30,populasi[i][k][2]+30)
										else:
											populasi[i][j][2] = random.randint(populasi[i][j][2]-30,populasi[i][j][2]+30)
									elif populasi[i][j][3]==5 and (populasi[i][k][3]==2 or populasi[i][k][3]==3):
										#cek prioritas
										if populasi[i][j][5] > populasi[i][k][5]:
											populasi[i][k][2] = random.randint(populasi[i][k][2]-30,populasi[i][k][2]+30)
										else:
											populasi[i][j][2] = random.randint(populasi[i][j][2]-30,populasi[i][j][2]+30)
									elif populasi[i][j][2]==6:
										#cek prioritas
										if populasi[i][j][5] > populasi[i][k][5]:
											populasi[i][k][2] = random.randint(populasi[i][k][2]-30,populasi[i][k][2]+30)
										else:
											populasi[i][j][2] = random.randint(populasi[i][j][2]-30,populasi[i][j][2]+30)
							
					#print("sesudah termutasi\n")
					#print(offspring[i])
			populasi=offspring
			#print("Generasi ini:", generasi_ini)
		
		#individu_terbaik
		simpan_fitness=[]
		fitness_terbaik=0
		individu_terbaik=[]
		for i in range(jumlah_individu):
			fitness=0
			skor = 0
			for j in range(jumlah_proker):   
				for k in range(j+1,jumlah_proker):
					#print("indeks ",j,"dibanding dengan indeks ", k)
					#cek tanggal
					if populasi[i][j][2] == populasi[i][k][2]:
						#cek target
						if populasi[i][j][4]==3 and populasi[i][k][4]==3:
							#cek waktu       
							if populasi[i][j][3] == populasi[i][k][3]:                            
								fitness+=0
							elif populasi[i][j][3]==4 and (populasi[i][k][3]==1 or populasi[i][k][3]==2):
								fitness+=0
							elif populasi[i][j][3]==5 and (populasi[i][k][3]==2 or populasi[i][k][3]==3):
								fitness+=0
							elif populasi[i][j][3]==6:
								fitness+=0
							else:
								fitness+=1
						else:
							fitness+=1
					else:
						fitness+=1
					
			if fitness>fitness_terbaik:
				fitness_terbaik=fitness
				individu_terbaik=i
				
			simpan_fitness.append(fitness)
			#print("individu ", i," skor fitness =", fitness)
		#print("sesudah:")
			
		for i in populasi[individu_terbaik]:
			id_org = str(i[1])
			id_kgn = str(i[0])
			waktu = str(i[3])
			target = str(i[4])
			tgl = dtm.strptime(str(i[2]),'%y%j')
			tglnew = dtm.strftime(tgl,'%Y-%m-%d')
			#print(tglnew)
			q = db.engine.execute("SELECT nama_kgn FROM kegiatan WHERE id_kgn=%s",i[0])
			for x in q:
				nama_kgn=x.nama_kgn
			#s = db.engine.execute("INSERT INTO jadwal (id_org,id_kgn,nama_kgn,tanggal,waktu,target) VALUES (%s,%s,%s,%s,%s,%s)",(id_org,id_kgn,nama_kgn,tglnew,waktu,target))
			#print(tgl)
			#print("organisasi",i[0],"pada hari ke",i[1],"waktu:",i[2],"target:",i[3],"prioritas",i[4],"id kegiatan",i[5])

		#print("individu terbaik adalah ", populasi[individu_terbaik],"dengan fittnes ", fitness_terbaik)
		#print("proses selesai")
		return redirect(url_for('dashboardadmin'))
		
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/dashboardorg/<int:id_org>")
def dashboardorg(id_org):
	if 'username' in session:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
		data_org = ''
		for i in r:
			data_org = i
			id_org = data_org.id_user
			nama_org = data_org.nama
			foto = data_org.foto
		rv = db.engine.execute("SELECT jadwal.id_kgn,kegiatan.nama_kgn,jadwal.tanggal,jadwal.id_org FROM kegiatan INNER JOIN jadwal ON jadwal.id_kgn=kegiatan.id_kgn")
		dataJson = []
		for result in rv:
			id_kgn = result[0]
			nama = result[1]
			tanggal = result[2]
			harike = tanggal.strftime('%j')
			
			tglstr = dtm.strftime(tanggal,'%d')
			blnstr = dtm.strftime(tanggal,'%m')
			thstr = dtm.strftime(tanggal,'%Y')
			tgl = int(tglstr)
			bln = int(blnstr)
			th = int(thstr)
			date = str(th) +','+ str(bln) +','+ str(tgl)

			id_user=result[3]
			if id_user == 2:
				warna = "blue"
			elif id_user == 3:
				warna = "darkblue"
			elif id_user == 4:
				warna = "black"
			elif id_user == 5:
				warna = "green"
			elif id_user == 6:
				warna = "darkred"
			elif id_user == 7:
				warna = "red"
			elif id_user == 8:
				warna = "chocolate"
			elif id_user == 9:
				warna = "orange"
			elif id_user == 10:
				warna = "brown"
			elif id_user == 11:
				warna = "darkgreen"
			elif id_user == 12:
				warna = "dodgerblue"
			else:
				warna = "gray"
			content = {
				"title":nama,
				"id_kgn":id_kgn,
				"start":date,
				"backgroundColor":warna,
				"borderColor":warna
			}
			#conten = json.codecs.decode(content,encoding='utf-8')
			dataJson.append(content)
			content = {}
		return render_template('org_dashboard.html', id_org=id_org, nama=nama_org, foto=foto, dataJson=dataJson)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/profileorg/<int:id_org>")
def profileorg(id_org):
	if'username' in session:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
		data_org = ''
		for i in r:
			data_org = i
			session['username']=data_org.username
			id_org=data_org.id_user
			foto_org=data_org.foto
			nama=data_org.nama
			email=data_org.email
			nomor=data_org.nomor
			username=data_org.username
			password=data_org.password
			return render_template('org_profile.html',id_org=id_org, username=username, password=password, foto=foto_org, nama=nama, nomor=nomor, email=email)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/editprofileorg/<int:id_org>",methods=['POST','GET'])
def editprofileorg(id_org):
	if'username' in session:
		if request.method == 'POST':
			r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
			data_org = ''
			for i in r:
				data_org = i
				session['username']=data_org.username
				passwd=data_org.password
			nama = request.form['nama']
			nomor = request.form['nomor']
			L = list(nomor)
			if L[0] == '0':
				L[0]='62'
				nomor = "".join(L)
			email = request.form['email']
			foto = request.files['foto']
			username = request.form['username']
			newpassword = request.form['newpassword']
			newpass = request.form['newpass']
			passw = request.form['password']
			if passw == passwd:
				if newpassword !='':
					if newpass == newpassword:
						passw = newpass
						if foto and allowed_file(foto.filename):
							filename = secure_filename(foto.filename)
							foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
							r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, foto=%s, username=%s, password=%s WHERE id_user=%s",(nama,nomor,email,foto.filename,username,passw,id_org))
							flash('Profil berhasil diubah', 'success')
							s = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
							data_org = ''
							for i in s:
								data_org = i
								session['username']=data_org.username
								foto_org=data_org.foto
								nama=data_org.nama
								email=data_org.email
								nomor=data_org.nomor
								username=data_org.username
							return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
						else:
							r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s,  username=%s, password=%s WHERE id_user=%s",(nama,nomor,email,username,passw,id_org))
							flash('Profil berhasil diubah', 'success')
							s = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
							data_org = ''
							for i in s:
								data_org = i
								session['username']=data_org.username
								foto_org=data_org.foto
								nama=data_org.nama
								email=data_org.email
								nomor=data_org.nomor
								username=data_org.username
							return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
					else:
						flash('Password baru yang anda masukkan tidak sesuai','warning')
						s = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
						data_org = ''
						for i in s:
							data_org = i
							session['username']=data_org.username
							foto_org=data_org.foto
							nama=data_org.nama
							email=data_org.email
							nomor=data_org.nomor
							username=data_org.username
						return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
				else:
					if foto and allowed_file(foto.filename):
						filename = secure_filename(foto.filename)
						foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, foto=%s, username=%s WHERE id_user=%s",(nama,nomor,email,foto.filename,username,id_org))
						flash('Profil berhasil diubah', 'success')
						s = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
						data_org = ''
						for i in s:
							data_org = i
							session['username']=data_org.username
							foto_org=data_org.foto
							nama=data_org.nama
							email=data_org.email
							nomor=data_org.nomor
							username=data_org.username
						return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
					else:
						r = db.engine.execute("UPDATE user SET nama=%s, nomor=%s, email=%s, username=%s WHERE id_user=%s",(nama,nomor,email,username,id_org))
						flash('Profil berhasil diubah', 'success')
						s = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
						data_org = ''
						for i in s:
							data_org = i
							session['username']=data_org.username
							foto_org=data_org.foto
							nama=data_org.nama
							email=data_org.email
							nomor=data_org.nomor
							username=data_org.username
						return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
			else:
				flash('Profil tidak dapat diubah karena password yang anda masukkan salah', 'warning')
				r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
				data_org = ''
				for i in r:
					data_org = i
					session['username']=data_org.username
					foto_org=data_org.foto
					nama=data_org.nama
					email=data_org.email
					nomor=data_org.nomor
					username=data_org.username
				return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
				#return redirect(url_for('editprofileorg/'+format(id_org)))
		else:
			r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
			data_org = ''
			for i in r:
				data_org = i
				session['username']=data_org.username
				foto_org=data_org.foto
				nama=data_org.nama
				email=data_org.email
				nomor=data_org.nomor
				username=data_org.username
			return render_template('org_editprofile.html',id_org=id_org,foto=foto_org,nama=nama,email=email,nomor=nomor,username=username)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/isikegiatan/<int:id_org>", methods=['POST', 'GET'])
def isikegiatan(id_org):
	if'username' in session:
		if request.method == 'POST':
			nama = request.form['nama']
			desc = request.form['desc']
			tanggal = request.form['tanggal']
			waktustr = request.form['waktu']
			waktu = int(waktustr)
			targetstr = request.form['target']
			target = int(targetstr)
			huruf = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
			q = db.engine.execute("SELECT * FROM kegiatan WHERE id_user=%s",id_org)
			jumlah = sum([1 for row in q])
			id_kgn = format(id_org)+huruf[id_org-2]+format(jumlah+1)

			#convtgl = dtm.strptime(tanggal,'%d/%m/%Y')
			tglnew = dtm.strptime(tanggal,'%Y-%m-%d')
			tglstr = dtm.strftime(tglnew,'%d')
			tgl = int(tglstr)
			if id_org == 2:
				if tgl <= 10:
					prioritas = 1
				elif tgl > 10 and tgl <= 20:
					prioritas = 6
				else:
					prioritas = 11
			elif id_org == 3:
				if tgl <= 10:
					prioritas = 2
				elif tgl > 10 and tgl <= 20:
					prioritas = 7
				else:
					prioritas = 12
			elif id_org == 4:
				if tgl <= 10:
					prioritas = 12
				elif tgl > 10 and tgl <= 20:
					prioritas = 1
				else:
					prioritas = 10
			elif id_org == 5:
				if tgl <= 10:
					prioritas = 11
				elif tgl > 10 and tgl <= 20:
					prioritas = 2
				else:
					prioritas = 9
			elif id_org == 6:
				if tgl <= 10:
					prioritas = 10
				elif tgl > 10 and tgl <= 20:
					prioritas = 3
				else:
					prioritas = 8
			elif id_org == 7:
				if tgl <= 10:
					prioritas = 9
				elif tgl > 10 and tgl <= 20:
					prioritas = 4
				else:
					prioritas = 7
			elif id_org == 8:
				if tgl <= 10:
					prioritas = 8
				elif tgl > 10 and tgl <= 20:
					prioritas = 5
				else:
					prioritas = 6
			elif id_org == 9:
				if tgl <= 10:
					prioritas = 7
				elif tgl > 10 and tgl <= 20:
					prioritas = 12
				else:
					prioritas = 1
			elif id_org == 10:
				if tgl <= 10:
					prioritas = 6
				elif tgl > 10 and tgl <= 20:
					prioritas = 11
				else:
					prioritas = 2
			elif id_org == 11:
				if tgl <= 10:
					prioritas = 5
				elif tgl > 10 and tgl <= 20:
					prioritas = 10
				else:
					prioritas = 3
			elif id_org == 12:
				if tgl <= 10:
					prioritas = 4
				elif tgl > 10 and tgl <= 20:
					prioritas = 9
				else:
					prioritas = 4
			elif id_org == 13:
				if tgl <= 10:
					prioritas = 3
				elif tgl > 10 and tgl <= 20:
					prioritas = 8
				else:
					prioritas = 5
			p = db.engine.execute("INSERT INTO kegiatan (id_kgn,nama_kgn,deskripsi,tanggal,waktu,target,prioritas,id_user) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(id_kgn,nama,desc,tanggal,waktu,target,prioritas,id_org))
			r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
			s = db.engine.execute("SELECT * FROM kegiatan WHERE id_user=%s ORDER BY %s",(id_org,tanggal))
			data_org = ''
			for i in r:
				data_org = i
				id_org = data_org.id_user
				nama = data_org.nama
				foto = data_org.foto
			return render_template('org_isikegiatan.html', s=s, id_org=id_org, nama=nama, foto=foto)
		else:
			r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
			s = db.engine.execute("SELECT * FROM kegiatan WHERE id_user=%s",id_org)
			data_org = ''
			for i in r:
				data_org = i
				id_org = data_org.id_user
				nama = data_org.nama
				foto = data_org.foto
			return render_template('org_isikegiatan.html', s=s, id_org=id_org, nama=nama, foto=foto)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

@app.route("/jadwalorg/<int:id_org>")
def jadwalorg(id_org):
	if'username' in session:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=%s",id_org)
		data_org = ''
		for i in r:
			data_org = i
			id_org = data_org.id_user
			nama_org = data_org.nama
			foto = data_org.foto
		rv = db.engine.execute("SELECT jadwal.id_kgn,kegiatan.nama_kgn,jadwal.tanggal,jadwal.id_org FROM jadwal INNER JOIN kegiatan ON kegiatan.id_kgn=jadwal.id_kgn WHERE jadwal.id_org=%s",id_org)
		dataJson = []
		for result in rv:
			id_kgn = result[0]
			nama = result[1]
			tanggal = result[2]
			harike = tanggal.strftime('%j')
			
			tglstr = dtm.strftime(tanggal,'%d')
			blnstr = dtm.strftime(tanggal,'%m')
			thstr = dtm.strftime(tanggal,'%Y')
			tgl = int(tglstr)
			bln = int(blnstr)
			th = int(thstr)
			date = str(th) +','+ str(bln) +','+ str(tgl)

			id_user=result[3]
			if id_user == 2:
				warna = "blue"
			elif id_user == 3:
				warna = "darkblue"
			elif id_user == 4:
				warna = "black"
			elif id_user == 5:
				warna = "green"
			elif id_user == 6:
				warna = "darkred"
			elif id_user == 7:
				warna = "red"
			elif id_user == 8:
				warna = "chocolate"
			elif id_user == 9:
				warna = "orange"
			elif id_user == 10:
				warna = "brown"
			elif id_user == 11:
				warna = "darkgreen"
			elif id_user == 12:
				warna = "dodgerblue"
			else:
				warna = "gray"
			content = {
				"title":nama,
				"id_kgn":id_kgn,
				"start":date,
				"backgroundColor":warna,
				"borderColor":warna
			}
			dataJson.append(content)
			#content = {}
		return render_template('org_jadwal.html', id_org=id_org, nama=nama_org, foto=foto, dataJson=dataJson)
	else:
		r = db.engine.execute("SELECT * FROM user WHERE id_user=1")
		data_user =''
		for i in r:
			data_user = i
			kontak=data_user.nomor
			email=data_user.email
			return render_template('index.html',kontak=kontak, email=email)

if __name__=='__main__':
	# app.secret_key = os.urandom(12)
	app.run(debug=True)
