from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,NewOrder
from app.models import Profile, Order
from django.contrib.auth.models import User
from .functions import newProfile, matchOrder
from .request import price


#view for registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Congratulations {}! your account has been created successfully, now you are able to log-in'.format(username))
            newProfile(username)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})



#view for profile pageorder
def profile(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    buyorders = Order.objects.filter(profile = profile, quantity__gt = 0).order_by('-datetime')
    sellorders = Order.objects.filter(profile=profile, quantity__lt=0).order_by('-datetime')
    balance = round(profile.balance,2)
    BTC = round(profile.BTC,2)
    for order in sellorders:
        order.quantity = abs(order.quantity)
        order.remaining = abs(order.remaining)
    return render(request, 'user/profile.html', {'user' : user, 'profile' : profile,'buyorders' : buyorders, 'sellorders' : sellorders, 'balance' : balance, 'BTC' : BTC})


#view for trade page
def trade(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    balance = round(profile.balance, 2)
    BTC = round(profile.BTC, 2)
    actualBtc = (round(price() * 0.84, 2))  #calling function that sand a request to determinate the actual price og bitcoin according coinMarketCap

    if request.method == 'POST':
        form = NewOrder(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.profile = profile

            #checking if the order a sell order
            if ('sell' in request.POST):
                # checking if the user has BTC to make the exchange
                if order.quantity > profile.BTC:
                    messages.warning(request, 'Error, you dont have enough bitcoins ')
                    return redirect('trade')
                else:
                    order.remaining = order.quantity
                    order.quantity = (order.quantity) * (-1)
                    profile.pendingBTC += abs(order.quantity)
                    profile.BTC += order.quantity
                    profile.save()
            # buy order
            else:
                # checking if the user has money to make the exchange
                if (float(order.quantity) * float(order.price)) > profile.balance:
                    messages.warning(request, 'Error, you dont have enough founds ')
                    return redirect('trade')
                else:
                    order.remaining = order.quantity
                    profile.pendingBalance += order.price * order.quantity
                    profile.balance -= order.price * order.quantity
                    profile.save()

            order.save()
            messages.success(request,'Congratulations!your order has been registered ')
            matchOrder(order,request)  #calling the function that match orders with others
            return redirect('profile')
    else :
        form = NewOrder()
    return render(request, 'user/trade.html', {'form' : form,'balance' : balance, 'BTC' : BTC, 'actualBtc' : actualBtc})