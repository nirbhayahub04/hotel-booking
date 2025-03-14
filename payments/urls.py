from django.urls import path

from payments import views


urlpatterns = [
    path("esewa-payment/", views.esewa_initiate, name="pay_with_esewa"),
    path("khalti-payment/", views.khalti_initiate, name="pay_with_khalti"),
    path("verify-esewa/", views.esewa_verify, name="verify_esewa"),
    path("verify-khalti/", views.khalti_verify, name="verify_khalti"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failure/", views.payment_failure, name="payment_failure"),
]
