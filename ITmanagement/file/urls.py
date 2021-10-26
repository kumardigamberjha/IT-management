from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('user-status/', views.user_status, name="user-status"),
    path('IT-Purchase/', views.Purchase_Item, name="IT-Purchase"),
    path('User-requisition/', views.User_requisition, name="user-requisition"),

    path('user-values/<id>/', views.user_value, name="user-value"),
    path('Issued-items/', views.Issued_To, name="issued"),
    path('show-all-status/', views.Opening_Stocks, name="show-all-items"),
    path("SignUp/", views.Signup_view, name="signup"),
    path('login/', views.Login_view, name="login"),
    path('logout/', views.Logout_view, name="logout"),
    path('purchase_form/<req_number>/', views.Purchase_Form, name="IT-form"),
    path('opening_stock_form/', views.Opening_Stock_FormView, name="opening_stock_form"),
    path('requisition-form/', views.User_requisition_form, name="requistion-form"),
    path('receiving-form/<purchase_id>', views.Receiving_Item_Form, name="receiving-form"),
    path('All_Purchase/', views.All_Purchased_Item, name="all_purchase"),
    path('Purchase_Issue_Item_form/<purchase_id>', views.Purchase_Issue_Form, name="purchase_issue_form"),
    path('Stock_Issue_Item_form/<stock_id>', views.Stock_Issue_Form, name="stock_issue_form"),
    path('total_stock/', views.Total_Stock, name="total_stock"),
    
    # path('Trace_order/', views.Order_trace, name="trace-order"),
    # path('Update_form/<req_number>/', views.Edit_User_Requisition, name="update-user-requisition-form"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)