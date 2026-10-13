# Appointment System — Đề 40
Sinh viên: Lường Đức Mạnh | Môn: Triển khai và Quản trị Hệ thống Phần mềm

## Khởi chạy (Ubuntu)
```bash
cp .env.example .env
nano .env
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs -f web
```
Thay toàn bộ mật khẩu mẫu và DJANGO_SECRET_KEY trong `.env`. Không commit `.env`.

## Tạo tài khoản admin và dữ liệu mẫu
```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python /app/seed_data.py
```

## Truy cập
- Website: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/
- pgAdmin: http://127.0.0.1:5050/

Trong pgAdmin thêm server: Host `db`, port `5432`, database/user/password lấy từ `.env`.

## Kiểm tra
```bash
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 db
curl -i http://127.0.0.1:8000/health/
docker compose exec web python manage.py check
docker compose exec web python manage.py showmigrations
```

Giai đoạn này triển khai Django, PostgreSQL, pgAdmin, quản lý dịch vụ/khung giờ/lịch hẹn. Nginx, Prometheus, Grafana, Loki, Promtail và hardening nâng cao sẽ thêm ở các giai đoạn sau.
