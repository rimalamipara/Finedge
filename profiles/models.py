from django.db import models
import datetime

class BasicDetails (models.Model):
    # (Name, Sex, DOB, Annual income, Email, Mobile number, Occupation) 
    name = models.CharField(max_length = 50, default = None)  # Name of the user
    sex = models.CharField(max_length = 1, default = None) 
    annual_income = models.IntegerField(default = 0)  # Annual income of the user
    email = models.EmailField(default = None)  # Email address
    mobile = models.IntegerField(default = 0) # Mobile number
    occupation = models.CharField(max_length = 50, default = None) 
    DOB = models.DateField(default = None) # Date of Birth 
    user_name = models.CharField(max_length = 150, default = None)  # Username for the user
    
    def __str__(self):
        return f"{self.name}"

class PresentLocation (models.Model):
    # (Country, State, City, Street, Pincode) 
    country = models.CharField(max_length = 50, default = "India") # Default country is India
    state = models.CharField(max_length = 50) 
    city = models.CharField(max_length = 50)    
    street = models.CharField(max_length = 50) 
    pincode = models.IntegerField()
    user_name = models.CharField(max_length = 150, default = None)
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country} - {self.pincode}"

class Status (models.Model):
    account_number = models.IntegerField(unique=True)  # Unique account number
    balance = models.IntegerField()
    user_name = models.CharField(max_length=150, default=None)
    upi_id = models.CharField(max_length=100, editable=False)

    def save(self):
        # Ensure upi_id is based on current user_name
        if self.user_name:
            self.upi_id = f"{self.user_name}@finedge"
        super().save()

    def __str__(self):
        return f"Account: {self.account_number}, Balance: {self.balance} INR, UPI ID: {self.upi_id}"

class MoneyTransfer(models.Model):
    recipient_name= models.CharField(max_length = 50, default = None)  # Name of the recipient
    recipient_account_number= models.IntegerField()  # Account number of the recipient
    transfer_amount = models.IntegerField()  # Amount to be transferred
    transfer_method = models.CharField(max_length = 20)  # Method of transfer (e.g., IMPS, NEFT)
    purpose= models.CharField(max_length = 100, default="null")  # Purpose of transfer
    date_of_transfer = models.DateField(default = datetime.date.today)  # Date of transfer
    remarks= models.CharField(max_length = 200, blank = True, null = True)  # Optional remarks
    
    def __str__(self):
        return f"Transfer to {self.recipient_name} ({self.recipient_account_number}) of amount {self.transfer_amount} INR on {self.date_of_transfer}"
    
class OnlinePayment(models.Model):
    recipient_name = models.CharField(max_length=100, default="Unknown")
    recipient_upi_id = models.CharField(max_length=100)  # UPI ID of the recipient
    payment_amount = models.IntegerField()  # Amount to be paid
    description = models.CharField(max_length = 200, blank = True, null = True)  # Optional remarks
    date_of_payment = models.DateField(default=datetime.date.today)  # Date of payment
    def __str__(self):
        return f"Payment of {self.payment_amount} INR to {self.recipient_upi_id} on {self.date_of_payment}"
    
class RecentTransaction(models.Model):
    sender_name = models.CharField(max_length=50, default=None)  # Name of the sender
    sender_account_number = models.IntegerField()  # Account number of the sender
    recipient_name = models.CharField(max_length=50, default=None)  # Name of the recipient
    recipient_account_number = models.IntegerField()  # Account number of the recipient
    transfer_amount = models.IntegerField()  # Amount transferred
    transfer_method = models.CharField(max_length=20)  # Method of transfer
    description = models.CharField(max_length=100, default="null")  # Purpose of transfer
    date_of_transfer = models.DateField(default=datetime.date.today)  # Date of transfer
    
    def __str__(self):
        return f"Transaction of amount {self.transfer_amount} INR on {self.date_of_transfer}"