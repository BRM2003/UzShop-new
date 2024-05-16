from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/panel/', admin.site.urls, name='admin'),
    path('login_user/', views.login_user, name='login'),
    path('logout', views.logout, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('control/', views.control_page, name='control'),
    path('control/reqs', views.orders_page, name='control'),
    path('control/reqs/change/order', views.change_status),
    path('control/operators', views.operator_page),
    path('control/admins', views.admins_page)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)