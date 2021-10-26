from django.db import models
from datetime import timedelta, datetime

class Item_Master(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Brand_Master(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.name

class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, default="", blank=True)
    sub_category = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return self.name

class User_Master(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phn_no = models.CharField(max_length=10, blank=True)
    outlook_email = models.CharField(max_length=50, blank=True)
    gmail = models.CharField(max_length=50, blank=True)
    departments = models.ForeignKey(Department, blank=False, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

class item_status(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

class item_condition(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

class warranty_period(models.Model):
    status = models.CharField(max_length=20)

    if status == "1 year":
        datetime.today() + timedelta(365)

    if status == "2 year":
        datetime.today() + timedelta(365)


    def __str__(self):
        return self.status

class item_location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Vendor_Master(models.Model):
    name = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50)
    number = models.PositiveBigIntegerField()
    location = models.CharField(max_length=50)
    second_contact_person = models.CharField(max_length=50, blank=True, null=True)
    second_contact_person_number = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Order_Status(models.Model):
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.status

class Req_Approval(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class RequisitionForm(models.Model):
    req_number = models.AutoField(primary_key=True)
    req_Date = models.DateField(auto_now=True)
    user = models.CharField(max_length=50, default="")
    # user = models.ForeignKey(User_Master, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=50, default="")
    item = models.CharField(max_length=50, default="")
    capacity = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    qty = models.IntegerField(blank=True, default=1, null=True)
    item_image = models.ImageField(default="", blank=True)
    status = models.CharField(max_length=15, default="Pending", blank=True)
    
    def __str__(self):
        return str(self.req_number)

from datetime import date

class IT_Purchase(models.Model):
    purchase_id = models.BigAutoField(primary_key=True)
    date_of_purchase = models.DateField(auto_now=True)
    brand = models.CharField(max_length=35, default="")
    item_model = models.CharField(max_length=50, blank=True, null=True)
    item_serial_number = models.CharField(max_length=50, null=True, blank=True)
    Vendor = models.CharField(max_length=35, default="")
    warranty_period = models.CharField(max_length=35, default="")
    item_location = models.CharField(max_length=35, default="")
    purchase_qty = models.IntegerField()
    rec_status = models.CharField(max_length=15, default="Pending", blank=True, null=True)  #Recieving
    issue_status = models.CharField(max_length=15, default="Not Issued", blank=True, null=True)
    req = models.ForeignKey('RequisitionForm', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0)
    rec_qty = models.IntegerField(default=1, blank=True, null=True)
    issue_qty = models.IntegerField(default=1, blank=True, null=True)
    last_date_of_warranty = models.DateField(default="2021-09-13", blank=True,null=True)
    warranty_period_warning = models.CharField(default="", blank=True, max_length=100)

    def __str__(self):
        return str(self.purchase_id)

    def older_than_ten_days(self):
        return (self.last_date_of_warranty - date.today()).days < 10

class Purchase_Receiving(models.Model):
    date_of_receiving = models.DateField(auto_now=True)
    Bill_No = models.CharField(unique=True, max_length=20)
    pur = models.ForeignKey(IT_Purchase, on_delete=models.SET_NULL, null=True, blank=True)
    rec_qty = models.IntegerField(default=1, blank=True, null=True)
    purchase_price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Bill_No)
    
class Opening_Stock(models.Model):
    stock_id = models.BigAutoField(primary_key=True)
    item = models.CharField(max_length=50,default="")
    brand = models.CharField(max_length=50,default="")
    item_model = models.CharField(max_length=50, default=None, blank=True)
    Vendor = models.CharField(max_length=20, default="Opening Stock", blank=True)
    capacity = models.CharField(max_length=20, default=None,null=True, blank=True)
    version = models.CharField(max_length=50, default="", null=True, blank=True)
    item_location = models.CharField(max_length=50,default="")
    issued = models.CharField(max_length=15, default="Not Issued")
    qty = models.IntegerField()
    issue_qty = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return str(self.stock_id)

class Issued_to(models.Model):
    asset_id = models.AutoField(primary_key=True, unique=True)
    O_stock = models.ForeignKey(Opening_Stock,on_delete=models.CASCADE, blank=True, null=True, default="")
    purchase = models.ForeignKey(IT_Purchase,on_delete=models.CASCADE, blank=True, null=True, default="")
    Users = models.ForeignKey(User_Master, on_delete=models.CASCADE, default=1)
    date_of_issue = models.DateField(auto_now=True)
    issue_qty = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return str(self.asset_id)

    class Meta:
        unique_together = (("O_stock", "purchase", "Users"))

# class Stock(models.Model):
