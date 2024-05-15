from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from goods.models import *
from claims.models import *


@csrf_exempt
def main_shop_page(request):
    response = {}
    try:
        if request.method == 'GET':
            categories = []
            goods = []
            category = request.GET.get('category', '')
            search = request.GET.get('search', '')
            response['order'] = request.GET.get('order', '')
            if category != '':
                selected_categories = []
                for el in category.split('^'):
                    selected_category = GoodsCategory.objects.get(title=el)
                    selected_categories.append(el)
                    for obj in Goods.objects.filter(category=selected_category.id, title__contains=search):
                        goods.append(obj)
                response['goods'] = goods
                response['selected_categories'] = selected_categories
            elif category == '' and search != '':
                for obj in Goods.objects.filter(title__contains=search):
                    goods.append(obj)
                response['goods'] = goods
            else:
                response['goods'] = Goods.objects.all().reverse()
            # get all categories
            for category in GoodsCategory.objects.all():
                categories.append(category.title)
                response['categories'] = categories
        if request.user.is_authenticated:
            response['authenticated'] = True
            if Admins.objects.filter(user=request.user).exists():
                response['admin'] = True
        else:
            response['authenticated'] = False
    except Exception as e:
        response['success'] = True
        response['error_message'] = ['Error', str(e)]
    return render(request, 'shop/main_shop.html', response)


def product_page(request):
    response = {}
    try:
        if request.method == 'GET':
            product_id = request.GET.get('num', '#')
            if int(product_id) != '#':
                product = Goods.objects.get(id=product_id)
                response['product'] = product
        else:
            product = Goods.objects.get(id=request.POST['product_id'])
            # client_user = Clients.objects.get(user=request.user)
            new_order = Orders.objects.create(user_name=request.POST['user_name'],
                                              user_phone_number=request.POST['phone_number'],
                                              product=product,
                                              status=1)
            new_order.save()
            return redirect('/shop?order=success')
        if request.user.is_authenticated:
            response['authenticated'] = True
        else:
            response['authenticated'] = False
    except Exception as e:
        print(str(e))
        response['success'] = False
        response['error_message'] = ['Error', str(e)]
    return render(request, 'shop/product_buy.html', response)
