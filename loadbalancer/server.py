from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import plyvel
import json

db = plyvel.DB('/home/node1/Desktop/DBs/db3', create_if_missing=True)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        # Parse the query string. The second argument to parse_qs sets 'keep_blank_values' to True.
        query_components = urllib.parse.parse_qs(parsed_path.query, keep_blank_values=True)
        print("Query Components:", query_components)  # Debugging output

        if parsed_path.path == '/list':  # List all key-value pairs
            self.list_all_keys()
        # Fetching a specific key's value
        elif query_components:
            # Extract the first key found in the query string
            key = next(iter(query_components), None)
            if key:
                db_value = db.get(key.encode())
                response = {key: db_value.decode() if db_value else None}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(400, "Bad Request: No key provided")
                self.end_headers()
        else:
            self.send_error(400, "Bad Request")
            self.end_headers()




    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_components = urllib.parse.parse_qs(parsed_path.query)
        if query_components:
            key, values = next(iter(query_components.items()))  # Gets the first key-value pair
            value = values[0]
            db.put(key.encode(), value.encode())
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Data stored successfully'}).encode())
        else:
            self.send_error(400, 'Bad Request')
            self.end_headers()

    def list_all_keys(self):
        all_data = {key.decode(): value.decode() for key, value in db.iterator()}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(all_data).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
