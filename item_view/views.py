from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .forms import upload_item, update_item_description
#from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View,CreateView
from .models import Item, category
from bootstrap_modal_forms.generic import BSModalCreateView
from django.views.generic.edit import UpdateView

from django.contrib.auth import logout

def welcome_page(request):
	recommended_uploded_items = Item.objects.all().order_by('-date_created')[10:16]
	recently_uploded_items = Item.objects.all().order_by('-date_created')[:12]
	featured_uploded_items = Item.objects.all().order_by('-date_created')[17:23]
	categories = category.objects.all()

	return render(request, "admin_template/item_image.html", {'featured_uploded_items': featured_uploded_items, 'recently_uploded_items': recently_uploded_items, 'recommended_uploded_items': recommended_uploded_items, 'category': categories})


#View for the cateories page
#Login is required to view the cateories page





@login_required(login_url='authentication:sign_in')
def upload_product(request):
	if request.method == 'POST':
		form = upload_item(request.POST, request.FILES)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Successfully uploaded")
			print('data saved')

			return HttpResponseRedirect(instance.get_absolute_url())
		else:

			print('form is not valid')

	form = upload_item()

	return render(request, "upload.html", {'form': form})


def item_list(request):
	uploded_items = Item.objects.all()

	return render(request, 'item_list.html', {'items': uploded_items})


def item_detail(request, name):
		instance = get_object_or_404(Item, item_name=name)
		form = update_item_description(request.POST or None, instance=instance)
		if request.method == "post":
			if form.is_valid():
				form.save(commit=False)

				item_description_changed = form.cleaned_data['item_description']
				item_price = form.cleaned_data['item_price']
				item_category = form.cleaned_data['item_category']




				instance.update(item_description=item_description_changed)



		uploaded_item = get_object_or_404(Item, item_name=name)
		same_category_items = Item.objects.all().filter(item_category=uploaded_item.item_category)[:6]
		#same_seller_items = Item.objects.all().filter(item_owner=request.user)
		categories = category.objects.all()
		return render(request, 'admin_template/item_detail.html', {'item': uploaded_item, 'form': form ,'category':
		categories,'same_category_items': same_category_items})


def categories(request, category_name):
	categorized_items = Item.objects.all().filter(item_category=category_name)


	categories = category.objects.all()
	return render(request, 'admin_template/category.html', {'item': categorized_items, 'category': categories})


class UploadView(LoginRequiredMixin, View):
		login_url = 'authentication:sign_in'
		form_class = upload_item
		template_name = 'admin_template/upload.html'

		def get(self, request):
			form = self.form_class(None)
			return render(request, self.template_name, {'form': form})

		def post(self, request):
			form = self.form_class(request.POST, request.FILES)
			if form.is_valid:
				instance = form.save(commit=False)

				user = form.save(commit=False)
				user.item_owner = request.user
				user.save()
				instance.save()

				messages.success(request, "Successfully uploaded")

				print("data saved")

				return HttpResponseRedirect(instance.get_absolute_url())

			else:

				print('form is valid')

			return render(request, self.template_name, {'form': form})


@login_required(login_url='authentication:sign_in')
def upload_item(request):
	if request.method == 'POST':
		form = upload_item(request.POST, request.FILES)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
		else:

			print('form is not valid')

	form = upload_item()

	return render(request, 'upload.html', {'form': form})

@login_required(login_url='authentication:sign_in')
def profile(request):
	return render(request, 'admin_template/profile.html')

def header(request):
	return render(request, 'admin_template/header.html')




