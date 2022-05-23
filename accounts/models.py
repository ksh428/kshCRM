from django.db import models
#pass:12345 ,name:kshounish
# Create your models here.
from django.contrib.auth.models import User

#always use null=true when updating a model
class Customer(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE) # a customer will be related to exactly 1 user
	name=models.CharField(max_length=200,null=True)
	phone=models.CharField(max_length=200,null=True)
	profile_pic=models.ImageField(default="lfc.jpg",null=True,blank=True)
	email=models.CharField(max_length=200,null=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True) #take the current time
	def __str__(self):
		return self.name

class Tag(models.Model):
	name=models.CharField(max_length=200,null=True)
	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY=(
		('Indoor','Indoor'),
		('Outdoor','Outdoor'),
		)
	name=models.CharField(max_length=200,null=True)
	price=models.FloatField(null=True)
	description=models.CharField(max_length=200,null=True,blank=True)
	category=models.CharField(max_length=200,null=True,choices=CATEGORY)
	date_created=models.DateTimeField(auto_now_add=True,null=True)
	tags=models.ManyToManyField(Tag)  #return all peoducts with tag of sports   #Product.ojects.filter(tags__name="Sports")
	def __str__(self):
		return self.name

class Order(models.Model):  
	STATUS=(
		('Pending','Pending'),
		('Out for Delivery','Out for Delivery'),
		('Delivered','Delivered'),
		)
	customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)#many to one :many this order can have many customers
	product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL) 
	date_created=models.DateTimeField(auto_now_add=True,null=True)
	status=models.CharField(max_length=200,null=True,choices=STATUS)
	def __str__(self):
		return self.product.name

