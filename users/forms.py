from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, FileInput, CharField, PasswordInput
from goods.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class GoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'category', 'description', 'amount', 'price_for_admin', 'photo']

        widgets = {
            "title": TextInput(attrs={
                'name': "pr_name",
                'class': "form-control",
                'placeholder': "Mahsulot Nomi",
                'required': ""
            }),
            "category": Select(attrs={
                'name': "pr_category",
                'class': "form-control"
            },),
            "description": Textarea(attrs={
                'name':  "pr_about",
                'class': "form-control",
                'placeholder': "Mahsulot Haqida malumot",
                'required': ""
            }),
            "amount": NumberInput(attrs={
                'name': "pr_price",
                'class':"form-control",
                "placeholder": "Mahsulot Narxi",
                "required": ""
            }),
            "price_for_admin": NumberInput(attrs={
                'name': "pr_admin_price",
                'class': "form-control",
                "placeholder": "Admin uchun To'lov",
                "required": ""
            }),
            "photo": FileInput(attrs={
                'name': "pr_media",
                'accept': "video/*,image/*"
            }),
        }


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    widgets = {
        "password": PasswordInput(attrs={
            'placeholder': "Parol",
            'required': ""
        }),
    }
