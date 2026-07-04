# 🚀 Deploy Notes - Nice Fold Saigon (Production VPS)

Tệp này hướng dẫn thiết lập và triển khai Website Nice Fold Saigon lên VPS (ví dụ: 123Host).

---

## 1. Các biến môi trường cần cấu hình (.env)

Trước khi chạy server trên VPS, bạn cần tạo một file `.env` nằm ở thư mục gốc của dự án với các biến sau:

```env
# Cổng chạy ứng dụng
PORT=3000

# Khóa gửi email Resend (Bắt buộc)
RESEND_API_KEY=re_ipBYmcFn_JxbThTFu7H2ezxkTjSBaTkcS

# Các Webhook phụ trợ (Đã có sẵn giá trị mặc định trong code, chỉ chỉnh sửa khi cần đổi URL)
GOOGLE_FORM_RESPONSE_URL=https://docs.google.com/forms/d/e/1FAIpQLSfMTQAoppyHdDGNcGGiDWDI3Gonl6t1WkcbdlMQseX7ORg31g/formResponse
N8N_ADMIN_CUSTOMERS_URL=https://hoangoanh.app.n8n.cloud/webhook/admin-customers
N8N_ADMIN_ORDERS_URL=https://hoangoanh.app.n8n.cloud/webhook/admin-orders
N8N_UPDATE_ORDER_URL=https://hoangoanh.app.n8n.cloud/webhook/update-order
```

---

## 2. Các cổng kết nối & Dịch vụ

* **Cổng lắng nghe (Listening Port):** Mặc định là `3000` (hoặc cấu hình thông qua biến `PORT` ở `.env`).
* **Đường dẫn Admin:** `http://<IP_VPS>:<PORT>/admin` (ví dụ: `http://localhost:3000/admin`).
* **Database:** Sử dụng SQLite (`brain.db`). Tự động khởi tạo cấu trúc bảng và cập nhật cột khi khởi chạy server lần đầu.

---

## 3. Các lệnh để khởi động server trên VPS

### Bước A: Cài đặt Node.js và NPM
Đảm bảo VPS đã cài đặt Node.js (khuyến nghị phiên bản 18 LTS trở lên).
Trên Ubuntu/Debian:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Bước B: Cài đặt thư viện của dự án
Di chuyển vào thư mục dự án và chạy:
```bash
npm install
```

### Bước C: Chạy ứng dụng

* **Chạy thử nghiệm (Development):**
  ```bash
  node server.js
  ```

* **Chạy lâu dài trên Production (Khuyến nghị dùng PM2):**
  Cài đặt PM2 để giữ server chạy ngầm liên tục ngay cả khi tắt SSH:
  ```bash
  sudo npm install -y -g pm2
  pm2 start server.js --name "nicefoldsaigon"
  pm2 save
  pm2 startup
  ```

---

## 4. Cấu hình Nginx làm Reverse Proxy (Khuyến nghị cho Production)
Để chạy website qua tên miền (ví dụ: `nicefoldsaigon.vn`) mà không cần gõ cổng `:3000`, hãy cấu hình Nginx chuyển tiếp yêu cầu đến cổng `3000`:

```nginx
server {
    listen 80;
    server_name nicefoldsaigon.vn www.nicefoldsaigon.vn;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
Sau đó cài đặt chứng chỉ SSL miễn phí bằng Certbot (Let's Encrypt).
