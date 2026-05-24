# Tìm Kiếm Thuốc - Web App

Ứng dụng web tìm kiếm thuốc trên nhiều file Excel cùng lúc, hỗ trợ xem PDF file gốc trực tiếp trong trình duyệt.

---

## Tính năng

- Chọn thư mục chứa nhiều file `.xlsx` / `.xls` cùng lúc
- **Hai ô tìm kiếm độc lập** — lọc đồng thời theo tên thuốc và chẩn đoán (logic AND)
  - Ô **Tên thuốc**: tìm theo cột `TENDUOCDAYDU`
  - Ô **Chẩn đoán**: tìm theo cột `CHANDOANVAOKHOA`
- Gợi ý autocomplete khi gõ (tối đa 15 gợi ý, highlight từ khớp)
- Tìm kiếm accent-insensitive: gõ `"thuoc"` tìm được `"Thuốc"`
- Kết quả hiển thị dạng bảng **4 cột**: Nguồn File / Tên Thuốc / Chẩn Đoán / File Gốc
- Nút **copy** trên cột File Gốc để sao chép đường dẫn đầy đủ
- Click vào dòng → xem PDF file gốc ngay trong panel bên phải
- Xem PDF: zoom (nút +/−, hoặc **Ctrl + scroll chuột**), chuyển trang, thumbnail
- Kéo thanh chia giữa để điều chỉnh tỉ lệ panel trái/phải
- Kéo tiêu đề cột để thay đổi độ rộng từng cột
- **Tự động lưu dữ liệu** vào IndexedDB — F5 không mất dữ liệu, tự load lại
- Không upload dữ liệu lên internet

---

## Cấu trúc file Excel yêu cầu

| Cột | Mô tả |
|-----|-------|
| `TENDUOCDAYDU` | Tên thuốc đầy đủ — dùng để tìm kiếm ô 1 |
| `CHANDOANVAOKHOA` | Chẩn đoán vào khoa — dùng để tìm kiếm ô 2 (tuỳ chọn) |
| `LOCAL_FILE` | Đường dẫn đầy đủ tới file PDF (ví dụ: `E:\file_Thuoc\...\Signed_xxx.pdf`) |
| Các cột khác | Giữ nguyên, không ảnh hưởng |

---

## Chạy local (có xem PDF)

### Yêu cầu
- Python 3.7+

### Khởi động
```bash
cd d:\@Code\WebSeachThuocXemFile
python server.py
```

Mở trình duyệt vào: **http://localhost:8080**

Dừng server: nhấn `Ctrl+C` trong terminal.

> **Lưu ý:** Chỉ dùng `python server.py`, **không** dùng `python -m http.server` (thiếu endpoint `/local-file` để đọc PDF).

---

## Deploy lên GitHub Pages (không xem được PDF local)

### Bước 1: Tạo repository
1. Vào [github.com](https://github.com) → **New repository**
2. Đặt tên repo (ví dụ: `thuoc-search`), chọn **Public**
3. Nhấn **Create repository**

### Bước 2: Push code
```bash
git init
git add index.html
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/TEN_BAN/TEN_REPO.git
git push -u origin main
```
> Thay `TEN_BAN` và `TEN_REPO` bằng tên GitHub và tên repo của bạn.

### Bước 3: Bật GitHub Pages
1. Vào repo → **Settings** → **Pages**
2. **Source**: `Deploy from a branch`
3. Branch: `main` / folder: `/ (root)` → **Save**

### Bước 4: Truy cập
```
https://TEN_BAN.github.io/TEN_REPO/
```

> Trên GitHub Pages: tìm kiếm và xem dữ liệu Excel hoạt động bình thường. Xem PDF local (`E:\...`) chỉ hoạt động khi chạy qua `server.py`.

---

## Cách sử dụng

1. Chạy `python server.py` → mở `http://localhost:8080`
2. Nhấn **Chọn thư mục Excel** → chọn thư mục chứa các file `.xlsx`
3. Chờ thanh tiến trình hoàn tất
4. Gõ tên thuốc vào ô **Tên thuốc** và/hoặc chẩn đoán vào ô **Chẩn đoán** → chọn gợi ý hoặc nhấn **Enter**
5. Hai ô kết hợp AND: để trống ô nào thì không lọc theo ô đó
6. Click vào dòng kết quả → PDF hiển thị bên phải
7. F5 trang: dữ liệu tự load lại từ cache, không cần chọn file lại

### Phím tắt PDF
| Thao tác | Phím / Chuột |
|----------|-------------|
| Trang trước | `←` hoặc `Page Up` |
| Trang sau | `→` hoặc `Page Down` |
| Phóng to / Thu nhỏ | `Ctrl` + lăn chuột |
| Zoom bằng nút | `+` / `−` trên toolbar |

---

## Ghi chú kỹ thuật

- **Excel parsing**: SheetJS (xlsx 0.20.3) chạy trong Web Worker — không block UI
- **Worker pool**: `min(CPU cores, 4)` workers xử lý song song
- **Search index**: hai mảng `searchIdx[]` và `diagIdx[]` đã normalize sẵn, tìm kiếm `includes()` trên 400k+ dòng < 50ms
- **PDF viewer**: PDF.js 3.11.174
- **Cache**: IndexedDB lưu ArrayBuffer của từng file Excel
- **Local file server**: Python `http.server` mở rộng với endpoint `/local-file?path=...`, hỗ trợ Unicode NFC normalization và fuzzy path matching
