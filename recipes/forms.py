from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Step, Recipe

class RecipeForm(forms.Form):
    delicacy = forms.CharField(label='料理名稱', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'delicacy', 'placeholder': '例如: 茶凍'}))
    introduction = forms.CharField(label='料理簡介', max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'introduction', 'placeholder': '例如: 微甜、口感扎實的茶凍'}))
    delicacy_photo = forms.ImageField(label='料理圖片', required=False, widget=forms.FileInput(attrs={'class': 'form-control form-control-sm', 'id': 'delicacy_photo', 'placeholder': 'delicacy_photo'}))
    DELICACY_TYPE_CHOICES = (
        ('a', '開胃菜(appetizer)'),
        ('m', '主餐(main course)'),
        ('sf', '主食(staple food)'),
        ('sd', '副菜(side dish)'),
        ('d', '甜點(dessert)'),
        ('b', '飲品(beverages)'),
    )
    delicacy_type = forms.ChoiceField(label='料理類型', choices=DELICACY_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'id': 'introduction', 'placeholder': 'delicacy_type'}))
    CATEGORY_CHOICES=(
        ('m','葷(meat)'),
        ('v','純素(vegan)'),
        ('o','蛋奶素(ovo-lacto vegetarian)'),
        ('f','五辛素(Five pungent spices vegan)'),
    )
    category = forms.ChoiceField(label='葷素', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'id': 'introduction', 'placeholder': 'category'}))
    cooking_time = forms.IntegerField(label='料理時間', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'cooking_time', 'placeholder': 'cooking_time'}))
    servings = forms.IntegerField(label='幾人份', widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'servings', 'placeholder': 'servings'}))
    reference = forms.CharField(label='參考來源', max_length=1000, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'reference', 'placeholder': 'reference'}))
    memo_text = forms.CharField(label='溫馨提醒', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'memo_text', 'placeholder': 'memo_text'}))
    storage_method = forms.CharField(label='保存方法', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'storage_method', 'placeholder': 'storage_method'}))


class MethodForm(forms.Form):
    step = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    step_photo = forms.ImageField(label='圖片', required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'step_photo', 'placeholder': 'step_photo'}))
    description = forms.CharField(label='描述', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'placeholder': '例如: 將食材放如容器中'}))
    notes = forms.CharField(label='溫馨提醒', max_length=1000, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'notes', 'placeholder': '例如: 如果使用XX食材會更好吃唷～'}))


        
