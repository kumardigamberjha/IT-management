import re
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Brand_Master, Department, Item_Master, Opening_Stock, IT_Purchase, Purchase_Receiving, User_Master, Issued_to, RequisitionForm, Vendor_Master, item_location, warranty_period
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, IT_Purchase_form,Purchase_Issue_Item_Form, Item_Receiving_Form, Opening_Stock_form, UserRequisitionForm, Stock_Issue_Item_Form
from .filters import IssuedToFilters
from datetime import timedelta, datetime

# Matplotlib
import matplotlib.pyplot as plt


def index(request):
    purchase = Opening_Stock.objects.all()

    context = {'data': purchase}
    return render(request, 'file/index.html', context)

def user_status(request):
    detail = Issued_to.objects.all()
    f = IssuedToFilters(request.POST, queryset=detail)

    name = ""
    if request.method == "POST":
        name = request.POST.get('user')
    print(name)
    context = {'filter': f, "name": name, 'detail': detail}
    return render(request, 'file/user-status.html', context)

def user_value(request, id):
    purchase = Issued_to.objects.get(asset_id=id)

    context = {'data': purchase}
    return render(request, 'file/user_value.html', context)

def Opening_Stocks(request):
    data = Opening_Stock.objects.all()
    context = {'data':data}
    return render(request, 'file/opening-stock.html', context)

def Logout_view(request):
    logout(request)
    return redirect('login')


def Signup_view(request):
    form = CreateUserForm()
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if request.method=='POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            user = form.cleaned_data.get("username")
            messages.success(request, "Account created for "+ user+ " succesfully")
            return redirect('login')

    return render(request, 'file/signup.html', {'form':form})

def Login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            messages.info(request, 'Invalid username/password')

    return render(request, 'file/login.html')


def Opening_Stock_FormView(request):
    item = Item_Master.objects.all()
    brand = Brand_Master.objects.all()
    vendor = Vendor_Master.objects.all()
    location = item_location.objects.all()
    form = Opening_Stock_form()

    if request.method == "POST":
        form = Opening_Stock_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('show-all-items')

    context = {'form':form, 'item': item, 'brand': brand, 'vendor': vendor, 'location': location}
    return render(request, "file/opening_stock_form.html",context)

def User_requisition_form(request):
    userss = User_Master.objects.all()
    item_master = Item_Master.objects.all()
    department = Department.objects.all()
    
    form = UserRequisitionForm()
    print(request.POST)
    if request.method == "POST":
        form = UserRequisitionForm(request.POST)

        if form.is_valid():
            print("Saved")
            form.save()
            return redirect('user-requisition')

    context = {'form':form, "user": userss, "item": item_master, "department": department}

    return render(request, 'file/user-requisition-form.html', context)

data1 = []
purchase1 = []

def User_requisition(request):
    data = RequisitionForm.objects.all()
    pur = IT_Purchase.objects.all()
    
    context = {"data": data, 'pur':pur, 'data1':data1, 'purchase1':purchase1}
    return render(request, 'file/Requisition_display.html', context)

p_warranty_period = ""
def Purchase_Form(request, req_number):
    data = RequisitionForm.objects.get(req_number = req_number)
    brand = Brand_Master.objects.all()
    vendor = Vendor_Master.objects.all()
    location = item_location.objects.all()
    w_period = warranty_period.objects.all()
    global p_warranty_period
    form = IT_Purchase_form()
    if request.method == "POST":

        form = IT_Purchase_form(request.POST)
        purchase_qty = request.POST.get('purchase_qty')
        qty1 = request.POST.get('qty1')
        price = request.POST.get('price')
        p_warranty_period = request.POST.get('warranty_period')
        # last_date_of_warranty = request.POST.get('last_date_of_warranty')
        # print("Last Date Of Warranty: ", last_date_of_warranty)
        print(p_warranty_period)
        print(purchase_qty)
        print("qty1: ", qty1)
        print(request.POST)
        if form.is_valid():
            datas = form.save(commit=False)
            left_qty = int(qty1) - int(purchase_qty)
            if left_qty <= 0:
                RequisitionForm.objects.filter(req_number = req_number).update(status = "Purchased")
            
            RequisitionForm.objects.filter(req_number = req_number).update(qty=left_qty)
            
            datas.save()
            print("Saved")
            return redirect("IT-Purchase")
            
    context = {'form':form, 'data': data, 'brand':brand, 'w_period': w_period, 'location':location, 'vendor': vendor}
    return render(request, "file/purchase_form.html",context)

def Purchase_Item(request):
    data = IT_Purchase.objects.all()
    context = {'data': data}
    return render(request, 'file/purchase.html', context)

def Receiving_Item_Form(request, purchase_id):
    data = IT_Purchase.objects.get(purchase_id = purchase_id)
    form = Item_Receiving_Form()

    if request.method == "POST":
        rec_qty = request.POST.get('rec_qty')
        pur_qty = request.POST.get('pur_qty')
        Bill_No = request.POST.get('Bill_NO')
        item_price = request.POST.get('purchase_price')

        form = Item_Receiving_Form(request.POST)
        print('p',pur_qty)
        print('i',rec_qty)
        print("item_price ", item_price)
        print(request.POST)
        if form.is_valid():
            left_qty = int(pur_qty) - int(rec_qty)
            print(left_qty)
            if left_qty <= 0:
                IT_Purchase.objects.filter(purchase_id = purchase_id).update(rec_status = "Recieved")

            global p_warranty_period
            print(p_warranty_period)
            if p_warranty_period == "1 year":
                today_data = datetime.today() + timedelta(365)

                IT_Purchase.objects.filter(purchase_id = purchase_id).update(last_date_of_warranty = today_data)

            IT_Purchase.objects.filter(purchase_id = purchase_id).update(purchase_qty = left_qty)
            IT_Purchase.objects.filter(purchase_id = purchase_id).update(rec_qty = rec_qty)

            form.save()

            print("Saved")
            return redirect("IT-Purchase")
            
    context = {'form':form, 'data': data}
    return render(request, 'file/item_receiving.html', context)

def All_Purchased_Item(request):
    data = Purchase_Receiving.objects.all()
    context = {'data': data}
    return render(request, 'file/all_purchase.html', context)

def Stock_Issue_Form(request, stock_id):
    stock = Opening_Stock.objects.get(stock_id = stock_id)
    form = Stock_Issue_Item_Form()

    if request.method == "POST":
        form = Stock_Issue_Item_Form(request.POST)
        issue_qty = request.POST.get('issue_qty')
        qty = request.POST.get('qty')

        print(issue_qty)
        print(qty)
        print(request.POST)
        if form.is_valid():
            left_qty = int(qty) - int(issue_qty)
            print(left_qty)
            if left_qty <= 0:
                Opening_Stock.objects.filter(stock_id = stock_id).update(issued = "Issued")

            Opening_Stock.objects.filter(stock_id = stock_id).update(qty = left_qty)
            Opening_Stock.objects.filter(stock_id = stock_id).update(issue_qty = issue_qty)

            form.save()

            print("Saved")
            return redirect("index")
            
    context = {'form':form, 'stock': stock}

    return render(request, 'file/stock_issue_form.html', context)

def Purchase_Issue_Form(request, purchase_id):
    stock = IT_Purchase.objects.get(purchase_id = purchase_id)
    form = Purchase_Issue_Item_Form()

    if request.method == "POST":
        form = Purchase_Issue_Item_Form(request.POST)
        issue_qty = request.POST.get('issue_qty')
        rec_qty = request.POST.get('rec_qty')

        print(issue_qty)
        print(request.POST)
        if form.is_valid():
            left_qty = int(rec_qty) - int(issue_qty)
            print(left_qty)
            if left_qty <= 0:
                IT_Purchase.objects.filter(purchase_id = purchase_id).update(rec_status = "Recieved")

            IT_Purchase.objects.filter(purchase_id = purchase_id).update(issue_qty = issue_qty)
            IT_Purchase.objects.filter(purchase_id = purchase_id).update(rec_qty = left_qty)

            form.save()

            print("Saved")
            return redirect("index")
            
    context = {'form':form, 'stock': stock}

    return render(request, 'file/purchase_issue_form.html', context)

def Issued_To(request):
    issued = Issued_to.objects.all()
    context = {'issued': issued}
    return render(request, 'file/issued.html', context)

def Total_Stock(request):
    pur = Purchase_Receiving.objects.all()
    stock = Opening_Stock.objects.all()
    context = {'pur': pur, 'stock': stock}
    return render(request, 'file/stock.html', context)