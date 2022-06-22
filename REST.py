# Ali Shazaei
from flask import Flask, jsonify, request
from flask_restful import Resource,Api,reqparse
import os
from datetime import date
import re 

app = Flask(__name__)
api=Api(app)

class sms(Resource):
    def __init__(self) :
        self.username="ali"
        self.password="123"
    def post(self):
        parser =reqparse.RequestParser()
        parser.add_argument('message',required=True,type=str)
        parser.add_argument('username',required=True , type=str )
        parser.add_argument('password',required=True, type=str )
        parser.add_argument('phonenum',required=True , type=str)
        parser.add_argument('show',required=False , type=str)


        
        arguments= parser.parse_args()
        message = arguments['message']
        username = arguments['username']
        password = arguments['password']
        phonenum = arguments['phonenum']
        showarg = arguments['show']
        conf = open("/etc/smsd.conf" , "r" )
        for line in conf : 
            conf_user, conf_password=(re.search('(.+):(.+)' , line)).group(1,2)
       

            if username == conf_user and password == conf_password:
                if showarg == "True" and username == self.username and password == self.password: 
                    f=open("/var/log/smsd.log","r")
                    return f.read()

                try : 
                 os.popen("./sendsms {} \"{}\"".format(phonenum , message))
                except:
                    print("The send sms file not found or something wen wrong with that! ")
                    return {"status" : "Failure"}

                try : 
                    f= open("/var/log/smsd.log" , "a" )
                    f.write("{} , {} has send the message : {}  TO {} \n".format(date.today() , self.username , message , phonenum))
                    f.close()
                    return {"status" : "Success"}

                except:
                    print("something went wrong with log file")

           
        return {"status" : "Failure"} 


api.add_resource(sms,'/sms')

if __name__ == '__main__':  
    app.run(port='5000',host="0.0.0.0",debug = True)

  
