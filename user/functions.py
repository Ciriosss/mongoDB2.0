from app.models import Profile, Order
from django.contrib.auth.models import User
import random


#function for create a new profile at registration moment
def newProfile(username):
    user = User.objects.get(username=username)
    initialBtc = round(random.uniform(1,10),2)
    BTC = initialBtc
    profile = Profile.objects.create(user=user, initialBtc=initialBtc, BTC=BTC, balance=0, pendingBalance = 0, pendingBTC = 0)
    profile.save()



def matchOrder(order, request):

    #matching buyorders
    if order.quantity > 0 :

        sellorders = Order.objects.filter(quantity__lte = 0 , price__lte=order.price, remaining__gt = 0).order_by('price')   #sales orders that have a price lower or equal than the purchase price
        user = User.objects.get(username=request.user)
        buyer = Profile.objects.get(user=user)

        if len(sellorders) > 0:
            i = 0

            # cycle to match orders until the order is fully matched or until there are no more offers
            while (order.remaining != 0) and (i <= ( len(sellorders) - 1)):
                sellorder = sellorders[i]
                profile = sellorder.profile
                seller = Profile.objects.get(id=profile.id)

                if order.remaining > sellorder.remaining:
                    buyer.pendingBalance -= float(order.price) * float(sellorder.remaining)
                    seller.balance += float(order.price) * float(sellorder.remaining)
                    buyer.BTC += sellorder.remaining
                    seller.pendingBTC -= sellorder.remaining
                    order.remaining -= sellorder.remaining
                    sellorder.remaining = 0
                    sellorder.save()
                    order.save()
                    buyer.save()
                    seller.save()
                    i += 1

                elif order.remaining == sellorder.remaining:
                    buyer.pendingBalance -= float(order.price) * float(order.remaining)
                    seller.balance += float(order.price) * float(order.remaining)
                    buyer.BTC += sellorder.remaining
                    seller.pendingBTC -= sellorder.remaining
                    sellorder.remaining = 0
                    order.remaining = 0
                    sellorder.save()
                    order.save()
                    buyer.save()
                    seller.save()
                    break

                elif order.remaining < sellorder.remaining:
                    buyer.pendingBalance -= float(order.price) * float(order.remaining)
                    seller.balance += float(order.price) * float(order.remaining)
                    buyer.BTC += order.remaining
                    seller.pendingBTC -= order.remaining
                    sellorder.remaining -= order.remaining
                    order.remaining = 0
                    sellorder.save()
                    order.save()
                    buyer.save()
                    seller.save()
                    break

    # matching sellorders
    else:
        # purchase orders that have a higher or equal price than the sell price
        buyorders = Order.objects.filter(quantity__gte = 0 ,remaining__gt = 0, price__gte=order.price).order_by('-price')
        user = User.objects.get(username=request.user)
        seller = Profile.objects.get(user=user)
        if len(buyorders) > 0:
            i = 0

            # cycle to match orders until the order is fully matched or until there are no more offers
            while (order.remaining != 0) and (i <= (len(buyorders) - 1)):
                buyorder = buyorders[i]
                profile = buyorder.profile
                buyer = Profile.objects.get(id=profile.id)

                if order.remaining > buyorder.remaining:
                    seller.balance += float(buyorder.price) * float(buyorder.remaining)
                    buyer.pendingBalance -= float(buyorder.price) * float(buyorder.remaining)
                    seller.pendingBTC -= buyorder.remaining, 4
                    buyer.BTC += buyorder.remaining
                    order.remaining -= buyorder.remaining
                    buyorder.remaining = 0
                    buyer.save()
                    seller.save()
                    buyorder.save()
                    order.save()
                    i += 1

                elif order.remaining == buyorder.remaining:
                    seller.balance += float(buyorder.price) * float(buyorder.remaining)
                    buyer.pendingBalance -= float(buyorder.price) * float(buyorder.remaining)
                    buyer.BTC += buyorder.remaining
                    seller.pendingBTC -= buyorder.remaining
                    buyorder.remaining = 0
                    order.remaining = 0
                    buyorder.save()
                    order.save()
                    buyer.save()
                    seller.save()
                    break

                elif order.remaining < buyorder.remaining:
                    seller.balance += float(buyorder.price) * float(order.remaining)
                    buyer.pending_balance -= float(buyorder.price) * float(buyorder.remaining)
                    buyer.BTC += order.remaining
                    seller.pending_BTC += order.remaining
                    buyorder.remaining -= order.remaining
                    order.remaining = 0
                    buyorder.save()
                    order.save()
                    break
