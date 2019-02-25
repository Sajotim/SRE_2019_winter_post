#!/usr/bin/env python
# coding: utf-8
# from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib import request
import json

class Mhandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        res=request.urlopen(self.path)
        self.send_response(200)
        content_type=res.headers['Content-Type'].split(';')[0]
        self.send_header('Content-type',content_type)
        self.end_headers()
        self.wfile.write(res.read())
    def do_POST(self):
#         todo...

if __name__ == '__main__':
    host = ('localhost', 4000)
    server = HTTPServer(host, Mhandler)
    server.serve_forever()

