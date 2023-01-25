from django.db.models.signals import post_save, post_delete    # send a message/signal after save or delete in this checkout app 
from django.dispatch import receiver   #this receives the messages 

from .models import OrderLineItem    # specifying what/where we ar elistening for the save or delet 

@receiver(post_save, sender=OrderLineItem)             # we are receiving signals form save on the orderlineitems   do the below 
def update_on_save(sender, instance, created, **kwargs):     #kwargs -- keyword arguments 
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()

@receiver(post_delete, sender=OrderLineItem)
def update_on_save(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()