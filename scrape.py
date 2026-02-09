from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Ambil data dari URL
        url_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(url_path.query)
        
        tool_id = query_params.get('id', [''])[0]
        user_query = query_params.get('query', [''])[0]

        # 2. Logik Scraping (Contoh Ringkas)
        # Sila tambahkan library scraping anda di sini (seperti requests atau yt-dlp)
        result_text = f"Data untuk {user_query} berjaya diekstrak oleh Otak Python."
        result_link = f"https://www.google.com/search?q={user_query}" # Contoh link hasil

        # 3. Hantar Balasan ke HTML
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "result": result_text,
            "link": result_link
        }
        
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
