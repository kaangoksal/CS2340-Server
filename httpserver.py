#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

class S(BaseHTTPRequestHandler):

    postMethods = {}

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        Auth = "my code is secret"
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print self.path
        for content in self.headers:
            print "Header: " + content
            print type(content)
            print "---------------------------------------"
            print "Content:" + self.headers[content]
            print type(self.headers[content])
            print "---------------------------------------"
        functiontoUse = self.postMethods[self.path]
        functiontoUse(self.headers, self)
        # print "Here is the body " + post_data
        # try:
        #     if self.headers["authorization"] == Auth:
        #         self._set_headers()
        #         self.wfile.write("<html><body><h1>Authorized</h1></body></html>")
        #     else:
        #         self._set_headers()
        #         self.wfile.write("<html><body><h1>Authorization failed</h1></body></html>")
        # except (KeyError):
        #     self._set_headers()
        #     self.wfile.write("<html><body><h1>Authorization failed</h1></body></html>")


def handleLogin(Headers, self):
    Auth = "123"
    try:
        if Headers["authorization"] == Auth:
            self._set_headers()
            self.wfile.write("<html><body><h1>Authorized</h1></body></html>")
        else:
            self._set_headers()
            self.wfile.write("<html><body><h1>Authorization failed</h1></body></html>")
    except (KeyError):
        self._set_headers()
        self.wfile.write("<html><body><h1>Authorization failed</h1></body></html>")


        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    S.postMethods = {'/login': handleLogin}
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
