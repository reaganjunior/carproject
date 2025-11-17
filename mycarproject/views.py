from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, CarForm, ContactForm, OrderForm, AdminForm
from .models import Car, Brand, ContactMessage, Order, Admin

def home(request):
    mycarproject = Car.objects.all()
    return render(request, 'mycarproject/home.html', {'mycarproject': mycarproject})


def cars(request):
    data = Car.objects.all()

    name = request.GET.get('name')
    transmission = request.GET.get('transmission')
    fuel_type = request.GET.get('fuel_type')
    color = request.GET.get('color')
    year = request.GET.get('year')

    highlighted_id = None

    # If all filters are present, try to find a car that matches all of them
    if name and transmission and fuel_type and color and year:
        try:
            result = Car.objects.get(
                name__icontains=name,
                transmission__iexact=transmission,
                fuel_type__iexact=fuel_type,
                color__iexact=color,
                year=year
            )
            highlighted_id = result.id
        except Car.DoesNotExist:
            highlighted_id = None

    return render(request, 'mycarproject/cars.html', {
        'data': data,
        'highlighted_id': highlighted_id
    })




def add_car(request):
    """ Always show the admin password form first """
    if request.method == 'POST' and not request.session.get('is_admin_authenticated', False):
        form = AdminForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['admin_password'] == 'admin1234':
                request.session['is_admin_authenticated'] = True
                return redirect('add_car')
            else:
                messages.error(request, 'Incorrect admin password.')
    elif not request.session.get('is_admin_authenticated', False):
        request.session['is_admin_authenticated'] = False  # Force re-authentication
        form = AdminForm()
        return render(request, 'mycarproject/admin_password.html', {'form': form})

    # Once authenticated, show the form
    form = CarForm()
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['is_admin_authenticated'] = False  # Reset auth after use
            return redirect('cars')

    return render(request, 'mycarproject/add_car.html', {'form': form})





def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            number = form.cleaned_data['number']
            message = form.cleaned_data['message']


            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                subject=subject,
                number=number,
                message=message
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'mycarproject/contact.html', {'form': form})


def dashboard(request):
    """ Always show the admin password form first """
    if request.method == 'POST' and not request.session.get('is_admin_authenticated', False):
        form = AdminForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['admin_password'] == 'admin1234':
                request.session['is_admin_authenticated'] = True
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect admin password.')
    elif not request.session.get('is_admin_authenticated', False):
        request.session['is_admin_authenticated'] = False  # Force re-authentication
        form = AdminForm()
        return render(request, 'mycarproject/admin_password.html', {'form': form})

    
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # Reset auth after dashboard is loaded
    request.session['is_admin_authenticated'] = False

    return render(request, 'mycarproject/dashboard.html', {
        
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    })


@require_POST
def mark_delivered(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = 'Delivered'
    order.save()
    return redirect('dashboard')


def create_customer(request):
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            #data=Customer.objects.get(id=1)
            return redirect('one')
    else:
        form = CustomerForm()
    return render(request, 'mycarproject/create_customer.html', {'form': form})

def customer_page(request):
    data=Customer.objects.get(id=id)
    return render(request,'mycarproject/x.html')


def create_order_with_details(request, id):
    car = Car.objects.get(id=id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
       
            order = form.save(commit=False)
            order.status = 'Pending' 
            order.customer = request.user
            order.save()
            return redirect('cars')
    else:
        '''
        initial_data = {
            'name': car.name,
            'price': car.price,
            'location': car.location,
            'fuel_type': car.fuel_type,
            'mileage': car.mileage,
            'transmission': car.transmission,
            'color': car.color,
            'year': car.year,
            'photo': car.photo,
        }'
        '''
        form = OrderForm(instance=car)
    
    return render(request, 'mycarproject/create_order.html', {'form': form,'data':car})



def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)  # Change Car to Order
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    return render(request, 'mycarproject/update.html', {'form': form})

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    return render(request, 'mycarproject/confirm_delete.html', {'order': order})



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Password mismatch')
            return redirect('/register')  # Keep it consistent with your URL pattern
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already in use')
            return redirect('/register')
        else:
            user1 = User.objects.create_user(username=username, email=email, password=password2)
            user1.save()
            return redirect('/login')  # Redirect to your login page

    return render(request, 'mycarproject/register.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        data = authenticate(request, username=username, password=password)
        if data is not None:
            login(request, data)
            messages.success(request, 'Logged in successfully')
            return redirect('home')  # ✅ correct URL name from your urls.py
        else:
            messages.error(request, 'Provide correct credentials')
            return redirect('login')  # ✅ cleaned up redirect
    return render(request, 'mycarproject/login.html')


def logout_view(request):
    logout(request)

    messages.info(request, "You have successfully logged out.")

    return redirect('home')