from http.server import SimpleHTTPRequestHandler
import time

class CachingRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'max-age=315360000')  # 캐싱을 10년으로 설정
        self.send_header('Expires', time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time() + 315360000)))  # 만료 시간 설정
        super().end_headers()

# 서버 실행
if __name__ == '__main__':
    from http.server import HTTPServer

    server_address = ("", 8000)  # 원하는 포트 번호로 변경
    httpd = HTTPServer(server_address, CachingRequestHandler)
    httpd.serve_forever()
