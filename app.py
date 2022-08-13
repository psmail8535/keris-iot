from flask import Flask, request, render_template
from flask import jsonify
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
import psycopg2
from psycopg2.extras import RealDictCursor

def db_connect():
	con = psycopg2.connect(
	   database="d1prm2aq0rume1", user='hbvnkkcfmloojy'
	   , password='33a85551bf829bcecfb06b8f6ca80c2953a17deba76f1c5c04a7cd198a49048a'
	   , host='ec2-44-205-41-76.compute-1.amazonaws.com'
	   , port= '5432'
	   , sslmode='require'
	   ,connect_timeout=1024
	)
	return con
	
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/json_data')
def json_data():
	conn = db_connect()
	# ~ cur = con.cursor() 
	strQuery = "select * from keris_iot.v_data2;"
	
	print('strQuery: ',strQuery)
	cur = conn.cursor(cursor_factory=RealDictCursor)
	cur.execute(strQuery)
	data_sensor = cur.fetchall()

	# ~ print('data_sensor: ', data_sensor)
	count = len(data_sensor)
	# ~ print('count data_sensor: ', data_sensor)
	cur.close()
	conn.close()

	# ~ print('data: ', data_sensor  )
	return jsonify({'data': data_sensor}), 200


@app.route('/get_data_aktuator/', methods=['GET']) 
def get_data_aktuator():
	# ~ a = request.args.get('a')
	# ~ b = request.args.get('b')
	con = db_connect()
	cur = con.cursor()
	
	query = "select da.data_setup , da.data_hardware  from keris_iot.data_aktuator da \
			where da.id_aktuators = 1 and da.kd_sts_aktif = '1';;"  #% (a) 
	cur.execute(query)
	listdata = cur.fetchall()
	con.commit()
	# ~ print(listdata)
	# ~ print('type(listdata): ', type(listdata))
	
	sts_akt_setup = listdata[0][0]
	sts_akt_hardware = listdata[0][1]
	
	# ~ print('a: ', a)
	# ~ print('b: ', b)
	return jsonify({'setup': sts_akt_setup,'hardware':sts_akt_hardware}), 200




@app.route('/kontrol_aktuator/', methods=['GET']) 
def kontrol_aktuator():
	a = request.args.get('a')
	# ~ b = request.args.get('b')
	con = db_connect()
	cur = con.cursor()
	
	query = "UPDATE keris_iot.data_aktuator \
	SET  data_setup=%s \
	WHERE id_aktuators=1;" % (a) 
	cur.execute(query)
	con.commit()
	# ~ query = "update data_aktuator set status_aktuator='%s' where id_data=2" % (b)
	# ~ cur.execute(query)
	# ~ con.commit()
	
	print('a: ', a)
	# ~ print('b: ', b)
	return jsonify(hasil='Update status aktuator berhasil..'), 200


@app.route('/iot_get/', methods=['GET']) # ?suhu=27.0&hum=56.9
def iot_get():                    
	suhu=request.args.get('suhu')
	hum=request.args.get('hum')
	humsoil=request.args.get('hums')
	akt1Hardware = request.args.get('akt1')
	
	print('suhu: ', suhu)
	print('Kelembapan: ', hum)
	print('humsoil: ', humsoil)
	print('akt1Hardware: ', akt1Hardware)
	con = db_connect()
	cur = con.cursor() 

	query = "insert into keris_iot.data_sensor(id_sensor, data) values(1,'%s')" % (humsoil)
	print('query: ',query)
	cur.execute(query)
	con.commit()
	# ~ print('Simpan data ke database berhasil\n')
	
	query = "insert into keris_iot.data_sensor(id_sensor, data) values(2,'%s')" % (suhu)
	print('query: ',query)
	cur.execute(query)
	con.commit()
	# ~ print('Simpan data ke database berhasil\n')
	
	
	query = "insert into keris_iot.data_sensor(id_sensor, data) values(3,'%s')" % (hum)	
	print('query: ',query)
	cur.execute(query)
	con.commit()
	print('Simpan data ke database berhasil\n')
	
	
	query = "UPDATE keris_iot.data_aktuator \
			SET   data_hardware ='%s' where id_aktuators = 1; " % akt1Hardware
	cur.execute(query)
	con.commit()
	
	
	print('-----------------------------------------------------')
	query = 'select count(t1.id_sensor) as jml_data from keris_iot.data_sensor t1;'
	cur.execute(query)
	listdata = cur.fetchall()
	con.commit()
	# ~ print(listdata)
	# ~ print('type(listdata): ', type(listdata))	
	jml_data = int(listdata[0][0])
	
	print('jml_data: ', jml_data)
	if jml_data >= 45:
		query = "DELETE FROM keris_iot.data_sensor \
			WHERE id_data_sensor = any (array( \
			SELECT t1.id_data_sensor FROM keris_iot.data_sensor t1 \
			ORDER BY t1.timestamps desc LIMIT 12));"
		cur.execute(query)
		con.commit()
		print('DELETE data database berhasil\n')
	
	print('-----------------------------------------------------')
	query = "SELECT t1.data_setup FROM keris_iot.data_aktuator t1 \
			WHERE t1.id_data_aktuator=1 and t1.kd_sts_aktif='1';;"
	cur.execute(query)
	listdata = cur.fetchall()
	con.commit()
	# ~ print(listdata)
	# ~ print('type(listdata): ', type(listdata))
	
	sts_akt_1 = listdata[0]
	# ~ sts_akt_2 = listdata[1]
	
	print('sts_akt_1: ', sts_akt_1[0])
	# ~ print('sts_akt_2: ', sts_akt_2[0])
	return jsonify({"msg": 'berhasil', 'akt1':sts_akt_1[0]}), 200    
	# ~ return jsonify({"msg": 'berhasil'}), 200    
    

if __name__ == '__main__':
    WSGIRequestHandler.wbufsize = -1        
    app.run()
