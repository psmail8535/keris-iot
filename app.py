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
    

@app.route('/iot_get/', methods=['GET']) # ?suhu=27.0&hum=56.9
def iot_get(): 
	'''                   
	suhu=request.args.get('suhu')
	hum=request.args.get('hum')
	print('suhu: ', suhu)
	print('Kelembapan: ', hum)
	con = db_connect()
	cur = con.cursor() 

	query = "insert into keris_iot.data_sensor(data) values('%s')" % (suhu)
	cur.execute(query)
	con.commit()
	print('Simpan data ke database berhasil\n')
	'''
	# ~ print('-----------------------------------------------------')
	# ~ query = 'select t1.status_aktuator from data_aktuator t1 order by t1.id_data;'
	# ~ cur.execute(query)
	# ~ listdata = cur.fetchall()
	# ~ con.commit()
	# ~ print(listdata)
	# ~ print('type(listdata): ', type(listdata))
	
	# ~ sts_akt_1 = listdata[0]
	# ~ sts_akt_2 = listdata[1]
	
	# ~ print('sts_akt_1: ', sts_akt_1[0])
	# ~ print('sts_akt_2: ', sts_akt_2[0])
	# ~ return jsonify({"msg": 'berhasil', 'akt1':sts_akt_1[0],  'akt2':sts_akt_2[0]}), 200    
	return jsonify({"msg": 'berhasil'}), 200    
    

if __name__ == '__main__':
    WSGIRequestHandler.wbufsize = -1        
    app.run()
