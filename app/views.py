from django.shortcuts import render
from .models import Order, Profile

# home views
def home(request):
    return render(request,'app/home.html', {})


#view to determine the profile of users, and to comment on their activities
def profit(request):
    profiles = Profile.objects.all()
    if request.GET.get('profile'):
        id = request.GET.get('profile')
        profile = Profile.objects.get(id=id)
        revenues = 0
        costs = 0
        profit = 0

        buyorders = Order.objects.filter(quantity__gte = 0,profile=profile)
        sellorders = Order.objects.filter(quantity__lte = 0,profile=profile)

        if (len(sellorders) == 0) and (len(buyorders) == 0):
            profit = 0.0
            message = 'This user has not performed any transactions yet '

        elif (len(sellorders) > 0) and (len(buyorders) == 0):
            for sellorder in sellorders:
                revenues += ((abs(sellorder.quantity) - sellorder.remaining) * (sellorder.price))
            profit = revenues
            message = 'This user has only placed sales orders'

        elif (len(sellorders) == 0) and (len(buyorders) > 0):
            for buyorder in buyorders:
                costs += ((buyorder.quantity * buyorder.price) - (buyorder.remaining * buyorder.price))
            profit -= costs
            message = 'This user has only placed buy orders, he never sold'

        else:
            message = 'This user has a very active account'
            for sellorder in sellorders:
                revenues += ((abs(sellorder.quantity) - sellorder.remaining) * (sellorder.price))

            for buyorder in buyorders:
                costs += ((buyorder.quantity * buyorder.price) - (buyorder.remaining * buyorder.price))
            profit = revenues - costs
        return render(request, 'app/profit.html',{'profiles': profiles, 'profit': profit , 'id': id, 'message': message})

    return render(request, 'app/profit.html', {'profiles': profiles})



#view to return all orders that are still open
def orderBook(request):
    buyorders = Order.objects.filter(quantity__gte = 0,remaining__gt = 0)
    sellorders = Order.objects.filter(quantity__lte = 0,remaining__gt = 0)
    for order in sellorders:
        order.quantity = abs(order.quantity)
    return render(request, 'app/orderBook.html', {'buyorders' : buyorders, 'sellorders' : sellorders})