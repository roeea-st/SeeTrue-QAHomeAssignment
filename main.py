import gc
import os
import time
from classes import App, KnifeDetector, PistolDetector, BombDetector
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread, Lock, Event
import resource
import sys

gc.disable()

MAX_MEM_MB = 20000000000
resource.setrlimit(resource.RLIMIT_AS, (MAX_MEM_MB, MAX_MEM_MB))


def start_http_server(app, exit_event):
    class ServerHandler(BaseHTTPRequestHandler):
        lock = Lock()
        is_print = True
        def do_GET(self):
            try:
                if self.path == '/screened_bags_amount':
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(str(app.get_screened_bags_amount()).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                with ServerHandler.lock:
                    if ServerHandler.is_print:
                        print_menu()
            except MemoryError:
                with ServerHandler.lock:
                    #print('Exception Occurred: "MemoryError"')
                    print('Exception Occurred')
                    ServerHandler.is_print = False
                    exit_event.set()
            except Exception as e:
                print(f'Exception Occurred: "{e}"')

        def do_POST(self):
            try:
                if self.path == '/screen_next_bag':
                    app.screen_next_bag()
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
                with ServerHandler.lock:
                    if ServerHandler.is_print:
                        print_menu()
            except MemoryError:
                with ServerHandler.lock:
                    # print('Exception Occurred: "MemoryError"')
                    print('Exception Occurred')
                    ServerHandler.is_print = False
                    exit_event.set()
            except Exception as e:
                print(f'Exception Occurred: "{e}"')

    host = '127.0.0.1'
    port = 8000
    server = ThreadingHTTPServer((host, port), ServerHandler)
    server.serve_forever()


def print_menu():
    os.system('clear')
    menu_message = f'''
[HTTP Server running on http://127.0.0.1:8000]

Please choose and enter one of the following options:
1 - Send Next Bag to Screening
2 - Get Amount of Screened Bags So Far
3 - Exit App
'''
    print(menu_message)

def simulate():

    if getattr(sys, 'frozen', False):
        bag_image_dir = sys._MEIPASS
    else:
        bag_image_dir = '.'

    app = App(bag_image_dir)
    app.add_detector('knife', KnifeDetector())
    app.add_detector('pistol', PistolDetector())
    app.add_detector('bomb', BombDetector())

    exit_event = Event()
    server_thread = Thread(target=start_http_server, args=(app, exit_event), daemon=True)
    server_thread.start()

    os.environ['TERM'] = 'xterm'

    while not exit_event.is_set():
        print_menu()
        command = input()
        if exit_event.is_set():
            break
        if command == '1':
            app.screen_next_bag()
            print('Next Bag Sent.')
        elif command == '2':
            print(f'Amount of Screened Bags: { app.get_screened_bags_amount()}')
        elif command == '3':
            exit_event.set()
        else:
            print('Invalid Input')
        time.sleep(2)


if __name__ == "__main__":
    try:
        simulate()
    except Exception as e:
        print(f'Exception Occured: "{e}"')
    print('App Exited.')

