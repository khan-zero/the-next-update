from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Goods import models


@login_required(login_url='login') #user authenficatsiyadan otganini ishon hosil qilish
def myCart(request):
        cart = models.Cart.objects.get(
            author=request.user, 
            is_active=True)
        context = {}
        context['cart']=cart
        return render(request, 'user/cart/detail.html')
    
    

@login_required(login_url='login')
def addProductToCart(request):

    code = request.GET.get('code')
    quantity = request.GET.get('quantity', 1)

    # integer ligiga tkshirib olish
    quantity = int(quantity)
    if quantity < 1:

        return redirect('error/')

    product = get_object_or_404(models.Product, generate_code=code)
    cart, _ = models.Cart.objects.get_or_create(author=request.user, is_active=True)
    cart_product, created = models.CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}  # Default quantity cart products uchun
    )
    # agar mahsulot bor bolsa uni yangilash
    if not created:
        cart_product.quantity += quantity
        cart_product.save()


    return redirect('main/')


@login_required(login_url='login')
def substractProductFromCart(request):
    code = request.GET.get('code')
    quantity = int(request.GET.get('quantity', 1))
    product_cart = get_object_or_404(models.CartProduct, product__generate_code=code, cart__author=request.user)

    if quantity > product_cart.quantity:
        # kozinkadagi mahsulot bazdagidan ozligiga tekshirish
        return redirect('error/')

    product_cart.quantity -= quantity
    product_cart.save()
    
    if product_cart.quantity <= 0:
        product_cart.delete()

    return redirect('main/')

@login_required(login_url='login')
def deleteProductCart(request):
    code = request.GET['code']
    product_cart = models.CartProduct.objects.get(generate_code=code)
    product_cart.delete()
    return redirect('cart/')


def CreateOrder(request):
    cart = models.Cart.objects.get(
        generate_code = request.GET['generate_code']
        )
    
    cart_products = models.CartProduct.objects.filter(cart=cart)

    done_products = []

    for cart_product in cart_products:
        if cart_product.quantity <= cart_product.product.quantity:
            cart_product.product.quantity -= cart_product.quantity
            cart_product.product.save()
            done_products.append(cart_product)
        else:
            for product in done_products:
                product.product.quantity += product.quantity
                product.product.save()
            raise ValueError('Qoldiqda kamchilik')

    models.Order.objects.create(
        cart=cart,
        full_name = f"{request.user.first_name}, {request.user.last_name}",
        email = request.user.email,
        phone = request.GET['phone'],
        address = request.GET['address'],
        status = 1
        )
    cart.is_active = False
    cart.save()
    
    return redirect('main/')
