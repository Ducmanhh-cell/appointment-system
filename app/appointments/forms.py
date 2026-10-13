from django import forms
from django.utils import timezone
from .models import Appointment, Service, TimeSlot
ACTIVE=[Appointment.Status.PENDING,Appointment.Status.CONFIRMED]
class AppointmentForm(forms.ModelForm):
    service=forms.ModelChoiceField(label="Dịch vụ",queryset=Service.objects.none(),empty_label="-- Chọn dịch vụ --")
    slot=forms.ModelChoiceField(label="Ngày và khung giờ",queryset=TimeSlot.objects.none(),empty_label="-- Chọn khung giờ --")
    class Meta:
        model=Appointment
        fields=["customer_name","phone","email","note"]
        labels={"customer_name":"Họ và tên","phone":"Số điện thoại","email":"Email (không bắt buộc)","note":"Ghi chú (không bắt buộc)"}
        widgets={"customer_name":forms.TextInput(attrs={"placeholder":"Nguyễn Văn A","autocomplete":"name"}),
                 "phone":forms.TextInput(attrs={"placeholder":"09xxxxxxxx","autocomplete":"tel"}),
                 "email":forms.EmailInput(attrs={"placeholder":"email@example.com"}),
                 "note":forms.Textarea(attrs={"rows":3,"placeholder":"Nội dung cần lưu ý (không bắt buộc)"})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["service"].queryset=Service.objects.filter(is_active=True)
        slots=TimeSlot.objects.filter(is_active=True,service__is_active=True,date__gte=timezone.localdate()).exclude(
            appointments__status__in=ACTIVE).order_by("date","start_time")
        if self.is_bound:
            sid=self.data.get("service","")
            if sid.isdigit(): slots=slots.filter(service_id=int(sid))
        self.fields["slot"].queryset=slots
    def clean_phone(self):
        phone=self.cleaned_data["phone"].strip()
        digits="".join(c for c in phone if c.isdigit())
        if not 9 <= len(digits) <= 15: raise forms.ValidationError("Số điện thoại phải có từ 9 đến 15 chữ số.")
        return phone
    def clean(self):
        data=super().clean(); service=data.get("service"); slot=data.get("slot")
        if service and slot:
            if slot.service_id != service.id: self.add_error("slot","Khung giờ không thuộc dịch vụ đã chọn.")
            if not slot.is_active or not slot.service.is_active: self.add_error("slot","Khung giờ hoặc dịch vụ không khả dụng.")
            if slot.date < timezone.localdate(): self.add_error("slot","Không thể đặt lịch trong quá khứ.")
            if slot.appointments.filter(status__in=ACTIVE).exists(): self.add_error("slot","Khung giờ vừa được đặt; hãy chọn khung giờ khác.")
        return data
