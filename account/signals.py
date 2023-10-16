from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    if created:  # Correct the condition to check 'created' - User
        # get the group customer and assign it to every new customer that signs up
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            email=instance.email,
            name=instance.username
        )
        print(Customer.objects.all())


# Connect the signal handler // when there is a User that is saved, call the method
post_save.connect(customer_profile, sender=User)
