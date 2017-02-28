
import json
from pprint import pprint

class WaterAppApi():

    @staticmethod
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

    @staticmethod
    def registerAccount(Headers, datain):
        try:
            print "[DEBUG] - registerAccount: I'm handling it"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            print "email " + parsedJson["email"]
            print bcolors.OKBLUE +"password " + parsedJson["password"] + bcolors.ENDC

            datain._set_headers()
            datain.wfile.write("<html><body><h1>User Account Registered</h1></body></html>")
            print "DONE"

        except (KeyError):
            print "[ERROR] - registerAccount: Registeration failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Registration Failed</h1></body></html>")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'