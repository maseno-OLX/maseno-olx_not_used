from django import forms
from . models import Item, category
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class upload_item(forms.ModelForm):


	class Meta:
		model = Item
		fields = ['item_name', 'item_description', 'item_price', 'item_image', 'item_category']

class update_item_category(forms.ModelForm):

	class Meta:
		model = category
		fields = ['category_name']
class update_item_description(forms.ModelForm):

	class Meta:
		model = Item
		fields = ['item_description', 'item_price', 'item_category']

	def clean_item_description(self):
		item_description= self.cleaned_data['item_description']
		return item_description[0].upper() + item_description[1:].lower()

	def clean_item_price(self):
		item_price = self.cleaned_data['item_price']
		return item_price

	def clean_item_category(self):
		item_category = self.cleaned_data['item_category']
		return item_category



