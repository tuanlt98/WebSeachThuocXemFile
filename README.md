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

> **Giới hạn:** Tìm kiếm Excel hoạt động bình thường. Xem PDF file cục bộ (`E:\...`) **không hoạt động** trên GitHub Pages — cần chạy `server.py` ở máy tính.

---

### Bước 1: Tạo repository trên GitHub

1. Đăng nhập [github.com](https://github.com)
2. Nhấn nút **"+"** góc trên phải → **New repository**
3. Điền thông tin:
   - **Repository name**: đặt tên (ví dụ: `WebSeachThuocXemFile`)
   - **Visibility**: chọn **Public**
   - **KHÔNG tick** "Add a README file", "Add .gitignore", "Choose a license"
4. Nhấn **Create repository**

---

### Bước 2: Khởi tạo git và commit (chạy 1 lần duy nhất)

Mở terminal trong thư mục chứa project, chạy lần lượt:

```bash
git init
git add index.html server.py README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TEN_BAN/TEN_REPO.git
git push -u origin main
```

> Thay `TEN_BAN` bằng GitHub username và `TEN_REPO` bằng tên repo vừa tạo.
>
> Lần đầu push: trình duyệt sẽ hiện cửa sổ đăng nhập GitHub → đăng nhập vào là xong.

---

### Bước 3: Bật GitHub Pages

1. Vào repo trên GitHub → tab **Settings**
2. Kéo xuống phần **Pages** (menu bên trái)
3. Mục **Source**: chọn `Deploy from a branch`
4. Mục **Branch**: đổi từ `None` → **`main`**, folder giữ nguyên `/ (root)`
5. Nhấn **Save**

> **Lưu ý:** Nút "Start free for 30 days" trên trang đó là quảng cáo GitHub Enterprise — **bỏ qua**, không cần nhấn.

---

### Bước 4: Truy cập

Chờ ~1–2 phút (GitHub build lần đầu), sau đó mở:

```
https://TEN_BAN.github.io/TEN_REPO/
```

Ví dụ thực tế:
```
https://tuanlt98.github.io/WebSeachThuocXemFile/
```

---

### Cập nhật code sau này

Khi sửa `index.html` và muốn cập nhật lên GitHub Pages:

```bash
git add index.html
git commit -m "Mô tả thay đổi"
git push
```

GitHub Pages tự động deploy lại sau ~1 phút.

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
- **Cache**: IndexedDB lưu cả ArrayBuffer file Excel lẫn dữ liệu đã parse sẵn — reload trang khôi phục ngay lập tức, không parse lại
- **Local file server**: Python `http.server` mở rộng với endpoint `/local-file?path=...`, hỗ trợ Unicode NFC normalization và fuzzy path matching
