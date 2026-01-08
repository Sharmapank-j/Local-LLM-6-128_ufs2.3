from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json

LLAMA = "./build/bin/llama-cli"
MODEL = "models/model.gguf"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        data = json.loads(self.rfile.read(length))
        prompt = data.get("prompt", "")

        cmd = [
            LLAMA, "-m", MODEL, "-p", prompt,
            "--temp", "0.7", "--top-p", "0.9",
            "--repeat-penalty", "1.1", "--ctx-size", "2048"
        ]

        result = subprocess.run(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"response": result.stdout}).encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("API running on port 8000")
server.serve_forever()
