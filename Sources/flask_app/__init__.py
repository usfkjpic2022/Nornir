from flask import Flask, redirect
import threading, time

import http.server
import socketserver

class FlaskApp():
    def __init__(self, port: int = 8083, static_port: int = 8084, log_file: str = ""):
        self.app = Flask(__name__)
        self.running = False
        self.port = port
        self.static_port = static_port
        self.static_api = f"http://127.0.0.1:{static_port}/"
        self.log_file = log_file

        @self.app.route('/')
        def index():
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        @self.app.route('/log')
        def show_log():
            return redirect(self.static_api+"logs/"+self.log_file, code=301)

        @self.app.route('/server/terminate')
        def server_terminate():
            self.running = False
            return "Flask Server Thread is Terminated."

        @self.app.route('/Pyodide/<path:path>')
        def static_file(path):
            return redirect(self.static_api+"Pyodide/"+path, code=301)

        @self.app.route('/Starboard/<path:path>')
        def starboard_file(path):
            return redirect(self.static_api+"Starboard/"+path, code=301)

        @self.app.route('/JupyterLite/<path:path>')
        def jupyter_file(path):
            return redirect(self.static_api+"JupyterLite/"+path, code=301)

    def run_server(self):
        self.running = True
        self.app.run(port=self.port)

    def run_static_server(self):
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.static_port), Handler) as httpd:
            print("static serving at port", self.static_port)
            httpd.serve_forever()

    def run_app(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True 
        server_thread.start()
        static_thread = threading.Thread(target=self.run_static_server)
        static_thread.daemon = True 
        static_thread.start()

        while self.running:
            time.sleep(0)


if __name__ == '__main__':
    flaskapp = FlaskApp(port=8083, static_port=8084)
    flaskapp.run_app()
