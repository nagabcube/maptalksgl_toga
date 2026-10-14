"""
Maptalks-GL tests with Toga
"""
import threading
import toga
import pathlib
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
# http-server for webView... 
from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        # Elmentjük a Toga-tól kapott mappa elérési utat
        self.target_dir = directory
        # Meghívjuk az eredeti Python osztály inicializálóját a megadott mappával
        super().__init__(*args, directory=str(self.target_dir), **kwargs)

def run_http_server(base_dir):
    server_address = ("localhost", 8000)
    
    # Itt adjuk át a MyHTTPHandler-nek az app gyökérmappáját
    httpd = HTTPServer(
        server_address, 
        lambda *args, **kwargs: MyHTTPHandler(*args, directory=base_dir, **kwargs)
    )
    print(f"A helyi statikus szerver fut a {base_dir} mappából...")
    httpd.serve_forever()

class Maptalks(toga.App):
    def startup(self):
        base_dir = toga.App.app.paths.app
    	# Http_Server thread
        threading.Thread(
            target=run_http_server,
            args=(base_dir,), 
            daemon=True
        ).start()
        
        # Toga window
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        # Wait server
        self.webview = toga.WebView(
            url="http://localhost:8000/map.html",
            style=Pack(flex=1)
        )

        main_box.add(self.webview)

        self.main_window = toga.MainWindow("Maptalks-GL Map")
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return Maptalks("Maptalks-GL Map", "org.beeware.maptalks")

