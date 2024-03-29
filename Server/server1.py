import psutil
import time
import http.server
import socketserver
import os

def get_network_usage(interface='h1-eth0', interval=1, output_file='/home/mininet/proj/Network-Load-Balancer/Server/logging/log1.txt', status_file='/home/mininet/proj/Network-Load-Balancer/Server/status/status1.txt'):
    try:
        while True:
            # Get network usage statistics
            stats_before = psutil.net_io_counters(pernic=True)[interface]
            time.sleep(interval)
            stats_after = psutil.net_io_counters(pernic=True)[interface]

            # Calculate bytes per second
            bytes_per_second = stats_after.bytes_sent - stats_before.bytes_sent
            kb_per_second = bytes_per_second / 1024

            #link capacity
            link_capacity = 1
            
            # Link utilization percentage
            utilization_percentage = (bytes_per_second*8 / (link_capacity * 1000000)) * 100
            
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            # Print the result to the network usage file
            with open(output_file, 'a') as file_output:
                file_output.write(f'{current_time},{interface},{utilization_percentage:.2f}\n')

            # Update the status file based on the condition
            with open(status_file, 'w') as file_status:
                file_status.write(str(f"{utilization_percentage:.2f}"))

            # Log the result to the console
            #print(f'{interface} KB/s: {kb_per_second:.2f}')
    except KeyboardInterrupt:
        print("Exiting...")

def start_http_server(port=80, directory='/home/mininet/proj/Draft/Server/'):
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving files on port {port} from the directory {directory}")
        httpd.serve_forever()

# Example usage
if __name__ == "__main__":
    import threading

    # Start the network usage monitoring in a separate thread
    network_thread = threading.Thread(target=get_network_usage)
    network_thread.start()

    # Start the HTTP server in the main thread
    start_http_server()
