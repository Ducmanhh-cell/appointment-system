from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import AppointmentForm
from .models import Appointment, Service, TimeSlot
ACTIVE=[Appointment.Status.PENDING,Appointment.Status.CONFIRMED]
def home(request):
    services=Service.objects.filter(is_active=True)
    slots=TimeSlot.objects.filter(is_active=True,service__is_active=True,date__gte=timezone.localdate()).exclude(
        appointments__status__in=ACTIVE).select_related("service").order_by("date","start_time")[:8]
    return render(request,"appointments/index.html",{"services":services,"upcoming_slots":slots})
def book_appointment(request):
    if request.method=="POST":
        form=AppointmentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    slot=TimeSlot.objects.select_for_update().select_related("service").get(pk=form.cleaned_data["slot"].pk)
                    if not slot.is_active or not slot.service.is_active or slot.date < timezone.localdate():
                        form.add_error("slot","Khung giờ không còn khả dụng.")
                        raise ValueError("slot_unavailable")
                    if slot.appointments.filter(status__in=ACTIVE).exists():
                        form.add_error("slot","Khung giờ vừa được người khác đặt. Hãy chọn khung giờ khác.")
                        raise ValueError("slot_taken")
                    appointment=form.save(commit=False); appointment.slot=slot; appointment.save()
                messages.success(request,"Đặt lịch thành công. Lịch đang chờ xác nhận.")
                return redirect("booking_success",appointment_id=appointment.pk)
            except ValueError: pass
            except IntegrityError: form.add_error("slot","Khung giờ vừa được đặt. Vui lòng chọn khung giờ khác.")
    else: form=AppointmentForm()
    return render(request,"appointments/booking.html",{"form":form})
def booking_success(request,appointment_id):
    appointment=get_object_or_404(Appointment.objects.select_related("slot__service"),pk=appointment_id)
    return render(request,"appointments/booking_success.html",{"appointment":appointment})
def booking_lookup(request):
    appointments=None; error=None
    if request.method=="POST":
        phone=request.POST.get("phone","").strip()
        if phone:
            appointments=Appointment.objects.select_related("slot__service").filter(phone=phone).order_by("-created_at")[:10]
            if not appointments: error="Không tìm thấy lịch hẹn với số điện thoại này."
        else: error="Vui lòng nhập số điện thoại."
    return render(request,"appointments/booking_lookup.html",{"appointments":appointments,"error":error})
