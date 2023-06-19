import http.server
import socketserver


def run(port: int = 8084):
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", int(port)), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()
