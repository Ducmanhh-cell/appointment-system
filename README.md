# Appointment System
Dự án hệ thống đặt lịch hẹn sử dụng Django, PostgreSQL và Docker Compose, tích hợp Nginx, Prometheus, Grafana, Loki và Promtail để triển khai, giám sát và quản lý log.
## 1. Công nghệ sử dụng
- Backend: Django, Gunicorn
- Database: PostgreSQL
- Quản trị database: pgAdmin
- Reverse proxy: Nginx
- Metrics: Prometheus, cAdvisor
- Dashboard: Grafana
- Log aggregation: Loki, Promtail
- Triển khai: Docker Compose
## 2. Yêu cầu
- Docker Desktop hoặc Docker Engine có Docker Compose
- Git (nếu clone dự án từ GitHub)
## 3. Cấu hình môi trường
Sao chép file cấu hình mẫu:
```powershell
Copy-Item .env.example .env
```
Chỉnh sửa `.env`, thay tất cả giá trị mẫu bằng thông tin phù hợp với môi trường của bạn. Đặt `DJANGO_SECRET_KEY` và mật khẩu database đủ mạnh.
**Không commit hoặc chia sẻ file `.env`.** File này đã được khai báo trong `.gitignore`.
## 4. Khởi chạy dự án
Kiểm tra cấu hình:
```powershell
docker compose config --quiet
```
Build và khởi chạy các dịch vụ:
```powershell
docker compose up -d --build
docker compose ps
```
Xem log của Django:
```powershell
docker compose logs --tail=100 web
```
## 5. Khởi tạo tài khoản và dữ liệu mẫu
Tạo tài khoản quản trị Django:
```powershell
docker compose exec web python manage.py createsuperuser
```
Tạo dịch vụ và khung giờ mẫu:
```powershell
docker compose exec web python /app/seed_data.py
```
## 6. Các địa chỉ truy cập
| Dịch vụ | Địa chỉ |
|---|---|
| Website qua Nginx | http://127.0.0.1:8088/ |
| Django trực tiếp | http://127.0.0.1:18000/ |
| Django Admin qua Nginx | http://127.0.0.1:8088/admin/ |
| pgAdmin | http://127.0.0.1:15050/ |
| Prometheus | http://127.0.0.1:9090/ |
| Grafana | http://127.0.0.1:3000/ |
| cAdvisor | http://127.0.0.1:8081/ |
| Loki API | http://127.0.0.1:3100/ |
Các cổng trên dựa theo cấu hình Windows hiện tại; hãy kiểm tra `.env` và `docker-compose.yml` nếu đã thay đổi cổng.
## 7. Giám sát và log
- Prometheus thu thập metrics từ Prometheus và cAdvisor.
- Grafana hiển thị dashboard giám sát.
- Promtail thu thập log ứng dụng và gửi tới Loki.
- Có thể sử dụng Grafana Explore để truy vấn log bằng LogQL.
Ví dụ truy vấn log:
```logql
{job="appointment-system"}
```
Lọc log chứa thông báo INFO:
```logql
{job="appointment-system"} |= "INFO"
```
Tìm các log có nội dung liên quan đến lỗi:
```logql
{job="appointment-system"} |~ "(?i)error|exception|failed"
```
Kết quả truy vấn phụ thuộc vào log thực tế đã được thu thập.
## 8. Kiểm tra và xử lý sự cố
```powershell
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 db
docker compose logs --tail=100 nginx
docker compose exec web python manage.py check
docker compose exec web python manage.py showmigrations
```
Kiểm tra website qua Nginx:
```powershell
Invoke-WebRequest http://127.0.0.1:8088/ -UseBasicParsing
```
## 9. Dữ liệu và bảo mật
- Không đưa `.env`, mật khẩu thật hoặc khóa bí mật lên GitHub.
- Sử dụng mật khẩu mạnh và thay các giá trị mẫu trước khi triển khai.
- Các dịch vụ database và quản trị nên được giới hạn truy cập theo nhu cầu.
- Dữ liệu PostgreSQL được lưu trong Docker named volume; không xóa volume nếu chưa sao lưu.
- Kiểm tra cấu hình bảo mật và quyền truy cập trước khi triển khai trên môi trường công khai.
## 10. Repository
Mã nguồn dự án: https://github.com/Ducmanhh-cell/appointment-system
