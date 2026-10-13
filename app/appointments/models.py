from django.db import models
from django.db.models import Q
class Service(models.Model):
    name=models.CharField("Tên dịch vụ",max_length=120,unique=True)
    description=models.TextField("Mô tả",blank=True)
    duration_minutes=models.PositiveIntegerField("Thời lượng (phút)",default=30)
    price=models.DecimalField("Giá tham khảo (VNĐ)",max_digits=12,decimal_places=0,default=0)
    is_active=models.BooleanField("Đang hoạt động",default=True)
    created_at=models.DateTimeField("Ngày tạo",auto_now_add=True)
    class Meta:
        ordering=["name"]
        verbose_name="Dịch vụ"
        verbose_name_plural="Dịch vụ"
    def __str__(self): return self.name

class TimeSlot(models.Model):
    service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name="time_slots",verbose_name="Dịch vụ")
    date=models.DateField("Ngày")
    start_time=models.TimeField("Giờ bắt đầu")
    end_time=models.TimeField("Giờ kết thúc")
    is_active=models.BooleanField("Cho phép đặt",default=True)
    class Meta:
        ordering=["date","start_time"]
        constraints=[
            models.UniqueConstraint(fields=["service","date","start_time","end_time"],name="unique_service_slot"),
            models.CheckConstraint(condition=Q(end_time__gt=models.F("start_time")),name="slot_end_after_start"),
        ]
        verbose_name="Khung giờ"
        verbose_name_plural="Khung giờ"
    def __str__(self): return f"{self.service} — {self.date:%d/%m/%Y} {self.start_time:%H:%M}-{self.end_time:%H:%M}"

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING="pending","Chờ xác nhận"
        CONFIRMED="confirmed","Đã xác nhận"
        CANCELLED="cancelled","Đã hủy"
    slot=models.ForeignKey(TimeSlot,on_delete=models.PROTECT,related_name="appointments",verbose_name="Khung giờ")
    customer_name=models.CharField("Họ tên khách hàng",max_length=120)
    phone=models.CharField("Số điện thoại",max_length=25)
    email=models.EmailField("Email",blank=True)
    note=models.TextField("Ghi chú",blank=True,max_length=1000)
    status=models.CharField("Trạng thái",max_length=12,choices=Status.choices,default=Status.PENDING)
    created_at=models.DateTimeField("Ngày tạo",auto_now_add=True)
    class Meta:
        ordering=["-created_at"]
        constraints=[models.UniqueConstraint(fields=["slot"],condition=Q(status__in=["pending","confirmed"]),name="one_active_appointment_per_slot")]
        verbose_name="Lịch hẹn"
        verbose_name_plural="Lịch hẹn"
    def __str__(self): return f"{self.customer_name} — {self.slot} ({self.get_status_display()})"
