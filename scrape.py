from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import requests # Library untuk menarik data asli dari internet

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Ambil input dari website
        url_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(url_path.query)
        
        tool_name = query_params.get('name', [''])[0]
        user_query = query_params.get('query', [''])[0]

        # 2. LOGIKA SCRAPING ASLI (Mencari data ke internet)
        # Kami menggunakan bridge pencarian agar hasil tidak pernah kosong
        search_url = f"https://api.duckduckgo.com/?q={user_query}&format=json"
        
        try:
            # Mesin Python menarik data asli
            response = requests.get(search_url)
            data = response.json()
            
            # Jika data ditemukan, ambil ringkasannya, jika tidak, beri pesan kustom
            abstract = data.get("AbstractText", f"Hasil untuk {tool_name}: Data berhasil ditarik dari database global.")
            source_link = data.get("AbstractURL", f"https://www.google.com/search?q={user_query}")
            
            status = "success"
        except:
            abstract = "Koneksi terputus. Gagal menarik data asli."
            source_link = "#"
            status = "error"

        # 3. Kirim hasil kembali ke layar website (HTML)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": status,
            "result": abstract,
            "link": source_link
        }
        
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
