from django.shortcuts import render, redirect
from .forms import BillForm
from .models import Bill
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")  # 🟢
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")  # 🔴

    return render(request, "bills/login.html")


@login_required
def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST, request.FILES)

        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, "Bill added successfully!")  # 🟢
            return redirect('add')
        else:
            messages.error(request, "Error adding bill. Please try again.")  # 🔴

    else:
        form = BillForm()

    return render(request, 'bills/add_bill.html', {'form': form})



from datetime import date

@login_required
def bill_list(request):
    bills = Bill.objects.filter(user=request.user)
    today = date.today()
    return render(request, 'bills/bill_list.html', {
        'bills': bills,
        'today': today
    })


from django.shortcuts import get_object_or_404

@login_required
def delete_bill(request, id):
    bill = get_object_or_404(Bill, id=id, user=request.user)
    bill.delete()
    messages.success(request, "Bill deleted successfully!")  # 🟢
    return redirect('bill_list')



from datetime import date, timedelta
from django.core.mail import send_mail
from .models import Bill


def send_expiry_notifications():
    today = date.today()
    upcoming = today + timedelta(days=3)

    bills = Bill.objects.filter(
        expiry_date__range=[today, upcoming],
        email_sent=False
    )

    for bill in bills:
        message = f"""
Dear {bill.user.username},

This is a reminder from your Digital Warranty Management System.

Your warranty for the following product is about to expire:

Product Name: {bill.product_name}
Purchase Date: {bill.purchase_date}
Expiry Date: {bill.expiry_date}

Please take necessary action before the expiry date to avoid loss of warranty benefits.

Thank you for using Digital Warranty System.

Regards,
Digital Warranty Team
"""

        send_mail(
            subject="⚠ Warranty Expiry Reminder",
            message=message,
            from_email="Digital Warranty <yourgmail@gmail.com>",
            recipient_list=[bill.user.email],
            fail_silently=False,
        )

        bill.email_sent = True
        bill.save()



def trigger_notifications(request):
    send_expiry_notifications()
    return HttpResponse("Emails sent successfully!")






import pytesseract
from PIL import Image
import re
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_bill_data(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))

    # find date patterns
    date_patterns = r"\d{2}/\d{2}/\d{4}"
    dates = re.findall(date_patterns, text)

    purchase_date = None

    if dates:
        try:
            purchase_date = datetime.strptime(dates[0], "%d/%m/%Y").date()
        except:
            pass

    return purchase_date




@login_required
def extend_warranty(request, id):
    bill = get_object_or_404(Bill, id=id, user=request.user)

    if request.method == "POST":
        months = int(request.POST.get("months"))
        bill.expiry_date += timedelta(days=30*months)
        bill.extended_months += months
        bill.save()
        return redirect("bill_list")

    return render(request, "bills/extend_warranty.html", {"bill": bill})





def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")  # 🟢
            return redirect('login')

        else:
            messages.error(request, "Registration failed. Please check details.")  # 🔴

    else:
        form = UserCreationForm()

    return render(request, 'bills/register.html', {'form': form})



from django.shortcuts import render
from .models import Bill
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta


@login_required
def dashboard(request):
    today = timezone.now().date()

    total_bills = Bill.objects.filter(user=request.user).count()
    active = Bill.objects.filter(expiry_date__gt=today).count()
    expired = Bill.objects.filter(expiry_date__lt=today).count()

    return render(request, 'dashboard.html', {
        'total_bills': total_bills,
        'active': active,
        'expired': expired
    })

def home(request):
    return render(request, 'bills/home.html')
   

