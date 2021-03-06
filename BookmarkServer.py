#!/usr/bin/env python3
#
# A *bookmark server* or URI shortener.

# Import the python http.server librar/module - For creating Web Servers - That can listen and respond to
# incoming HTTP request/Traffic on a port over the internet
import http.server

# Import the python request module - Creating programs that acts like a client - making HTTP requests
import requests

# Import the python urllib module - Used for performing various tasks on HTTP Request urls
from urllib.parse import unquote, parse_qs

# Import the python os environment library(dictionary) - Which have access to all environment variables
import os

# Import threading module - Overrides the "http.server.HTTPServer" class inability to handle more than one task. 
# Implements Concurrency - Ability to handle two ongoing tasks at same time.
import threading
from socketserver import ThreadingMixIn

# ThreadHTTPServer class
class ThreadHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."

# Creating a memory for the server - Stores the users message through the HTTP POST verb/method
memory = {}

# Creating the HTML form code snippet - Requested with the HTTP GET method as the root page
form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
<form method="POST">
    <label>Long URI:
        <input name="longuri">
    </label>
    <br>
    <label>Short name:
        <input name="shortname">
    </label>
    <br>
    <button type="submit">Save it!</button>
</form>
<p>URIs I know about:
<pre>
{}
</pre>
'''

# Creates a function to check if the URI entered by the user is valid - It uses the requests module
# To send a GET request to the server(uri) under the hood to validate the entered URI
def CheckURI(uri, timeout=5):
    '''Check whether this URI is reachable, i.e. does it return a 200 OK?

    This function returns True if a GET request to uri returns a 200 OK, and
    False if that GET request returns any other response, or doesn't return
    (i.e. times out).
    '''
    try:
        r = requests.get(uri, timeout=timeout)
        # If the GET request returns, was it a 200 OK?
        return r.status_code == 200
    except requests.RequestException:
        # If the GET request raised an exception, it's not OK.
        return False

# Creates a class to shorten the entered URI
class Shortener(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # A GET request will either be for / (the root path) or for /some-name.
        # Strip off the / and we have either empty string or a name.
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                # We know that name! Send a redirect to it.
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                # We don't know that name! Send a 404 error.
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(name).encode())
        else:
            # Root path. Send the form.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # List the known associations in the form.
            known = "\n".join("{} : {}".format(key, memory[key])
                              for key in sorted(memory.keys()))
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        # Decode the form data.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        # Check that the user submitted the form fields.
        if "longuri" not in params or "shortname" not in params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing form fields!".encode())
            return

        longuri = params["longuri"][0]
        shortname = params["shortname"][0]

        if CheckURI(longuri):
            # This URI is good!  Remember it under the specified name.
            memory[shortname] = longuri

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # Didn't successfully fetch the long URI.
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(
                "Couldn't fetch URI '{}'. Sorry!".format(longuri).encode())

#if __name__ == '__main__':
#    server_address = ('', 8000)
#    httpd = http.server.HTTPServer(server_address, Shortener)
#    httpd.serve_forever()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    # httpd = http.server.HTTPServer(server_address, Shortener)
    # Creates a threadHTTPServer instead - Implementing Concurrency
    httpd = ThreadHTTPServer(server_address, Shortener)
    httpd.serve_forever()

