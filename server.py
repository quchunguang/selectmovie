# -*- encoding: utf-8 -*-
'''
python server.py
'''
import BaseHTTPServer
import CGIHTTPServer
import cgitb


def main():
    cgitb.enable()  # This line enables CGI error reporting
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_address = ("", 8005)
    handler.cgi_directories = ["/"]

    httpd = server(server_address, handler)
    print "http://localhost:8005/movie.py"
    httpd.serve_forever()


if __name__ == '__main__':
    main()
