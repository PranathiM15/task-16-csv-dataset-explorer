from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import io
import csv
import pandas as pd
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", 8000
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CSV Atlas — Dataset Explorer</title>
<style>
:root{--ink:#17233f;--muted:#6d7890;--paper:#f5f7fb;--line:#e2e8f2;--blue:#2459e0;--cyan:#24b8c7;--orange:#ff8b45}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 90% 4%,#dff8f7 0,transparent 24%),radial-gradient(circle at 0% 0%,#e8edff 0,transparent 27%),var(--paper);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink)}
header{height:76px;padding:0 clamp(18px,5vw,76px);display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #e7ebf3;background:#ffffffc9;backdrop-filter:blur(14px);position:sticky;top:0;z-index:2}
.brand{display:flex;align-items:center;gap:12px;font-weight:850;letter-spacing:-.5px;font-size:19px}.mark{width:37px;height:37px;border-radius:12px;background:linear-gradient(145deg,var(--blue),#6b88ff);display:grid;place-items:center;color:white;font-size:19px;box-shadow:0 8px 20px #2459e033}.brand span{color:var(--blue)}.topnote{color:var(--muted);font-size:13px}
main{max-width:1180px;margin:38px auto;padding:0 22px 60px}.hero{display:grid;grid-template-columns:1.2fr .8fr;gap:28px;align-items:center;margin-bottom:28px}.eyebrow{text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:800;color:var(--blue)}h1{font-size:clamp(34px,5vw,56px);line-height:1.02;letter-spacing:-2.5px;margin:12px 0 16px}.hero p{max-width:590px;color:var(--muted);line-height:1.7;margin:0}.hero-art{min-height:180px;border-radius:26px;background:linear-gradient(135deg,#1c3477,#2459e0 62%,#21b9c6);padding:24px;color:white;position:relative;overflow:hidden;box-shadow:0 20px 45px #294ca525}.hero-art:before,.hero-art:after{content:"";position:absolute;border:1px solid #ffffff40;border-radius:50%;width:240px;height:240px;right:-35px;top:-100px}.hero-art:after{width:170px;height:170px;right:25px;top:-65px}.art-label{font-size:12px;opacity:.8;letter-spacing:1.5px}.art-big{font-size:35px;font-weight:800;letter-spacing:-1px;margin-top:14px}.art-small{font-size:13px;opacity:.85;margin-top:8px}
.layout{display:grid;grid-template-columns:340px 1fr;gap:22px;align-items:start}.panel{background:#fff;border:1px solid var(--line);border-radius:20px;padding:24px;box-shadow:0 8px 26px #253a6510}.panel h2{font-size:17px;letter-spacing:-.4px;margin:0 0 7px}.sub{font-size:13px;color:var(--muted);line-height:1.55;margin:0 0 20px}.drop{border:1.5px dashed #b9c7e1;border-radius:16px;background:#f8faff;padding:22px 15px;text-align:center;transition:.2s}.drop.drag{border-color:var(--blue);background:#eef3ff}.upload-icon{width:44px;height:44px;border-radius:14px;background:#e8eeff;color:var(--blue);display:grid;place-items:center;font-size:23px;margin:0 auto 12px}.drop strong{display:block;font-size:14px}.drop small{display:block;color:var(--muted);margin:7px 0 14px}.file-button,.primary,.secondary{border:0;border-radius:11px;padding:11px 15px;font-weight:750;cursor:pointer;font-size:13px}.file-button{background:#fff;color:var(--blue);border:1px solid #d7e0f5}.primary{background:var(--blue);color:#fff;box-shadow:0 8px 16px #2459e026}.secondary{background:#eef2f9;color:#334363}.field{display:block;margin-top:18px;font-size:12px;font-weight:750;color:#465573}.field input{display:block;width:100%;margin-top:8px;border:1px solid var(--line);border-radius:10px;padding:11px 12px;font:inherit;font-weight:450;color:var(--ink);outline:none}.field input:focus{border-color:var(--blue);box-shadow:0 0 0 3px #2459e014}.or{display:flex;align-items:center;gap:10px;color:#98a2b6;font-size:11px;margin:17px 0}.or:before,.or:after{content:"";height:1px;background:var(--line);flex:1}.hint{font-size:11px;color:#8a95a9;line-height:1.6;margin-top:16px}.right{display:grid;gap:18px}.result-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.result-head h2{margin:0 0 6px;font-size:19px}.pill{display:inline-flex;align-items:center;gap:6px;background:#eafaf4;color:#16845c;padding:7px 10px;border-radius:30px;font-size:11px;font-weight:800;white-space:nowrap}.pill:before{content:"";width:6px;height:6px;background:#22b47a;border-radius:50%}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:20px}.stat{padding:14px;border:1px solid var(--line);border-radius:13px;background:#fbfcff}.stat span{font-size:11px;color:var(--muted)}.stat strong{display:block;font-size:22px;letter-spacing:-.7px;margin-top:5px}.table-card{padding:0;overflow:hidden}.table-title{display:flex;align-items:center;justify-content:space-between;padding:18px 20px;border-bottom:1px solid var(--line)}.table-title strong{font-size:14px}.table-title span{font-size:11px;color:var(--muted)}.table-wrap{overflow:auto;max-width:100%}table{border-collapse:collapse;width:100%;font-size:12px;white-space:nowrap}th{background:#f5f7fc;color:#566481;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.5px}td,th{padding:12px 15px;border-bottom:1px solid #edf0f6}tbody tr:last-child td{border-bottom:0}tbody tr:hover{background:#fafbff}.index{color:#9aa5b8;font-variant-numeric:tabular-nums}.empty{padding:48px 20px;text-align:center}.empty .empty-icon{font-size:32px}.empty h3{margin:12px 0 8px}.empty p{color:var(--muted);font-size:13px;line-height:1.6;max-width:340px;margin:0 auto}.notice{display:none;padding:12px 14px;border-radius:12px;background:#fff1ed;color:#ad4228;font-size:12px;margin-top:14px}.notice.show{display:block}.footer{display:flex;justify-content:space-between;gap:12px;color:#8994a8;font-size:11px;margin-top:26px;padding:0 3px}.footer b{color:#596783}
@media(max-width:850px){.hero{grid-template-columns:1fr}.hero-art{min-height:145px}.layout{grid-template-columns:1fr}.topnote{display:none}}@media(max-width:500px){main{padding:0 14px 35px;margin-top:25px}.panel{padding:18px}.stats{grid-template-columns:1fr 1fr}.stat:last-child{grid-column:span 2}.hero-art{display:none}.result-head{flex-direction:column}}
</style></head>
<body>
<header><div class="brand"><div class="mark">⌁</div>CSV <span>ATLAS</span></div><div class="topnote">A small, clear first step in data science&nbsp; ↗</div></header>
<main>
<section class="hero"><div><div class="eyebrow">Task 16 · Data loading</div><h1>Meet your data<br>at first glance.</h1><p>Load a CSV file with Pandas, inspect the first and last records, and quickly understand the shape of your dataset — all in one clean workspace.</p></div><div class="hero-art"><div class="art-label">DATASET SNAPSHOT / 001</div><div class="art-big">Read. Inspect. Learn.</div><div class="art-small">Built with Python + Pandas · No notebook required</div></div></section>
<section class="layout">
<aside class="panel"><h2>Import a dataset</h2><p class="sub">Choose a local CSV file or enter a public CSV link to get started.</p>
<div class="drop" id="drop"><div class="upload-icon">⇧</div><strong>Drop your CSV file here</strong><small>CSV format · up to 5 MB</small><label class="file-button" for="file">Choose CSV file</label><input id="file" type="file" accept=".csv,text/csv" hidden></div>
<div class="or">OR USE A PUBLIC SOURCE</div><label class="field">CSV URL<input id="url" type="url" placeholder="https://example.com/data.csv"></label>
<button class="primary" id="loadUrl" style="width:100%;margin-top:12px">Load from URL ↗</button><div class="notice" id="notice"></div>
<div class="hint">Tip: Try a dataset with column headers in the first row. CSV Atlas uses <b>pandas.read_csv()</b> and displays the first five and last five records.</div></aside>
<div class="right">
<section class="panel" id="summary"><div class="result-head"><div><h2>Dataset overview</h2><p class="sub" style="margin:0">Your loaded dataset summary will appear here.</p></div><span class="pill">Ready to explore</span></div><div class="stats"><div class="stat"><span>Rows</span><strong>—</strong></div><div class="stat"><span>Columns</span><strong>—</strong></div><div class="stat"><span>Missing values</span><strong>—</strong></div></div></section>
<section class="panel table-card" id="first"><div class="empty"><div class="empty-icon">▤</div><h3>First five records</h3><p>Load a CSV to preview the first five rows of your data.</p></div></section>
<section class="panel table-card" id="last"><div class="empty"><div class="empty-icon">↧</div><h3>Last five records</h3><p>The final records will appear here after your CSV is loaded.</p></div></section>
</div></section>
<div class="footer"><span><b>CSV ATLAS</b> · Task 16 learning project</span><span>Python · Pandas · HTML/CSS</span></div>
</main>
<script>
const fileInput=document.getElementById('file'),drop=document.getElementById('drop'),notice=document.getElementById('notice');
function message(t){notice.textContent=t;notice.classList.add('show')}function clearMessage(){notice.textContent='';notice.classList.remove('show')}
fileInput.addEventListener('change',()=>{if(fileInput.files[0])upload(fileInput.files[0])});
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.add('drag')}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,x=>{x.preventDefault();drop.classList.remove('drag')}));
drop.addEventListener('drop',e=>{const f=e.dataTransfer.files[0];if(f)upload(f)});
async function upload(file){clearMessage();if(!file.name.toLowerCase().endsWith('.csv'))return message('Please choose a file ending in .csv.');const fd=new FormData();fd.append('file',file);await request('/api/upload',fd)}
document.getElementById('loadUrl').addEventListener('click',async()=>{clearMessage();const url=document.getElementById('url').value.trim();if(!url)return message('Enter a public CSV URL first.');await request('/api/url',JSON.stringify({url}))});
async function request(path,body){const isForm=body instanceof FormData;try{const r=await fetch(path,{method:'POST',headers:isForm?{}:{'Content-Type':'application/json'},body});const data=await r.json();if(!r.ok)throw new Error(data.error||'Unable to load dataset.');render(data)}catch(e){message(e.message||'Something went wrong. Check the CSV and try again.')}}
function render(d){clearMessage();document.querySelector('#summary').innerHTML=`<div class="result-head"><div><h2>${esc(d.name)}</h2><p class="sub" style="margin:0">Dataset successfully loaded and checked with Pandas.</p></div><span class="pill">Loaded successfully</span></div><div class="stats"><div class="stat"><span>Total rows</span><strong>${d.rows.toLocaleString()}</strong></div><div class="stat"><span>Total columns</span><strong>${d.columns.length}</strong></div><div class="stat"><span>Missing values</span><strong>${d.missing.toLocaleString()}</strong></div></div>`;
document.querySelector('#first').innerHTML=tableSection('First five records','df.head()',d.columns,d.first,d.firstStart);
document.querySelector('#last').innerHTML=tableSection('Last five records','df.tail()',d.columns,d.last,d.lastStart)}
function tableSection(title,method,cols,rows,start){let html=`<div class="table-title"><strong>${title}</strong><span>Pandas · ${method}</span></div><div class="table-wrap"><table><thead><tr><th>#</th>${cols.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>`;if(!rows.length)html+='<tr><td colspan="'+(cols.length+1)+'">No records</td></tr>';rows.forEach((r,i)=>{html+='<tr><td class="index">'+(start+i+1)+'</td>'+r.map(v=>`<td>${esc(v===null?'':String(v))}</td>`).join('')+'</tr>'});return html+'</tbody></table></div>'}
function esc(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
</script></body></html>"""

def dataset_payload(df, name):
    # Keep the page responsive and avoid returning very wide/large tables.
    columns = [str(c) for c in df.columns[:30]]
    view = df.iloc[:, :30]
    def clean(v):
        if pd.isna(v):
            return ""
        return str(v)[:500]
    first = [[clean(v) for v in row] for row in view.head(5).itertuples(index=False, name=None)]
    last = [[clean(v) for v in row] for row in view.tail(5).itertuples(index=False, name=None)]
    return {
        "name": str(name)[:180], "rows": int(len(df)), "columns": columns,
        "missing": int(df.isna().sum().sum()), "first": first, "last": last,
        "firstStart": 0, "lastStart": max(0, len(df)-len(last))
    }

class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, status, content, content_type):
        data = content if isinstance(content, bytes) else content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status, payload):
        self.send_bytes(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self.send_bytes(200, HTML, "text/html; charset=utf-8")
        elif path == "/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "Page not found."})

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > MAX_UPLOAD_BYTES + 100_000:
            return self.send_json(413, {"error": "Request is empty or too large. CSV files must be 5 MB or smaller."})
        body = self.rfile.read(length)
        try:
            if path == "/api/upload":
                content_type = self.headers.get("Content-Type", "")
                if "multipart/form-data" not in content_type:
                    return self.send_json(400, {"error": "Please upload a CSV file."})
                # Parse multipart upload using the standard library email parser.
                from email.parser import BytesParser
                from email.policy import default
                msg = BytesParser(policy=default).parsebytes(
                    b"Content-Type: " + content_type.encode() + b"\r\nMIME-Version: 1.0\r\n\r\n" + body
                )
                part = next((p for p in msg.iter_parts() if p.get_param("name", header="content-disposition") == "file"), None)
                if part is None:
                    return self.send_json(400, {"error": "No file was included in the upload."})
                filename = Path(part.get_filename() or "uploaded.csv").name
                raw = part.get_payload(decode=True) or b""
                if len(raw) > MAX_UPLOAD_BYTES:
                    return self.send_json(413, {"error": "CSV files must be 5 MB or smaller."})
                df = pd.read_csv(io.BytesIO(raw))
                return self.send_json(200, dataset_payload(df, filename))
            if path == "/api/url":
                data = json.loads(body.decode("utf-8"))
                url = str(data.get("url", "")).strip()
                if not url.startswith(("https://", "http://")):
                    return self.send_json(400, {"error": "URL must begin with http:// or https://."})
                # Restrict local/private hostnames to reduce server-side request forgery risk.
                from urllib.parse import urlparse as parse_url
                import socket, ipaddress
                parsed = parse_url(url)
                if not parsed.hostname:
                    return self.send_json(400, {"error": "That URL is not valid."})
                try:
                    addresses = socket.getaddrinfo(parsed.hostname, None)
                    if any(ipaddress.ip_address(a[4][0]).is_private or ipaddress.ip_address(a[4][0]).is_loopback or ipaddress.ip_address(a[4][0]).is_link_local for a in addresses):
                        return self.send_json(400, {"error": "For safety, URLs pointing to local/private networks are not allowed."})
                except socket.gaierror:
                    return self.send_json(400, {"error": "Could not find that host. Check the URL."})
                import urllib.request
                req = urllib.request.Request(url, headers={"User-Agent": "CSVAtlas/1.0"})
                with urllib.request.urlopen(req, timeout=12) as response:
                    if response.status != 200:
                        return self.send_json(400, {"error": "The URL did not return a successful response."})
                    raw = response.read(MAX_UPLOAD_BYTES + 1)
                if len(raw) > MAX_UPLOAD_BYTES:
                    return self.send_json(413, {"error": "The remote CSV is larger than 5 MB."})
                df = pd.read_csv(io.BytesIO(raw))
                return self.send_json(200, dataset_payload(df, parsed.path.rsplit("/", 1)[-1] or "remote_dataset.csv"))
            return self.send_json(404, {"error": "Unknown API endpoint."})
        except pd.errors.EmptyDataError:
            return self.send_json(400, {"error": "The CSV file is empty."})
        except pd.errors.ParserError as e:
            return self.send_json(400, {"error": "Could not parse the CSV. Check the delimiter and column structure."})
        except UnicodeDecodeError:
            return self.send_json(400, {"error": "Text encoding was not recognized. Save the file as UTF-8 CSV and try again."})
        except Exception as e:
            return self.send_json(400, {"error": "Could not load the dataset. Make sure it is a valid CSV file or direct CSV URL."})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

if __name__ == "__main__":
    print(f"\nCSV Atlas is running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.\n")
    HTTPServer((HOST, PORT), Handler).serve_forever()
