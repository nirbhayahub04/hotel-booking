import base64
from email.mime.text import MIMEText
import hashlib
import hmac
import json
import os
import smtplib
import requests
from uuid import uuid1, uuid4
from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from accounts.models import CustomUser
from hotel.models import Reservation, Room
from payments.models import PaymentHistory


def payment_success(request):
    # Get booking data from cache
    booking_data = cache.get("booking_data")
    if not booking_data:
        return render(request, "404.html")

    user = get_object_or_404(CustomUser, id=booking_data["initiated_by"])
    room = get_object_or_404(Room, room_id=booking_data["room_id"])
    reservation = Reservation.objects.filter(
        room=room,
        check_in_date=booking_data["check_in"],
        check_out_date=booking_data["check_out"],
    ).first()

    if not reservation:
        return render(request, "500.html")

    room.availability_status = "BOOKED"
    room.save()

    context = {
        "hotel_name": room.hotel.hotel_name,
        "booking_number": reservation.reservation_id,
        "check_in": booking_data["check_in"],
        "check_out": booking_data["check_out"],
        "total_amount": room.base_price,
        "payment_method": "E-Banking",
        "user_email": user.email,
        "transaction_id": str(uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    cache.delete("booking_data")
    return render(request, "payment_success.html", context)


def payment_failure(request):
    cache.delete("booking_data")

    return render(request, "payment_failure.html")


def generate_signature(msg):
    message = msg.encode("utf-8")
    hmac_sha256 = hmac.new("8gBm/:&EnhH.1/q".encode("utf-8"), message, hashlib.sha256)
    digest = hmac_sha256.digest()
    signature = base64.b64encode(digest).decode("utf-8")

    return signature


@csrf_exempt
def esewa_initiate(request):
    cache_data = cache.get("booking_data")
    if not cache_data:
        return render(request, "500.html")

    room = get_object_or_404(Room, room_id=cache_data["room_id"])

    # Calculate total amount based on booking duration
    check_in = datetime.strptime(cache_data["check_in"], "%Y-%m-%d")
    check_out = datetime.strptime(cache_data["check_out"], "%Y-%m-%d")
    total_days = (check_out - check_in).days
    total_amount = room.base_price * total_days

    # Generate transaction details
    transaction_uuid = str(uuid4())
    product_code = "EPAYTEST"

    # Create signature
    msg = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    signature = generate_signature(msg)

    # Prepare payload
    payload = {
        "amount": str(total_amount),
        "tax_amount": "0",
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        "product_code": product_code,
        "total_amount": str(total_amount),
        "transaction_uuid": transaction_uuid,
        "success_url": "http://localhost:8000/verify-esewa",
        "failure_url": "http://localhost:8000/payment-failure",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": signature,
    }

    # Initiate payment
    target_url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
    response = requests.post(target_url, data=payload)

    if response.status_code == 200:
        return redirect(response.url)

    return render(request, "500.html")


@csrf_exempt
def esewa_verify(request):
    if request.method == "GET":
        encoded_data = request.GET.get("data")

        if encoded_data:
            try:
                decoded_data = json.loads(base64.b64decode(encoded_data))

                if decoded_data["status"] == "COMPLETE":
                    transaction_id = decoded_data["transaction_uuid"]
                    total_amount = decoded_data["total_amount"].replace(",", "")

                    # Get booking data from cache
                    booking_data = cache.get("booking_data")
                    if not booking_data:
                        return render(request, "500.html")

                    # Get user
                    user = get_object_or_404(
                        CustomUser, id=booking_data["initiated_by"]
                    )

                    # Get room details
                    room = get_object_or_404(Room, room_id=booking_data["room_id"])
                    hotel = room.hotel

                    # Save transaction
                    payment = PaymentHistory.objects.create(
                        transaction_id=transaction_id,
                        user=user,
                        total_payment=total_amount,
                        payment_via=PaymentHistory.PaymentMethod.ESEWA,
                    )

                    # Create reservation
                    Reservation.objects.create(
                        user=user,
                        room=room,
                        hotel=hotel,
                        check_in_date=booking_data["check_in"],
                        check_out_date=booking_data["check_out"],
                        number_of_guests=booking_data["no_of_guest"],
                        special_requests=booking_data["special_requests"],
                        payment_ref_id=payment,
                        payment_status=Reservation.PaymentStatus.PAID,
                    )
                    send_email(user, booking_data, transaction_id)

                    return redirect("payment_success")
            except Exception as e:
                print(f"Error processing eSewa verification: {e}")
                return render(request, "500.html")

    return redirect("payment_failure")


@csrf_exempt
def khalti_initiate(request):
    cache_data = cache.get("booking_data")
    if cache_data == None:
        return render(request, "500.html")

    print(cache_data)
    product = get_object_or_404(Room, room_id=cache_data["room_id"])

    check_in = cache_data["check_in"]
    check_out = cache_data["check_out"]

    start = datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.strptime(check_out, "%Y-%m-%d")
    total_days = (end - start).days
    total_amount = product.base_price * total_days

    purchase_id = uuid4().__str__()
    customer_info = {
        "name": request.user.full_name(),
        "email": request.user.email,
        "phone": request.user.phone_number,
    }

    raw_payload = {
        "return_url": "http://localhost:8000/verify-khalti",
        "website_url": "http://localhost:8000",
        "amount": round(total_amount * 100),
        "purchase_order_id": purchase_id,
        "purchase_order_name": product.get_product_code(),
        "customer_info": customer_info,
        "amount_breakdown": [
            {"label": "Mark Price", "amount": round(total_amount * 100)},
            {"label": "VAT", "amount": 0},
        ],
    }

    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    payload = json.dumps(raw_payload)

    headers = {
        "Authorization": "Key a7428914c6a7438fa018e551837f9231",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return redirect(response.json()["payment_url"])

    return render(request, "500.html")


@csrf_exempt
def khalti_verify(request):
    if request.method == "GET":
        status = request.GET.get("status", "Failed")

        if status == "Completed":
            pidx = request.GET.get("pidx")
            transaction_id = request.GET.get("transaction_id")
            amount = request.GET.get("amount")
            total_amount = request.GET.get("total_amount")
            purchase_order_id = request.GET.get("purchase_order_id")
            purchase_order_name = request.GET.get("purchase_order_name")

            try:
                # Get booking data from cache
                booking_data = cache.get("booking_data")
                if not booking_data:
                    return render(request, "500.html")

                # Get user
                user = get_object_or_404(CustomUser, id=booking_data["initiated_by"])

                # Get room details
                room = get_object_or_404(Room, room_id=booking_data["room_id"])
                hotel = room.hotel

                # Create payment history
                payment = PaymentHistory.objects.create(
                    transaction_id=transaction_id,
                    user=user,
                    total_payment=total_amount,
                    payment_via=PaymentHistory.PaymentMethod.KHALTI,
                )

                # Create reservation
                Reservation.objects.create(
                    user=user,
                    room=room,
                    hotel=hotel,
                    check_in_date=booking_data["check_in"],
                    check_out_date=booking_data["check_out"],
                    number_of_guests=booking_data["no_of_guest"],
                    special_requests=booking_data["special_requests"],
                    payment_ref_id=payment,
                    payment_status=Reservation.PaymentStatus.PAID,
                )

                # Send confirmation email to user
                send_email(user, booking_data, transaction_id)

                return redirect("payment_success")
            except Exception as e:
                print(f"Error: {e}")
                return render(request, "500.html")

    return redirect("payment_failure")


def send_email(user, booking_data, transaction_id):
    """Send booking confirmation email to user"""
    try:
        from_email = os.getenv("EMAIL_USER")
        to_email = user.email
        subject = f"Booking Confirmation - {booking_data.get('room_id')}"

        body = f"""
        Dear {user.get_full_name()},
        
        Your hotel booking has been confirmed.
        
        Booking Details:
        - Room: {booking_data.get('room_id')}
        - Check-in: {booking_data.get('check_in')}
        - Check-out: {booking_data.get('check_out')}
        - Guests: {booking_data.get('no_of_guest')}
        - Transaction ID: {transaction_id}
        
        Thank you for choosing us!
        """

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as server:
            server.starttls()
            server.login(from_email, os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
