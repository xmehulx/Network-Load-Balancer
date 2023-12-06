#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import logging


# Configure logging
logging.basicConfig(filename='/home/mininet/proj/Network-Load-Balancer/lb.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

link_utils = [0,0,0]
#c = 0 

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def proxy_request(self):
#        global c
        # Set the target IP address and port
        target_host = "10.0.0.1"  # Replace with the actual IP address
        arr=['10.0.0.1','10.0.0.2','10.0.0.3', "10.0.0.4"]
        target_port = 80  # Server listening port
        
#        #RR   
#        target_url = f"http://{arr[c%2]}:{target_port}{self.path}"
#        c+=1
#        print(f"c:{c} Target server: {target_url}")

        # Build the target URL
        if (self.path=='/bigfile'):
            target_url = f"http://{arr[3]}:{target_port}{self.path}"
        else:
            for i in range(0,3):
                try:
                    filename = f"/home/mininet/proj/Network-Load-Balancer/Server/status/status{i+1}.txt"
                    with open(filename, 'r') as file:
                        # Read the decimal number from the file and convert it to float
                        link_util = float(file.read().strip())                   
                        link_utils[i] = link_util
            
                except FileNotFoundError:
                    print(f"File not found: {filename}")
                except ValueError:
                    print(f"Invalid data in {filename}. It should contain a single decimal number.")
            
            free_server = link_utils.index(min(link_utils))
            #print(f"free server is {free_server}")
            target_url = f"http://{arr[free_server]}:{target_port}{self.path}"
#                
#        print(link_utils)



#            with open('/home/mininet/proj/Network-Load-Balancer/Server/status/status1.txt', 'r') as status_file:
#                status_content = status_file.read().strip()
#                if (int(float(status_content)) < 600):
#                    target_url = f"http://{arr[0]}:{target_port}{self.path}"
#                else:
#                    with open('/home/mininet/proj/Network-Load-Balancer/Server/status/status2.txt', 'r') as status_file:
#                        status_content = status_file.read().strip()
#                        if status_content == '0':
#                            target_url = f"http://{arr[1]}:{target_port}{self.path}"
#                        else:
#                            target_url = f"http://{arr[2]}:{target_port}{self.path}"   

        try:
            # Log the incoming request
            logging.info(f"Incoming Request: {self.path} - {self.client_address[0]}")

            # Forward the request to the target server
            if self.headers.get('Content-Length'):
                content_length = int(self.headers['Content-Length'])
                request_data = self.rfile.read(content_length)
                response = requests.post(target_url, data=request_data, headers=dict(self.headers))
            else:
                response = requests.get(target_url, headers=dict(self.headers))

            # Log the response and the server that served the request
            logging.info(f"Response: {response.status_code} - Served by: {target_url}")

            # Send the response back to the client
            self.send_response(response.status_code)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()

            self.wfile.write(response.content)

        except Exception as e:
            # Log errors
            logging.error(f"Error: {str(e)}")

            # Send an error response back to the client
            self.send_error(500, "Error forwarding request to the target server")

    

if __name__ == "__main__":
    PORT = 80  # Change this to the desired port
    handler = ProxyHandler
    httpd = HTTPServer(("", PORT), handler)

    print("Proxy server running on port", PORT)
    logging.info("Proxy server running on port %d", PORT)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info("Proxy server stopped")
