#!/usr/bin/env python3
"""
Server cục bộ cho ứng dụng Tìm Kiếm Thuốc.
Endpoint đặc biệt: /local-file?path=<đường_dẫn_đầy_đủ>
"""

import os
import sys
import mimetypes
import unicodedata
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Fix encoding cho Windows console (tránh crash khi print tiếng Việt)
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def decode_path(raw_path: str) -> str:
    """Decode URL-encoded path, normalize Unicode NFC + separators cho Windows."""
    p = urllib.parse.unquote(raw_path, encoding='utf-8')
    p = p.strip()                          # bỏ khoảng trắng thừa
    p = unicodedata.normalize('NFC', p)    # Excel NFD → Windows NFC
    p = p.replace('/', os.sep).replace('\\', os.sep)
    return os.path.normpath(p)


def resolve_path(path: str) -> str:
    """Giải quyết từng phần của path bằng fuzzy match (NFC, case-insensitive).
    Xử lý cả trường hợp tên thư mục cha có Unicode khác dạng."""
    drive, tail = os.path.splitdrive(path)
    parts = [p for p in tail.replace('\\', '/').split('/') if p]
    current = drive + os.sep
    for part in parts:
        exact = os.path.join(current, part)
        if os.path.exists(exact):
            current = exact
            continue
        # Fuzzy match trong thư mục hiện tại
        part_nfc = unicodedata.normalize('NFC', part).lower()
        matched = None
        try:
            for name in os.listdir(current):
                if unicodedata.normalize('NFC', name).lower() == part_nfc:
                    matched = name
                    break
        except OSError:
            pass
        if matched:
            print(f'[fuzzy] {part!r} → {matched!r}', flush=True)
            current = os.path.join(current, matched)
        else:
            return path  # không tìm được, trả về path gốc
    return current


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # ── Health check (detectServer) ──────────────────────────
        # Luôn trả 200 để JS biết server đang chạy
        if parsed.path == '/check-file':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            return

        # ── Đọc file cục bộ theo đường dẫn đầy đủ ───────────────
        if parsed.path == '/local-file':
            # parse_qs tự decode percent-encoding
            params    = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            raw_path  = params.get('path', [''])[0]
            file_path = decode_path(raw_path)

            print(f'[PDF] Raw   : {raw_path!r}', flush=True)
            print(f'[PDF] Tìm  : {file_path!r}', flush=True)
            print(f'[PDF] Bytes: {file_path.encode("utf-8")!r}', flush=True)

            # Thử resolve từng phần path nếu không tìm thấy chính xác
            if file_path and not os.path.isfile(file_path):
                file_path = resolve_path(file_path)

            if not file_path or not os.path.isfile(file_path):
                parent = os.path.dirname(file_path)
                if os.path.isdir(parent):
                    files_in_dir = os.listdir(parent)[:10]
                    print(f'[404] Không tìm thấy. Thư mục cha tồn tại. Các file trong đó:', flush=True)
                    for f in files_in_dir:
                        print(f'        {f!r}', flush=True)
                else:
                    print(f'[404] Thư mục cha không tồn tại: {parent!r}', flush=True)
                self.send_error(404, f'Not found: {os.path.basename(file_path)}')
                return

            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or 'application/octet-stream'

            try:
                file_size = os.path.getsize(file_path)
                print(f'[200] Phục vụ: {os.path.basename(file_path)!r} ({file_size:,} bytes)', flush=True)

                self.send_response(200)
                self.send_header('Content-Type', mime_type)
                self.send_header('Content-Length', str(file_size))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()

                with open(file_path, 'rb') as f:
                    # Đọc từng chunk để không tốn RAM với file lớn
                    while True:
                        chunk = f.read(65536)
                        if not chunk:
                            break
                        self.wfile.write(chunk)

            except PermissionError:
                print(f'[403] Không có quyền đọc: {file_path!r}', flush=True)
                self.send_error(403, 'Permission denied')
            except Exception as ex:
                print(f'[500] Lỗi: {ex}', flush=True)
                self.send_error(500, str(ex))
            return

        # ── Mặc định: serve static files ────────────────────────
        super().do_GET()

    def log_message(self, fmt, *args):
        # Bỏ qua log 200/304 (quá nhiều), chỉ in lỗi
        if args and len(args) >= 2 and not str(args[1]).startswith(('2', '3')):
            super().log_message(fmt, *args)


if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), Handler)
    print(f'Server đang chạy : http://localhost:{PORT}')
    print(f'Thư mục gốc      : {BASE_DIR}')
    print('Nhấn Ctrl+C để dừng.\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nĐã dừng server.')
