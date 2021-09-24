#  coding: utf-8 
import socketserver
import re
from time import gmtime, strftime
import time
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        data = re.split(r"[~\r\n]+", self.data.decode("utf-8"))
        for d in data:
            print (d)
        
        # variables change for different request
        length = 0
        status = '200 OK'
        ctype = "html"
        
        reqinfo = data[0].split()
        
        if reqinfo[0] != "GET":
        	status = '405 Method Not Allowed'
        
        if reqinfo[1][-1] == "/":
            reqinfo[1] = reqinfo[1]+ "index.html"
        else:
            if len(reqinfo[1].rsplit('.',1)) == 1:
                origin = reqinfo[1]+ "/"
                reqinfo[1] = reqinfo[1]+ "/index.html"
                status = "301 Moved Permanently"
            
        script_dir = "/home/yiyang/Desktop/CMPUT404-assignment-webserver/www"
        rel_path = reqinfo[1]
        abs_file_path = script_dir + rel_path
        ctype = reqinfo[1].rsplit('.',1)
        
        if len(ctype) > 1:
            ctype = ctype[1]
        else:
            status = "404 Not FOUND!"
        
        try:
            f = open (abs_file_path, "r")
        except FileNotFoundError:
            status = "404 Not FOUND!"
            
            self.request.send(bytearray(reqinfo[2] + " " + status + "\r\n",'utf-8'))
            if status == "301 Moved Permanently":
                self.request.send(bytearray("Location: http://127.0.0.1:8080/" + origin,'utf-8'))
            else:
                self.request.send(bytearray(time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()),'utf-8'))
                self.request.send(bytearray("Content-Length: " + str(length) + "\r\n",'utf-8'))
                self.request.send(bytearray("Connection: close\r\n",'utf-8'))
                self.request.send(bytearray("Content-Type: text/" +  ctype +"\r\n",'utf-8'))
                self.request.send(bytearray("\r\n",'utf-8'))
        else:
            
            l = f.read(1024)
            while (l):
                length += len(l)
                l = f.read(1024)
	
            self.request.send(bytearray(reqinfo[2] + " " + status + "\r\n",'utf-8'))
            self.request.send(bytearray(time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()),'utf-8'))
            self.request.send(bytearray("Content-Length: " + str(length) + "\r\n",'utf-8'))
            self.request.send(bytearray("Connection: close\r\n",'utf-8'))
            self.request.send(bytearray("Content-Type: text/" +  ctype +"\r\n",'utf-8'))
            self.request.send(bytearray("\r\n",'utf-8'))
        
            f = open (abs_file_path, "r")
            l = f.read(1024)
            while (l):
                self.request.send(bytearray(l,'utf-8'))
                l = f.read(1024)
        
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
