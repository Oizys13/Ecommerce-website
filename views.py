
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from xhtml2pdf import pisa
from django.template.loader import get_template




def search(request):
    categorys = Category.objects.all()
    products = Product.objects.all()
    sizes = Size.objects.all()
    context = {'products':products, 'categorys':categorys, 'sizes':sizes}

  

    if request.method == 'POST':
        searched = request.POST['searched'].upper()
        filtered = request.POST['filtered'].upper()
        prix_min = request.POST['maxprice']
        prix_max = request.POST['maxprice']
        



        if (searched !='' and searched is not None) and (filtered != '' and filtered is not None) and (prix_min !='' and prix_min is not None) and (prix_max !='' and prix_max is not None):
            prix_min = int(prix_min)
            prix_max = int(prix_max)
            products = Product.objects.filter(size__name = filtered)
            products = products.filter(name__icontains = searched)
            products = products.filter(price__gte = prix_min)
            products = products.filter(price__lte = prix_max)



        elif (searched !='' and searched is not None):
            products = Product.objects.filter(name__icontains = searched)
            if (prix_min !='' and prix_min is not None):
                prix_min = int(prix_min)
                products = products.filter(price__gte = prix_min)
            if (prix_max !='' and prix_max is not None):
                prix_max = int(prix_max)
                products = products.filter(price__lte = prix_max)





        elif(filtered != '' and filtered is not None):
            products = Product.objects.filter(size__name = filtered)
            if (prix_min !='' and prix_min is not None):
                prix_min = int(prix_min)
                products = products.filter(price__gte = prix_min)
            if (prix_max !='' and prix_max is not None):
                prix_max = int(prix_max)
                products = products.filter(price__lte = prix_max)


        elif (prix_max !='' and prix_max is not None) and (prix_min !='' and prix_min is not None):
            prix_max = int(prix_max)
            prix_min = int(prix_min)
            products = products.filter(price__lte = prix_max)
            products = products.filter(price__gte = prix_min)

        elif (prix_max !='' and prix_max is not None):
            prix_max = int(prix_max)
            products = products.filter(price__lte = prix_max)  

        elif (prix_min !='' and prix_min is not None):
            prix_min = int(prix_min)
            products = products.filter(price__gte = prix_min)              






    context = {'products':products, 'categorys':categorys, 'sizes':sizes}


    return render(request, 'base/shop.html', context)





def home(request):
    categorys = Category.objects.all()
    products = Product.objects.filter(sold = False)
    if request.method == 'POST':
        searched = request.POST['searched'].upper()
        if (searched !='' and searched is not None):
            products = Product.objects.filter(name__icontains = searched)

    context = {'products':products, 'categorys':categorys}
    return render(request, 'base/index.html', context)

def man(request):
    # filter fucntion only takes integer values as arguments
    # due to the order in which the gender values were introduced to the database (woman, man, kids) we have :
    # man = 1
    # woman = 2
    # kids = 3
    products = Product.objects.filter(gender = 1).filter(sold = False)
    categorys = Category.objects.exclude(name = 'Robes')


    context = {'products':products, 'categorys':categorys}
    return render(request, 'base/homme.html', context)

def woman(request):
    products = Product.objects.filter(gender = 2).filter(sold = False)
    categorys = Category.objects.all()
    context = {'products':products, 'categorys':categorys}
    return render(request, 'base/femme.html', context)

def kids(request):
    products = Product.objects.filter(gender = 3).filter(sold = False)
    categorys = Category.objects.all()
    context = {'products':products, 'categorys':categorys}
    return render(request, 'base/enfant.html', context)


def product(request, pk):

    product = Product.objects.get(id=pk)
    context= {'product' : product}
    return render(request, 'base/product.html',context)

@login_required(login_url='login')

def Sell(request):
    initial_data={
        'publisher': request.user  
    }
    form = SellForm(initial=initial_data)
    if (request.method == 'POST'):
        form = SellForm(request.POST, request.FILES)
        if form.is_valid():
            if (request.POST['category'] == "Chaussures") and (request.POST['pointure'] == '' or request.POST['pointure'] is None):
                messages.error(request, "please specify pointure")
            else:    
                product = form.save(commit=False)
                form.user = request.user
                product.save()
                return redirect('Home')
    context = {'form':form}
    return render(request, 'base/vendre.html', context)



@login_required()
def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = SellForm(instance=product)
    if request.user != product.publisher:
        return redirect('Home')
    else:   
        if request.method=='POST':
            form = SellForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('Home')
    context = {'form' : form}    
    return render(request, 'base/update.html', context)

@login_required()
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    context= {'product' : product}
    if request.user != product.publisher:
        return redirect('Home')
    else: 
        if request.method == 'POST':
            product.delete()
            return redirect('Home')
    return render(request, 'base/404.html',context)      


def loginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None :
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Incorrect password')



    context = {}
    return render(request,'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('Home')






def register(request):
    users = User.objects.all()
    form = loginForm()
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Welcome to your new account')
            return redirect('Home') 
        else:
            if request.POST['password1'] != request.POST['password2']:
                messages.error(request,'passwords does not match')    
            for user in users :
                if request.POST['username']== user.username:
                    messages.error(request,'Username already exists')    
            for user in users :
                if request.POST['email']== user.email:
                    messages.error(request,'email already exists')   

    return render(request, 'base/register.html', {'form': form})




@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id = pk)
    
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone']
         
        if first_name != '' and first_name is not None :
            user.first_name = first_name
        if last_name != '' and last_name is not None :
            user.last_name = last_name
        if username != '' and first_name is not None :
            user.username = username
        if email != '' and email is not None :
            user.email = email
        if phone_number != '' and phone_number is not None :
            user.phone = phone_number
        user.save() 



       




    products = Product.objects.filter(publisher= user)

    context = {'products':products}
    return render(request, 'base/My account.html', context)


@login_required()
def cart_add(request, id):
    products = get_object_or_404(Product, id=id)
    if products.cart.filter(id=request.user.id).exists():
        products.cart.remove(request.user)
    else:
        products.cart.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])        



@login_required()
def cart_list(request):
    products = Product.objects.filter(cart=request.user).filter(sold=False)
    if request.method == 'POST':
        for product in products:
            product.sold = True
            product.save()
    return render(request, 'base/cart.html', {'products':products})

@login_required()
def wishlist_add(request, id):
    products = get_object_or_404(Product, id=id)
    if products.wishlist.filter(id=request.user.id).exists():
        products.wishlist.remove(request.user)
    else:
        products.wishlist.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])        



@login_required()
def wish_list(request):
    products = Product.objects.filter(wishlist=request.user).filter(sold=False)
    return render(request, 'base/wishlist.html', {'products':products})

def contact1(request):
    if request.method == "POST" :
         nom=request.POST.get('name'),
         email=request.POST.get('email'),
         subject=request.POST.get('subject'),
         message=request.POST.get('message'),
         data = {
            'name1': nom,
            'email1': email,
            'subject1': subject,
            'message1': message
         }
         message='''
                Nouveau message de la part de : {}
                Email: {}
                message : {}  
         '''.format(data['name1'],data['email1'],data['message1'])  
         send_mail(data['subject1'],message,'',['clexetin@gmail.com'])     
    return render(request, 'base/contact1.html',{}) 
    
def form(request):
    return render(request,'base/form.html')  
def dashboard(request):
    produits=Product
    context={ 
              'nbr_robe_femme':Product.objects.filter(gender__name='Femme').filter(category__name='Robes').count(),
              'robe':Category.objects.get(name='Robes'),
              'nbr_pontalon_femme':Product.objects.filter(gender__name='Femme').filter(category__name='Pontalon').count(),
              'pontalon':Category.objects.get(name='Pontalon'),
              'nbr_Tishrt_femme':Product.objects.filter(gender__name='Homme').filter(category__name='Shirts').count(),
              'Tishrt':Category.objects.get(name='Shirts'),
              'nbr_veste_femme':Product.objects.filter(gender__name='Femme').filter(category__name='veste').count(),
              'veste':Category.objects.get(name='veste'),

              'nbr_robe_enfant':Product.objects.filter(gender__name='Enfant').filter(category__name='Robes').count(),
              'robe':Category.objects.get(name='Robes'),
              'nbr_pontalon_enfant':Product.objects.filter(gender__name='Enfant').filter(category__name='Pontalon').count(),
              'pontalon':Category.objects.get(name='Pontalon'),
              'nbr_Tishrt_enfant':Product.objects.filter(gender__name='Enfant').filter(category__name='Shirts').count(),
              'Tishrt':Category.objects.get(name='Shirts'),
              'nbr_veste_enfant':Product.objects.filter(gender__name='Enfant').filter(category__name='veste').count(),
              'veste':Category.objects.get(name='veste'),

              'nbr_pontalon_homme':Product.objects.filter(gender__name='Homme').filter(category__name='Pontalon').count(),
              'pontalon':Category.objects.get(name='Pontalon'),
              'nbr_Tishrt_homme':Product.objects.filter(gender__name='Homme').filter(category__name='Shirt').count(),
              'Tishrt':Category.objects.get(name='Shirts'),
              'nbr_veste_homme':Product.objects.filter(gender__name='Homme').filter(category__name='veste').count(),
              'veste':Category.objects.get(name='veste'),

              'nbr_femme':Product.objects.filter(gender__name='Femme').count(),
              'femme':Gender.objects.get(name='Femme'),

              'nbr_homme':Product.objects.filter(gender__name='Homme').count(),
              'homme':Gender.objects.get(name='Homme'),

              'nbr_enfant':Product.objects.filter(gender__name='Enfant').count(),
              'enfant':Gender.objects.get(name='Enfant'),

    }
    return render(request,'base/dashboard.html',context)    

def admin_profile(request, pk):
    return render(request, 'base/profile.html')


def admin_page(request, pk):
    users = User.objects.all()
    products = Product.objects.all()
    context = {'users':users, 'products':products}
    return render (request, 'base/admin.html', context)    


def show_form(request):
    products = Product.objects.filter(cart=request.user)
    return render(request,'base/form.html', {'products':products})


def pdf_report_creat(request):
        products = Product.objects.filter(cart=request.user)
        template_path = 'base/pdfForm.html'
        context = {'products': products}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="products_report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


    
def us(request):
    return render(request,'base/about.html')