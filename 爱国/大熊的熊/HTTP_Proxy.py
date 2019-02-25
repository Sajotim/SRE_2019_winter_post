import http.server
import urllib.request
import socketserver


class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(urllib.request.urlopen(self.path), self.wfile)


http_proxy = socketserver.TCPServer(('0.0.0.0', 23), Proxy)
http_proxy.serve_forever()
