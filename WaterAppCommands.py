"""
    Author: Kaan Goksal
    Version: 1.2
    Description: This code is for extending the functionality of the http server.
                 The WaterAppApi class includes functions which will be called by http server.
                 The code supports config files which is a huge upgrade, also the requests are
                 authenticated. It is a little more secure now...... maybe not....
"""




import sys
import json
import MySQLdb
import ConfigParser
import base64


class WaterAppApi():

    """
               This function returns configuration details
    """
    @staticmethod
    def readConfig(option):

        #try catch
        if option == "MySQL":
            Config = ConfigParser.ConfigParser()
            Config.read("config")
            MySQLhost = Config.get("MySQL Settings", "host")
            MySQLusername = Config.get("MySQL Settings", "username")
            MySQLpassword = Config.get("MySQL Settings", "password")
            database = Config.get("MySQL Settings", "database")
            return MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)
        else:
            return None

    """
           This function returns a MySQL connection, it reads the configuration file.
    """
    @staticmethod
    def mysql_connection():
        return WaterAppApi.readConfig("MySQL")
        # MySQLhost = "localhost"
        # MySQLusername = "python_backend"
        # MySQLpassword = "Secur1ty_1s_sexy"
        # database = "waterapp"
        # return MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)

    """
       This function handles login,

       http://localhost/login

       Body
       {
            "email" : "kaangoksal@groopapp.com",
            "password" : "cukasdfghjikubik",
            "token" : "",
            "username" : ""
       }
    """
    @staticmethod
    def handleLogin(Headers, datain):
        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]

        if WaterAppApi.authenticate(auth_string):
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Successful</h1></body></html>")
        else:
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Login Failed, Wrong Password</h1></body></html>")
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- handleLogin: Login failed"

    """
    This function registers an account,

    http://localhost/register

    Body
    {
        "email" : "kaangoksal@groopapp.com",
        "password" : "cukubik",
        "token" : "12311233",
        "username" : "kaangoksal"
    }

    """
    @staticmethod
    def registerAccount(Headers, datain):
        try:
            # print "[DEBUG] - registerAccount:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            Email = parsedJson["email"]
            Username = parsedJson["username"]
            Password = parsedJson["password"]
            Token = parsedJson["token"]

            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("SELECT email FROM users where email = \"%s\" " % Email)
            EmailDBResult = cursor.fetchone()
            cursor.execute("SELECT username FROM users where username = \"%s\" " % Username)
            UsernameDBResult = cursor.fetchone()

            if EmailDBResult == None and UsernameDBResult == None:
                print "[DEBUG] - registerAccount: Registering User"
                print "email " + parsedJson["email"]
                print "username " + parsedJson["username"]
                print bcolors.OKBLUE + "password " + parsedJson["password"] + bcolors.ENDC
                print "token " + parsedJson["token"]
                try:
                    cursor.execute("INSERT INTO users(email, username, password, token) VALUES \
        ('%s', '%s', '%s', '%s')" % (Email, Username, Password, Token))
                    DataBase.commit()
                    datain._set_headers()
                    datain.wfile.write("<html><body><h1>User Account Registered</h1></body></html>")
                    print "[DEBUG] - registerAccount: Account registered for "
                except:
                    DataBase.rollback()
                    print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- registerAccount: MySQL Commit Failed"
                DataBase.close()
            else:
                if EmailDBResult != None:
                    (EmailDBResult,) = EmailDBResult
                else:
                    EmailDBResult = "None"
                if UsernameDBResult != None:
                    (UsernameDBResult,) = UsernameDBResult
                else:
                    UsernameDBResult = "None"

                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- registerAccount: Registeration failed " + EmailDBResult + " " + UsernameDBResult
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Registration Failed</h1></body></html>")
                # username
                # password
                # email
                # account
                # type
                # token(to
                # send
                # push
                # notification)
                # created_at

        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- registerAccount: Registeration failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Registration Failed</h1></body></html>")

    @staticmethod
    def addWaterReport(Headers, datain):
        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]

        if WaterAppApi.authenticate(auth_string):
            try:
                # print "[DEBUG] - registerAccount:"
                content_length = int(datain.headers['Content-Length'])
                post_data = datain.rfile.read(content_length)
                parsedJson = json.loads(post_data)

                datetime = parsedJson["date"]
                report_number = parsedJson["report_number"]
                reporter = parsedJson["reporter"]
                location = parsedJson["location"]
                data = parsedJson["data"]
                print "[DEBUG] - AddWaterReport: datetime %s, reportnumber %s, reporter %s, location %s data %s " % (datetime,report_number, reporter, location,data)
                DataBase = WaterAppApi.mysql_connection()
                cursor = DataBase.cursor()

                cursor.execute("insert into reports (date, report_number, reporter, location, data) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                                   datetime, report_number, reporter, location, data))
                DataBase.commit()
                print "[DEBUG] - addWaterReport: Adding Water Report"
                print "date " + parsedJson["date"]
                print "report_number " + parsedJson["report_number"]
                print bcolors.OKBLUE + "reporter " + parsedJson["reporter"] + bcolors.ENDC
                print "location " + parsedJson["location"]
                print "data " + parsedJson["data"]

                datain._set_headers()
                datain.wfile.write("<html><body><h1>Report Added Successfully</h1></body></html>")
                print "[DEBUG] - AddWaterReport:Success "

            except Exception, e:
                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- AddWaterReport: Failed"
                print e
                datain._set_headers()
                datain.wfile.write("<html><body><h1>AddWaterReport Failed</h1></body></html>")
        else:
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- AddWaterReport: Authentication Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>AddWaterReport Failed</h1></body></html>")


    @staticmethod
    def getWaterReports(Headers, datain):
        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]

        if WaterAppApi.authenticate(auth_string):
            try:
                data_base = WaterAppApi.mysql_connection()
                cursor = data_base.cursor()
                cursor.execute("SELECT date, report_number, reporter, location, data from reports")
                data_get = cursor.fetchall()

                # print data_get
                # print str(type(data_get))
                data_base.commit()
                returnJsonList = []

                for report in data_get:

                    date = report[0]
                    report_number = report[1]
                    reporter = report[2]
                    location = report[3]
                    data = report[4]
                    dictlocal = {'report_number':report_number, 'date': str(date), 'reporter': reporter, 'location':location, 'data': data }
                    returnJsonList.append(dictlocal)

                    #returnJsonList.append(json.dumps({'report_number':report_number, 'date': date, 'reporter': reporter, 'location':location, 'data': data }))
                    # print "Report " + report_number
                    # print "date " + str(date)
                    # print "reporter " + reporter
                    # print "location " + location
                    # print "data " + data
                dictContainer = {'reports':returnJsonList}
                returnstring = json.dumps(dictContainer, sort_keys=True, indent=4, separators=(',', ': '))


                datain._set_headers()
                datain.wfile.write(returnstring)
                print "[DEBUG] - getWaterReport: Successful "


            except (KeyError):
                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- getWaterReport: Failed"
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Fetch waterreports Failed</h1></body></html>")
        else:
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- getWaterReport: Authentication Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Fetch waterreports Failed</h1></body></html>")


    @staticmethod
    def deleteWaterReport(Headers, datain):
        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]

        if WaterAppApi.authenticate(auth_string):
            try:
                print "[DEBUG] - deleteWaterReport:"
                content_length = int(datain.headers['Content-Length'])
                post_data = datain.rfile.read(content_length)
                parsedJson = json.loads(post_data)

                report_number = parsedJson["report_number"]

                DataBase = WaterAppApi.mysql_connection()
                cursor = DataBase.cursor()

                cursor.execute("SELECT date, report_number, reporter, location, data from reports")
                dataget = cursor.fetchone()
                DataBase.commit()

                print dataget

                # convert info to json and pass bietch


                datain._set_headers()
                datain.wfile.write("<html><body><h1>Here are the reports</h1></body></html>")
                print "[DEBUG] - deleteWaterReport: water report deleted "


            except (KeyError):
                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- deleteWaterReport: Failed"
                datain._set_headers()
                datain.wfile.write("<html><body><h1> delete water report failed</h1></body></html>")
        else:
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- deleteWaterReport: Authentication Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>delete water report failed</h1></body></html>")


    @staticmethod
    def editWaterReport(Headers, datain):
        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]

        if WaterAppApi.authenticate(auth_string):
            try:
                print "[DEBUG] - editWaterReport:"
                content_length = int(datain.headers['Content-Length'])
                post_data = datain.rfile.read(content_length)
                parsedJson = json.loads(post_data)

                datetime = parsedJson["date"]
                report_number = parsedJson["report_number"]
                reporter = parsedJson["reporter"]
                location = parsedJson["location"]
                data = parsedJson["data"]

                DataBase = WaterAppApi.mysql_connection()
                cursor = DataBase.cursor()

                cursor.execute(
                    "UPDATE reports set date= %s, reporter = %s, location = %s, data= %s where report_number = %s" % (
                    datetime, reporter, location, data, report_number))
                DataBase.commit()

                # convert info to json and pass bietch return the updated report

                datain._set_headers()
                datain.wfile.write("<html><body><h1>Here are the reports</h1></body></html>")
                print "[DEBUG] - editWaterReport: report edited "


            except (KeyError):
                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- editWaterReport: Failed"
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Fetch waterreports Failed</h1></body></html>")
        else:
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- editWaterReport: Authentication Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Fetch waterreports Failed</h1></body></html>")

    @staticmethod
    def editUser(Headers, datain):
        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]

        if WaterAppApi.authenticate(auth_string):
            try:
                print "[DEBUG] - editUser:"
                content_length = int(datain.headers['Content-Length'])
                post_data = datain.rfile.read(content_length)
                parsedJson = json.loads(post_data)

                username = parsedJson["username"]
                password = parsedJson["password"]
                email = parsedJson["email"]

                DataBase = WaterAppApi.mysql_connection()
                cursor = DataBase.cursor()

                cursor.execute("UPDATE users set username= \"%s\", password = \"%s\" where email = \"%s\"" % (
                username, password, email))
                DataBase.commit()

                # convert info to json and pass bietch return the updated report

                datain._set_headers()
                datain.wfile.write("<html><body><h1>Successful</h1></body></html>")
                print "[DEBUG] - editUser: user edited username = %s, email = %s" % (username, email)


            except (KeyError):
                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- editUser: Failed"
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Failed/h1></body></html>")
        else:
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- editUser: Authentication Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Failed/h1></body></html>")

    @staticmethod
    def test(Headers, datain):

        auth_string = Headers["Authorization"]
        auth_string = auth_string[auth_string.index(" ") + 1:]
        if WaterAppApi.authenticate(auth_string):
            print "success biach"
        else:
            print "authentication failed"

        print str(Headers.__class__)

        WaterAppApi.readConfig("config")
        print bcolors.OKGREEN + "[DEBUG]" + bcolors.ENDC + "- Test: Executed"
        datain._set_headers()
        datain.wfile.write("<html><body><h1>Test</h1></body></html>")

    @staticmethod
    def authenticate(credidental_base64):

        decoded_credidentals = base64.b64decode(credidental_base64)
        password = decoded_credidentals[decoded_credidentals.index(":") + 1:]
        email = decoded_credidentals[:decoded_credidentals.index(":")]

        data_base = WaterAppApi.mysql_connection()
        cursor = data_base.cursor()

        cursor.execute("SELECT password FROM users where email = \"%s\" " % email)
        db_password = cursor.fetchone()

        # db_password = ("pass",)


        if db_password != None:
            (db_password,) = db_password
            if db_password == password:

                return True
            else:
                print bcolors.WARNING + "[INFO] Authentication failed!" + bcolors.ENDC
                return False
        else:
            print bcolors.WARNING + "[INFO] Authentication failed!" + bcolors.ENDC
            return False




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
