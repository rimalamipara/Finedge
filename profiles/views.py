import datetime, random, re
from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
from profiles.models import Status 
from django.db.models import Q

def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000000000, 999999999999))

def index(request):
    try:
        curr_user = Status.objects.get(user_name=request.user) # getting details of current user
    except:
        # if no details exist (new user), create new details
        curr_user = Status()
        curr_user.account_number = randomGen() # random account number for every new user
        curr_user.balance = 0
        curr_user.user_name = request.user.username
        curr_user.save()
    display_name = curr_user.user_name.upper()
    return render(request, "profiles/profile.html", {"curr_user": curr_user,"display_name": display_name})

def money_transfer(request):
    if request.method == 'POST':
        recipient_name = request.POST.get('recipient_name', '').strip()
        account_number = request.POST.get('recipient_account_number') or request.POST.get('account_number')
        transfer_amount = request.POST.get('transfer_amount') or request.POST.get('amount')
        transfer_method = request.POST.get('transfer_method', 'IMPS').upper()
        purpose = request.POST.get('purpose', 'Personal')
        remarks = request.POST.get('remarks', '')

        if not (recipient_name and account_number and transfer_amount):
            messages.error(request, "All required fields must be filled.")
            return render(request, "profiles/money_transfer.html")

        try:
            account_number = int(account_number)
            transfer_amount = int(float(transfer_amount))
        except ValueError:
            messages.error(request, "Invalid account number or amount.")
            return render(request, "profiles/money_transfer.html")

        # Validate Sender
        try:
            sender_status = Status.objects.get(user_name=request.user.username)
        except Status.DoesNotExist:
            messages.error(request, "Sender account not found.")
            return render(request, "profiles/money_transfer.html")

        if sender_status.balance < transfer_amount:
            messages.error(request, "Insufficient balance.")
            return render(request, "profiles/money_transfer.html")

        # Validate Recipient
        try:
            recipient_status = Status.objects.get(account_number=account_number, user_name=recipient_name)
        except Status.DoesNotExist:
            messages.error(request, "Recipient account not found or name doesn't match.")
            return render(request, "profiles/money_transfer.html")

        # Perform Transfer
        sender_status.balance -= transfer_amount
        recipient_status.balance += transfer_amount
        sender_status.save()
        recipient_status.save()

        # Log Transaction
        models.MoneyTransfer.objects.create(
            recipient_name=recipient_name,
            recipient_account_number=account_number,
            transfer_amount=transfer_amount,
            transfer_method=transfer_method,
            purpose=purpose,
            remarks=remarks,
            date_of_transfer=datetime.date.today()
        )

        messages.success(request, "Money transferred successfully!")
        return redirect('profiles:money_transfer')

    return render(request, "profiles/money_transfer.html")

def loan(request):
    return render(request, "profiles/loans.html")

def ewallet(request):
    return render(request, "profiles/eWallet.html")

def online_pay(request):
    if request.method == "POST":
        recipient_upi_id = request.POST.get("recipient_upi_id", "").strip()
        payment_amount = request.POST.get("payment_amount", "").strip()
        description = request.POST.get("description", "").strip()

        upi_pattern = re.compile(r'^[\w.-]+@[\w.-]+$')
        errors = []

        if not recipient_upi_id or not upi_pattern.match(recipient_upi_id):
            errors.append("Invalid or empty UPI ID. Please enter a valid UPI ID like example@bank.")

        try:
            amount = int(payment_amount)
            if amount <= 0:
                errors.append("Payment amount must be greater than 0.")
        except ValueError:
            errors.append("Invalid payment amount. Please enter a valid number.")

        # Get sender's status entry
        try:
            sender_status = models.Status.objects.get(user_name=request.user.username)
        except models.Status.DoesNotExist:
            errors.append("Sender account status not found.")

        # Check if sender has enough balance
        if not errors and sender_status.balance < amount:
            errors.append("Insufficient balance for this transaction.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "profiles/online_payment.html", {
                "user": request.user.username,
                "form_data": {
                    "recipient_upi_id": recipient_upi_id,
                    "payment_amount": payment_amount,
                    "description": description,
                }
            })

        # Deduct balance from sender
        sender_status.balance -= amount
        sender_status.save()
        
        # Find recipient by UPI ID and credit amount
        try:
            recipient_status = models.Status.objects.get(upi_id=recipient_upi_id)
            recipient_status.balance += amount
            recipient_status.save()
        except models.Status.DoesNotExist:
            errors.append("Recipient account with this UPI ID does not exist.")
            # Refund sender balance
            sender_status.balance += amount
            sender_status.save()
            messages.error(request, "Recipient not found. Transaction cancelled and amount refunded.")
            return render(request, "profiles/online_payment.html", {
                "user": request.user.username,
                "form_data": {
                    "recipient_upi_id": recipient_upi_id,
                    "payment_amount": payment_amount,
                    "description": description,
                }
            })
        recipient_name = recipient_upi_id.split('@')[0]

        # Save to OnlinePayment
        models.OnlinePayment.objects.create(
            recipient_name=recipient_name,
            recipient_upi_id=recipient_upi_id,
            payment_amount=amount,
            description=description,
            date_of_payment=datetime.date.today()
        )
        # Save to RecentTransaction
        models.RecentTransaction.objects.create(
            sender_name=request.user.username,
            sender_account_number=sender_status.account_number,
            recipient_name=recipient_name,
            recipient_account_number=recipient_status.account_number,
            transfer_amount=amount,
            transfer_method="UPI",
            description=description or "UPI Payment",
            date_of_transfer=datetime.date.today()
        )
        
        
        messages.success(request, "Payment processed and transaction recorded successfully.")
        return redirect("profiles:online_pay")
    transactions = models.RecentTransaction.objects.filter(
        Q(sender_name=request.user.username) | Q(recipient_name=request.user.username)
    ).order_by("-date_of_transfer")[:10]
    
    return render(request, "profiles/online_payment.html", {
        "user": request.user.username, 
        "transactions": transactions,
    })

def settings(request):
    return render(request, "profiles/settings.html")

def edit_details(request):
    # Handle form submissions
    if request.method == "POST":
        # Basic Details Form
        if 'basic-form' in request.POST:
            try:
                # Update existing record
                basic = models.BasicDetails.objects.get(user_name=request.user)
                basic.name = request.POST.get('name')
                basic.sex = request.POST.get('sex')
                basic.annual_income = request.POST.get('annual_income')
                basic.email = request.POST.get('email')
                basic.mobile = request.POST.get('mobile')
                basic.occupation = request.POST.get('occupation')
                basic.DOB = request.POST.get('DOB')
                basic.save()
            except models.BasicDetails.DoesNotExist:
                # Create new record
                models.BasicDetails.objects.create(
                    user_name=request.user,
                    name=request.POST.get('name'),
                    sex=request.POST.get('sex'),
                    annual_income=request.POST.get('annual_income'),
                    email=request.POST.get('email'),
                    mobile=request.POST.get('mobile'),
                    occupation=request.POST.get('occupation'),
                    DOB=request.POST.get('DOB')
                )
            return redirect("profiles:account_status")

        # Present Location Form
        elif 'location-form' in request.POST:
            try:
                # Update existing record
                location = models.PresentLocation.objects.get(user_name=request.user)
                location.country = request.POST.get('country')
                location.state = request.POST.get('state')
                location.city = request.POST.get('city')
                location.street = request.POST.get('street')
                location.pincode = request.POST.get('pincode')
                location.save()
            except models.PresentLocation.DoesNotExist:
                # Create new record
                models.PresentLocation.objects.create(
                    user_name=request.user,
                    country=request.POST.get('country'),
                    state=request.POST.get('state'),
                    city=request.POST.get('city'),
                    street=request.POST.get('street'),
                    pincode=request.POST.get('pincode')
                )
            return redirect("profiles:edit_details")

    # GET request - show forms
    try:
        basic_details = models.BasicDetails.objects.get(user_name=request.user)
    except models.BasicDetails.DoesNotExist:
        basic_details = None

    try:
        location_details = models.PresentLocation.objects.get(user_name=request.user)
    except models.PresentLocation.DoesNotExist:
        location_details = None

    return render(request, "profiles/edit_details.html", {
        'basic_details': basic_details,
        'location_details': location_details
    })
        
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    return render(request, "profiles/delete_account.html")

def debit_cards(request):
    return render(request, "profiles/debit_card.html")

def credit_cards(request):
    return render(request, "profiles/credit_card.html")

def statement(request):
    return render(request, "profiles/statement.html")

def investment(request):
    return render(request, "profiles/investment.html")