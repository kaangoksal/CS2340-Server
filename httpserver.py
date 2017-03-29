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
from WaterAppCommands import WaterAppApi
import SocketServer
import ConfigParser

class S(BaseHTTPRequestHandler):

    RegisteredMethods = {}


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

        if self.RegisteredMethods.has_key(("post", self.path)):
            print "[DEBUG] Found the method: " + self.path
            functiontoUse = self.RegisteredMethods[("post", self.path)]
            functiontoUse(self.headers, self)
        else: #This means that such function does not exist in the server.
            print "[ERROR] Method Does not exists: " + self.path
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<html><body><h1>Wrong Api</h1></body></html>")

    # def print_debug(self):
    #     print self.path
    #     for content in self.headers:
    #         print "---------------------------------------"
    #         print "Header: " + content
    #         print type(content)
    #         print "\n"
    #         print "Content:" + self.headers[content]
    #         print type(self.headers[content])
    #         print "---------------------------------------"
    #         content_length = int(self.headers['Content-Length'])
    #         post_data = self.rfile.read(content_length)

class MainServer:

    registeredMethods = []

    def registerMethod(self, method, url, protocol):
        self.registeredMethods.append((protocol, url, method))

    def syncMethodsWithServerInstance(self, ServerClass):
        for methodTuple in self.registeredMethods:
            (Protocol, Url, Method) = methodTuple
            ServerClass.RegisteredMethods[(Protocol, Url)] = Method

    def run(self, server_class=HTTPServer, handler_class=S, port=80):
        server_address = ('', port)
        #S.postMethods = {'/login': WaterAppApi.handleLogin}
        self.syncMethodsWithServerInstance(handler_class)
        httpd = server_class(server_address, handler_class)
        print 'Starting httpd...'
        httpd.serve_forever()




if __name__ == "__main__":
    from sys import argv

    x = MainServer()
    #registering methods.
    x.registerMethod(WaterAppApi.handleLogin, "/login", "post")
    x.registerMethod(WaterAppApi.registerAccount, "/register", "post")
    x.registerMethod(WaterAppApi.addWaterReport, "/add_water_report", "post")
    x.registerMethod(WaterAppApi.editUser, "/edit_user", "post")
    x.registerMethod(WaterAppApi.test, "/test", "post")
    x.registerMethod(WaterAppApi.getWaterReports, "/get_water_reports", "post")
    x.registerMethod(WaterAppApi.getWaterPurityReports, "/get_water_purity_reports", "post")
    x.registerMethod(WaterAppApi.getWaterSourceReports, "/get_water_source_reports", "post")



    if len(argv) == 2:
        x.run(port=int(argv[1]))
    else:
        x.run()
