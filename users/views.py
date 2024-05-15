import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response

from .forms import *

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
from .forms import *
from .models import Admins
from goods.models import *
from claims.models import *


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(form)
    else:
        form = SignupForm()
    response = {'form': form}
    return render(request, 'authenticate/sign_up.html', response)


@csrf_exempt
def login_user(request):
    response = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'page_return' in request.POST:
                page_return = request.POST['page_return']
                if page_return == '':
                    if Admins.objects.filter(user=user).exists():
                        page_return = 'control'
                    else:
                        page_return = '/shop'
            else:
                if Admins.objects.filter(user=user).exists():
                    page_return = 'control'
                else:
                    page_return = '/shop'
            return redirect(page_return)
        else:
            messages.success(request, "Error")
            return render(request, 'authenticate/login.html', {'error': 'Username or Password is incorrect'})
    else:
        response['page_return'] = request.GET.get('page_return', '')
        print(response['page_return'])
    return render(request, 'authenticate/login.html', response)


@permission_classes([IsAuthenticated])
def control_page(request):
    response = {}
    try:
        if Admins.objects.filter(user=request.user).exists():
            if request.method == 'POST':
                pr_category = GoodsCategory.objects.get(id=request.POST['category'])
                form = GoodsForm(request.POST, request.FILES)
                if form.is_valid():
                    product = Goods.objects.create(title=request.POST['title'],
                                                   category=pr_category,
                                                   description=request.POST['description'],
                                                   amount=request.POST['amount'],
                                                   price_for_admin=request.POST['price_for_admin'],
                                                   currency='UZS',
                                                   photo=request.FILES['photo'],
                                                   cr_by=request.user)
                    product.save()
            response['form'] = GoodsForm()
            admin = Admins.objects.get(user=request.user)
            response['admin'] = admin
            response['count_of_orders'] = len(Orders.objects.all())
            # response['categories'] = GoodsCategory.objects.all()
        else:
            response['error'] = 100
            response['message'] = "you don't have access"
            return redirect('login')
    except Exception as e:
        print(str(e))
    return render(request, 'admin/main.html', response)


@permission_classes([IsAuthenticated])
def orders_page(request):
    response = {}
    try:
        if Admins.objects.filter(user=request.user).exists():
            if request.method == 'GET':
                orders_filter = request.GET.get('filter', '')
                region_filter = request.GET.get('region', '')
                search_by_id = request.GET.get('searchById', '')
                search_by_phone = request.GET.get('searchByPhone', '')
                if search_by_phone != '':
                    response['orders'] = Orders.objects.filter(user__phone_number=search_by_phone)
                elif search_by_id != '':
                    response['orders'] = Orders.objects.filter(order_id=search_by_id)
                elif orders_filter != '':
                    response['orders'] = Orders.objects.filter(status=orders_filter)
                elif region_filter != '':
                    response['orders'] = Orders.objects.filter(region=region_filter)
                else:
                    response['orders'] = Orders.objects.all()
                if len(response['orders']) > 0:
                    response['count_of_orders'] = len(response['orders'])
                else:
                    response['count_of_orders'] = 0
            else:
                if request.POST['change_status']:
                    order = Orders.objects.get(order_id=request.POST['order'])
                    if request.POST['UpdateForm[status]'] != 0:
                        order.status = request.POST['UpdateForm[status]']
                    order.operator = request.POST['operator']
                    order.save()
                response['orders'] = Orders.objects.all()
                response['count_of_orders'] = len(response['orders'])
            if request.user.is_superuser:
                response['super_user'] = True
                response['admin_list'] = Admins.objects.all()
            else:
                response['super_user'] = False
        else:
            return redirect('login')
    except Exception as e:
        print(str(e))
        response['success'] = False
        response['error_message'] = str(e)
    return render(request, 'admin/orders.html', response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_status(request):
    response = {}
    try:
        if Admins.objects.filter(user=request.user).exists():
            data = request.data
            response['success'] = True
            response['orders'] = Orders.objects.all()
            response['count_of_orders'] = len(response['orders'])
            admin = Admins.objects.get(id=data['UpdateForm[admin]'])
            if Orders.objects.filter(order_id=data['order']).exists():
                order = Orders.objects.get(order_id=data['order'])
                order.region = data['viloyat']
                order.status = data['UpdateForm[status]']
                order.admin = admin
                order.count_of_products = data['quant']
                order.total_amount = data['summa']
                order.comment = data['UpdateForm[comment]']
                order.up_on = datetime.datetime.now()
                order.save()
            else:
                response['success'] = False
                response['error'] = 'there is no order'
        else:
            return redirect('login')
    except Exception as e:
        response['success'] = False
        response['error'] = str(e)
    return render(request, 'admin/orders.html', response)


@permission_classes([IsAuthenticated])
def operator_page(request):
    def count_of_claims(filter_value, operator_id):
        result = Orders.objects.filter(operator=operator_id, status=filter_value)
        return result
    response = {'table': {}}
    try:
        if Admins.objects.filter(user=request.user).exists():
            all_operators = Operators.objects.all()
            for operator in all_operators:
                response['table']['operator_' + str(operator.user.id) + ' (' + str(operator.user.username) + ')'] = {}
                for stat in [1, 2, 3, 6, 8, 4, 7]:
                    orders_result = count_of_claims(stat, operator.user.id)
                    response['table']['operator_' + str(operator.user.id) + ' (' + str(operator.user.username) + ')']['orders_len_' + str(stat)] = len(orders_result)
        else:
            return redirect('login')
    except Exception as e:
        print(str(e))
    return render(request, 'admin/operators.html', response)


@permission_classes([IsAuthenticated])
def admins_page(request):
    def count_of_claims(filter_value, adm):
        result = Orders.objects.filter(admin=adm, status=filter_value)
        return result

    def get_all_amount(adm):
        local_orders = Orders.objects.filter(admin=adm)
        result = 0
        for order in local_orders:
            result += order.total_amount
        return result

    response = {'table': {}}
    try:
        if Admins.objects.filter(user=request.user).exists():
            admins = Admins.objects.all()
            for admin in admins:
                response['table']['admin_' + str(admin.id)] = {}
                response['table']['admin_' + str(admin.id)]['admin_name'] = admin
                for stat in range(10):
                    orders_result = count_of_claims(stat + 1, admin)
                    response['table']['admin_' + str(admin.id)]['orders_len_' + str(stat+1)] = len(orders_result)
                response['table']['admin_' + str(admin.id)]['total_amount'] = get_all_amount(admin)
        else:
            return redirect('login')
    except Exception as e:
        print(str(e))
        response['success'] = False
        response['error_message'] = str(e)
    return render(request, 'admin/admins.html', response)


@permission_classes([IsAuthenticated])
def logout(request):
    try:
        logout(request)
    except Exception as e:
        print(str(e))
    return redirect('/shop')
