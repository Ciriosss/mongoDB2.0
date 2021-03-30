from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initialBtc = models.FloatField()
    BTC = models.FloatField()
    balance = models.FloatField()
    pendingBalance = models.FloatField()    #money spent on bitcoin but not yet matched with other orders
    pendingBTC = models.FloatField()        #BTC spent  but not yet matched with other orders

                                            # useful to avoid double expenses

class Order(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    quantity = models.FloatField()
    remaining = models.FloatField()     #remaining quantity to consider the order closed
