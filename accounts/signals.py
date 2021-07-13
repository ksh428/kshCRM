from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Customer

#create the customer model and add to customer grp whenever a user registers
def customer_profile(sender, instance, created, **kwargs): #instance is the user
	if created:
		group = Group.objects.get(name='customers')
		instance.groups.add(group)
		Customer.objects.create(
			user=instance,
			name=instance.username,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)

#while using signals always modify the apps.py file

