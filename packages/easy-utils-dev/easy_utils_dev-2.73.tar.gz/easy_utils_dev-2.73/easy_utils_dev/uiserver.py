from werkzeug.serving import ThreadedWSGIServer
from easy_utils_dev.utils import getRandomKey , generateToken
from flask_socketio import SocketIO
from engineio.async_drivers import gevent
from engineio.async_drivers import threading
from flask_cors import CORS
import logging ,  json
from flask import Flask , send_file
from threading import Thread
from easy_utils_dev.custom_env import cenv
from easy_utils_dev.utils import kill_thread
from multiprocessing import Process
from werkzeug.serving import make_ssl_devcert


def getClassById( id ) :
    return cenv[id]

def create_ssl(host,output) :
    '''
    host : is the IP/Adress of the server which servers the web-server
    output: the output locaiton to generate the ssl certificate. it should end with filename without extension
    '''
    return make_ssl_devcert( output , host=host)
    

class UISERVER :
    def __init__(self ,
                 id=getRandomKey(n=15),
                 secretkey=generateToken(),
                 address='localhost',
                 port=5312 , 
                 https=False , 
                 ssl_crt=None,
                 ssl_key=None,
                 template_folder='templates/' 
                   ,**kwargs
                ) -> None:
        self.id = id
        self.app = app = Flask(self.id , template_folder=template_folder)
        app.config['SECRET_KEY'] = secretkey
        CORS(app,resources={r"/*":{"origins":"*"}})
        self.address= address 
        self.port = port
        self.thread = None
        self.ssl_crt=ssl_crt
        self.ssl_key=ssl_key
        self.enable_test_url=True
        if https :
            self.httpProtocol = 'https'
        else :
            self.httpProtocol = 'http'
        self.socketio = SocketIO(app , cors_allowed_origins="*"  ,async_mode='threading' , engineio_logger=False , always_connect=True ,**kwargs )
        cenv[id] = self
        self.fullAddress = f"{self.httpProtocol}://{self.address}:{self.port}"

    def update_cert(self , crt, ssl ) :
        self.ssl_crt=crt
        self.ssl_key=ssl


    def getInstance(self) :
        return self.getFlask() , self.getSocketio() , self.getWsgi()
    
    def getSocketio( self ):
        return self.socketio
    
    def getFlask( self ):
        return self.app
    
    def getWsgi(self) :
        return self.wsgi_server

    def shutdownUi(self) :
        kill_thread(self.thread)
        self.wsgi_server.server_close()
        self.wsgi_server.shutdown()

    def thrStartUi(self) :
        if self.enable_test_url :
            print(f'TEST URL GET-METHOD /connection/test/internal')
            @self.app.route('/connection/test/internal' , methods=['GET'])
            def test_connection():
                return f"Status=200<br> ID={self.id}<br> one-time-token={getRandomKey(20)}"
        if self.httpProtocol == 'http' :
            con = None
        elif self.httpProtocol == 'https' :
            con=(self.ssl_crt , self.ssl_key)
        self.wsgi_server = wsgi_server = ThreadedWSGIServer(
            host = self.address ,
            ssl_context=con,
            # ssl_context=('ssl.crt', 'ssl.key'),
            port = self.port,
            app = self.app )
        print(f"web-socket: {self.fullAddress}")
        print(f"UI URL : {self.fullAddress}")
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        wsgi_server.serve_forever()
    
    def startUi(self ,daemon ) :
        self.thread = self.flaskprocess = Thread(target=self.thrStartUi)
        self.flaskprocess.daemon = daemon
        self.flaskprocess.start()
        return self.thread
    
    def stopUi(self) :
        kill_thread(self.thread)
        return True
    
