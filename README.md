# 🧺 Nice Fold Saigon - Premium Hotel Laundry Web App & Chatbot

Dự án ứng dụng web đặt lịch giặt sấy cao cấp dành cho khách du lịch và khách lưu trú khách sạn tại Quận 1, TP.HCM. Hệ thống tích hợp tính toán chi phí tự động, Chatbot tư vấn khách hàng đa ngôn ngữ, hệ thống gửi email xác nhận tự động qua Resend, và Trang quản lý (Admin Dashboard) thân thiện.

---

## 📂 Cấu Trúc Thư Mục Dự Án

* `api.php`: API xử lý backend chính (PHP), chịu trách nhiệm điều hướng đặt lịch, khảo sát ý kiến, lưu dữ liệu đơn hàng và khách hàng dạng JSON, gửi email qua Resend và tích hợp Webhook thanh toán SePay.
* `app.js`: Tệp xử lý logic chính ở frontend (Javascript) bao gồm Chatbot AI, bảng tính phí, kiểm tra định dạng email/SĐT, và gửi yêu cầu đến backend.
* `index.html`: Giao diện trang chủ (Landing Page) giới thiệu dịch vụ và tích hợp khung Chatbot.
* `booking.html`: Giao diện trang đặt lịch giặt sấy trực tuyến và tính giá tự động.
* `pay.html`: Giao diện hiển thị mã QR thanh toán tích hợp nội dung chuyển khoản tự động.
* `shoes.html`: Giao diện đặt lịch riêng cho dịch vụ vệ sinh giày cao cấp.
* `admin/index.html`: Trang quản trị nội bộ dành cho tiệm để đối soát danh sách khách hàng, đơn hàng và sản phẩm.
* `resend_config.txt`: Tệp lưu trữ **Resend API Key** để gửi email tự động.
* `brain.db`: Cơ sở dữ liệu SQLite cục bộ lưu trữ các thiết lập giọng nói thương hiệu, dữ liệu khách hàng và đơn hàng (cho mục đích đối soát và AI).
* `email_log.txt` & `read_logs.php`: Tệp ghi nhật ký gửi email và trang web chẩn đoán lỗi gửi mail trực quan trên host.

---

## 🚀 Hướng Dẫn Triển Khai Lên Server Hosting

### **Bước 1: Tải mã nguồn lên Hosting**
1. Đăng nhập vào trình quản lý tệp (File Manager) trên cPanel/DirectAdmin hoặc sử dụng phần mềm FTP (như FileZilla).
2. Tải toàn bộ các tệp trong thư mục dự án lên thư mục gốc chạy web (thường là `public_html` hoặc `httpdocs`).
3. Bạn có thể sử dụng file giải nén trực tiếp từ **`nice-fold-saigon-premium.zip`** để tải lên nhanh hơn.

### **Bước 2: Cấu hình Khóa gửi mail (Resend API Key)**
1. Mở tệp `resend_config.txt` trên host.
2. Dán API Key của bạn từ tài khoản [Resend.com](https://resend.com) vào tệp này (ví dụ: `re_123456789...`).
3. Lưu lại. Backend `api.php` sẽ tự động đọc khóa bảo mật này để thực hiện gửi mail chào mừng và xác nhận đặt lịch.

### **Bước 3: Phân quyền thư mục (Permissions)**
Để đảm bảo PHP ghi được dữ liệu đơn hàng (`data_orders.json`), danh sách khách hàng (`data_customers.json`) và nhật ký gửi mail (`email_log.txt`):
* Hãy đảm bảo thư mục gốc chạy web có quyền ghi (**Write Permission** - thường là CHMOD `755` hoặc `775`).
* Nếu gặp lỗi không ghi được file, hãy CHMOD các file `.json` hoặc tệp `.txt` liên quan thành `644` hoặc `664`.

---

## 🛠️ Chẩn Đoán Lỗi & Mẹo Vận Hành

### **1. Chatbot không nhận diện được câu hỏi mới?**
* **Nguyên nhân:** Do trình duyệt của khách hàng lưu cache (lưu bộ nhớ đệm) file `app.js` rất nặng.
* **Cách xử lý:** Trong file `index.html` (và các file html khác), chúng tôi đã cấu hình liên kết script dạng `app.js?v=17.2`. Mỗi lần bạn thay đổi logic chatbot trong `app.js`, hãy tăng số phiên bản này lên (ví dụ: `v=17.3`) để ép trình duyệt tải lại file mới lập tức.

### **2. Khách đặt lịch hoặc đăng ký danh sách chờ nhưng không nhận được email?**
* **Cách xử lý:** 
  1. Truy cập trực tiếp đường dẫn **`https://yourdomain.com/read_logs.php`** trên trình duyệt để đọc 50 dòng log gửi mail gần nhất.
  2. Xem mã phản hồi HTTP:
     * `HTTP Code: 200`: Gửi mail thành công sang Resend.
     * `HTTP Code: 429`: Bị quá tần suất gửi mail miễn phí của Resend (hạn chế 2 mail/giây).
     * `HTTP Code: 401/403`: Khóa Resend API Key trong `resend_config.txt` bị sai hoặc hết hạn.
