from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.forms import inlineformset_factory #way to create multiple forms within 1 form
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #flashmsg
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #u can use mixins also
from django.contrib.auth.models import Group #default

from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only


# Create your views here.
@unauthenticated_user
def registerPage(request):
	
	form=CreateUserForm()
	if request.method=='POST':
		form=CreateUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			#django signals will handle the following 
			#group=Group.objects.get(name='customers') # get the grp
			#user.groups.add(group)  auto set group to customers whenever a user registers
			# Customer.objects.create( #create a new customer whenever a user registers
			# 	user=user,
			# 	name=user.username,
			# 	)
			messages.success(request,"Registered Successfully!! "+username)
			return redirect('login')
	context={'form':form}
	return render(request,"accounts/register.html",context)

@unauthenticated_user
def loginPage(request):
	
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None: #if the user is actually present
			login(request,user)
			return redirect('home')
		else :
			messages.info(request,"Incrrect info")
	context={}
	return render(request,"accounts/login.html",context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')  #if user is not logged in redirect to login
@admin_only #if user is admin keep at home page else send to userpage
def home(request):
	orders=Order.objects.all()
	customers=Customer.objects.all()
	total_customers=customers.count()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='Pending').count()
	context={
	'orders':orders,'customers':customers,
	'total_orders':total_orders,
	'delivered':delivered,
	'pending':pending
	}
	return render(request,"accounts/dashboard.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles='customers')
def userPage(request):
	orders=request.user.customer.order_set.all() #since user is related to customer(onetoone) and chain down for customer to get order
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='Pending').count()
	context={
	'orders':orders,
	'total_orders':total_orders,
	'delivered':delivered,
	'pending':pending
	}
	return render(request,'accounts/user.html',context)

	
@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def products(request):
	products=Product.objects.all()
	return render(request,"accounts/products.html",{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def customer(request,pk):
	customer=Customer.objects.get(id=pk)
	orders=customer.order_set.all()
	orders_count=orders.count()
	myFilter=OrderFilter(request.GET,queryset=orders)
	orders=myFilter.qs
	context={
	'customer':customer,'orders':orders,'orders_count':orders_count,'myFilter':myFilter
	}
	return render(request,"accounts/customer.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def createOrder(request,pk):#pk of customer //DIFFICULTY ADD
	customer=Customer.objects.get(id=pk)
	#parent model,childmodel
	OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=4) 
	formset=OrderFormSet(queryset=Order.objects.none(),instance=customer) #order.objects.none : dont display any obj initially
	
	#form=OrderForm(initial={'customer':customer}) //prefill the customer col
	if request.method=='POST':
		#form=OrderForm(request.POST) //send the data to the form
		formset=OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save() #automatically saves the order in db
			return redirect('/')

	context={
	'formset':formset,'customer':customer

	}
	return render(request,"accounts/order_form.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def updateOrder(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order) #prefill with prev values
	if request.method=='POST':
		form=OrderForm(request.POST,instance=order)#prevent createing a new form obj
		if form.is_valid():
			form.save() #automatically saves the order in db
			return redirect('/')
			
	context={
	'form':form

	}
	return render(request,"accounts/order_form.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def deleteOrder(request,pk):
	order=Order.objects.get(id=pk)
	if request.method=='POST':
		order.delete()
		return redirect('/')


	context={'item':order}
	return render(request,"accounts/delete.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer) #whenevr files are sent use requesr.FILES
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)


