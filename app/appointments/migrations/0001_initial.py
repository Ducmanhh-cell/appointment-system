import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Q

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="Tên dịch vụ")),
                ("description", models.TextField(blank=True, verbose_name="Mô tả")),
                ("duration_minutes", models.PositiveIntegerField(default=30, verbose_name="Thời lượng (phút)")),
                ("price", models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name="Giá tham khảo (VNĐ)")),
                ("is_active", models.BooleanField(default=True, verbose_name="Đang hoạt động")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")),
            ],
            options={"ordering": ["name"], "verbose_name": "Dịch vụ", "verbose_name_plural": "Dịch vụ"},
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Ngày")),
                ("start_time", models.TimeField(verbose_name="Giờ bắt đầu")),
                ("end_time", models.TimeField(verbose_name="Giờ kết thúc")),
                ("is_active", models.BooleanField(default=True, verbose_name="Cho phép đặt")),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="time_slots", to="appointments.service", verbose_name="Dịch vụ")),
            ],
            options={"ordering": ["date", "start_time"], "verbose_name": "Khung giờ", "verbose_name_plural": "Khung giờ"},
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=120, verbose_name="Họ tên khách hàng")),
                ("phone", models.CharField(max_length=25, verbose_name="Số điện thoại")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("note", models.TextField(blank=True, max_length=1000, verbose_name="Ghi chú")),
                ("status", models.CharField(choices=[("pending", "Chờ xác nhận"), ("confirmed", "Đã xác nhận"), ("cancelled", "Đã hủy")], default="pending", max_length=12, verbose_name="Trạng thái")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")),
                ("slot", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="appointments.timeslot", verbose_name="Khung giờ")),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "Lịch hẹn", "verbose_name_plural": "Lịch hẹn"},
        ),
        migrations.AddConstraint(
            model_name="timeslot",
            constraint=models.UniqueConstraint(fields=("service", "date", "start_time", "end_time"), name="unique_service_slot"),
        ),
        migrations.AddConstraint(
            model_name="timeslot",
            constraint=models.CheckConstraint(condition=Q(end_time__gt=models.F("start_time")), name="slot_end_after_start"),
        ),
        migrations.AddConstraint(
            model_name="appointment",
            constraint=models.UniqueConstraint(condition=Q(status__in=["pending", "confirmed"]), fields=("slot",), name="one_active_appointment_per_slot"),
        ),
    ]
