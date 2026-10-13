from django.contrib import admin
from .models import Appointment, Service, TimeSlot
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display=("name","duration_minutes","price","is_active")
    list_filter=("is_active",); search_fields=("name","description")
@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display=("service","date","start_time","end_time","is_active","booking_state")
    list_filter=("date","service","is_active"); date_hierarchy="date"
    @admin.display(description="Tình trạng")
    def booking_state(self,obj):
        if obj.appointments.filter(status__in=["pending","confirmed"]).exists(): return "Đã có lịch"
        return "Còn trống"
@admin.action(description="Xác nhận các lịch đã chọn")
def confirm_appointments(modeladmin,request,queryset):
    queryset.exclude(status=Appointment.Status.CANCELLED).update(status=Appointment.Status.CONFIRMED)
@admin.action(description="Hủy các lịch đã chọn")
def cancel_appointments(modeladmin,request,queryset):
    queryset.update(status=Appointment.Status.CANCELLED)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=("id","customer_name","phone","service_name","slot_date","slot_time","status","created_at")
    list_filter=("status","slot__date","slot__service"); search_fields=("customer_name","phone","email")
    readonly_fields=("created_at",); actions=(confirm_appointments,cancel_appointments)
    @admin.display(description="Dịch vụ")
    def service_name(self,obj): return obj.slot.service.name
    @admin.display(description="Ngày")
    def slot_date(self,obj): return obj.slot.date
    @admin.display(description="Khung giờ")
    def slot_time(self,obj): return f"{obj.slot.start_time:%H:%M}–{obj.slot.end_time:%H:%M}"
