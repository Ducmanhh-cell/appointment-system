from django.urls import path
from . import views
urlpatterns=[
 path("",views.home,name="home"),
 path("dat-lich/",views.book_appointment,name="book_appointment"),
 path("dat-lich/thanh-cong/<int:appointment_id>/",views.booking_success,name="booking_success"),
 path("tra-cuu/",views.booking_lookup,name="booking_lookup"),
]
