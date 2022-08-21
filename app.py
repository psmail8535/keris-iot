from flask import Flask, request, render_template
from flask import jsonify
from werkzeug.serving import WSGIRequestHandler
import psycopg2
from psycopg2.extras import RealDictCursor
import json
# ~ https://keris-iot.herokuapp.com/


import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
topic = 'jember_super/in_topic'
topicSensor = 'jember_super/topic_sensor'
# ~ topic = 'outTopic'
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

isNewDataExists = True

def on_message(client, userdata, msg):
	global isNewDataExists
	print(f"MQTT Received `{msg.payload.decode()}` from `{msg.topic}` topic")
	
	
	json_dbl = msg.payload.decode().replace("'",'"')
	print('json_dbl: ', json_dbl)
	json_data = json.loads(json_dbl)
	
	print('type(msg.payload.decode()): ', type(msg.payload.decode()))
	
	print('str(msg.payload.decode()): ', str(msg.payload.decode()))
	print('kode: ',json_data["kode"])
	print('data: ',json_data["data"])

	if json_data["kode"] == '0': # data sensor kelembaban tanah
		con = db_connect()
		cur = con.cursor() 		
		query = "insert into keris_iot.data_sensor(id_sensor, data) values(1,'%s')" % json_data["data"]
		print('query: \n', query)
		cur.execute(query)
		con.commit()
		isNewDataExists = True
		print('isNewDataExists: ', isNewDataExists)
	elif json_data["kode"] == '1':	# kontrol client
		pass
	elif json_data["kode"] == '2': # data status aktuator pompa
		con = db_connect()
		cur = con.cursor() 		
		query = "UPDATE keris_iot.data_aktuator \
			SET   data_hardware ='%s' where id_aktuators = 1; " % json_data["data"]
		print('query: \n', query)
		cur.execute(query)
		con.commit()
	else:
		isNewDataExists = False
		
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def publish(client, data):
	msg_count = 0
	# ~ while True:
	# ~ time.sleep(3)
	# ~ print('Masukkan 0 atau 1: ')
	print('Kirim Mqtt')
	msg = data.replace("'", '"') # # input()
	# ~ msg = f"Server python Pesan: {msg_count}"
	# ~ msg = str(msg_count)
	result = client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to topic `{topic}`")
	else:
		print(f"Failed to send message to topic {topic}")
	# ~ msg_count += 1
	# ~ if msg_count > 30:
		# ~ msg_count = 0


# ~ def run():
client = connect_mqtt()
client.loop_start()
client.subscribe(topic)
client.on_message = on_message
# ~ publish(client)


def db_connect():
	con = psycopg2.connect(
	   database="d1prm2aq0rume1", user='hbvnkkcfmloojy'
	   , password='33a85551bf829bcecfb06b8f6ca80c2953a17deba76f1c5c04a7cd198a49048a'
	   , host='ec2-44-205-41-76.compute-1.amazonaws.com'
	   , port= '5432'
	   , sslmode='require'
	   , connect_timeout=5
	)
	return con
	
def db_connect2():
	con = psycopg2.connect(
	   database="iot", user='istiyadi'
	   , password='123456'
	   , host='localhost'
	   , port= '5432'
	   # ~ , sslmode='require'
	   , connect_timeout=5
	)
	return con

def count_data(p_id):	
	jml_data
	
	
	strQuery = "select count(*) as jml_data from keris_iot.v_data2;"
	
	print('strQuery: ',strQuery)
	cur = conn.cursor(cursor_factory=RealDictCursor)
	cur.execute(strQuery)
	data_sensor = cur.fetchall()

	# ~ print('data_sensor: ', data_sensor)
	count = len(data_sensor)
	# ~ print('count data_sensor: ', data_sensor)
	cur.close()
	conn.close()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/json_data')
def json_data():	
	global isNewDataExists
	conn = db_connect()
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
	isNewDataExists = False
	print('isNewDataExists: ', isNewDataExists  )
	return jsonify({'data': data_sensor}), 200


@app.route('/get_data_aktuator/', methods=['GET','POST']) 
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



@app.route('/kontrol_aktuator2/', methods=['POST','GET']) 
def kontrol_aktuator2():
	print('request.json: ', request.json)
	kode = request.json.get('kode')
	data = request.json.get('data')
	# ~ a = request.args.get('a')
	# ~ b = request.args.get('b')
	
	publish(client, str(request.json))
	
	con = db_connect()
	cur = con.cursor()
	
	query = "UPDATE keris_iot.data_aktuator \
	SET  data_setup=%s \
	WHERE id_aktuators=1;" % (data) 
	cur.execute(query)
	con.commit()
	# ~ query = "update data_aktuator set status_aktuator='%s' where id_data=2" % (b)
	# ~ cur.execute(query)
	# ~ con.commit()
	
	print('data: ', data)
	# ~ print('b: ', b)
	return jsonify(hasil='Update status aktuator berhasil..'), 200


@app.route('/kontrol_aktuator/', methods=['GET']) 
def kontrol_aktuator():
	a = request.args.get('a')
	# ~ b = request.args.get('b')
	
	publish(client, a)
	
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


@app.route('/is_exist_new_data', methods=['GET']) 
def is_exist_new_data():	
	global isNewDataExists
	strIsExistsNewData = '0'
	if isNewDataExists:
		strIsExistsNewData = '1'	
	
	print('strIsExistsNewData: ', strIsExistsNewData)
	return jsonify(new_data=strIsExistsNewData), 200

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
