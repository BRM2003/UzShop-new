from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.response import Response

from .models import *


@csrf_exempt
def change_status(request):
    try:
        # status = request.POST['status']
        # print(order_list)
        for order in request.POST:
            if order != 'status':
                orders = Orders.objects.get(order_id=request.POST[order])
                orders.status = request.POST['status']
                orders.save()
        return redirect('control')
    except Exception as e:
        print(str(e))
        return redirect('control')
