from django.shortcuts import render,redirect,get_object_or_404
from ecomapp.models import *
import json
import razorpay
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse


# Create your views here.
def footer(request):
	return render(request,"footer.html")

def navbar(request):
	return render(request,"navbarnew.html")

def show(request):
	var=Dummy.objects.all()
	return render(request,"show.html",{"data":var})

def faq1(request):
	var=faq.objects.all()
	return render(request,"faq.html",{"data":var})

def contact(request):
	if request.method=="POST":
		nm=request.POST.get("n")
		em=request.POST.get("e")
		ms=request.POST.get("ms")
		ph=request.POST.get("ph")
		x=Mycontact()
		x.name=nm
		x.email=em
		x.message=ms
		x.phone_no=ph
		x.save()
		return render(request,"contactus.html")
	else:
		return render(request,"contactus.html")

	return render(request,"contactus.html")


def register(request):
	if request.method=="POST":
		fn=request.POST.get("n")
		ln=request.POST.get("l")
		em=request.POST.get("e")
		ps=request.POST.get("p")
		rtp=request.POST.get("rp")
		if ps==rtp:
			if Register1.objects.filter(email=em).exists():
		 		return render(request,"Registerpage.html",{"msg":3})
			else:
			    x=Register1()
			    x.first_name=fn
			    x.last_name=ln
			    x.email=em
			    x.password=ps
			    x.retype_password=rtp
			    x.save()
			    return render(request,"Registerpage.html",{"msg":1})
		else:
			return render(request,"Registerpage.html",{"msg":2})
	else:
		return render(request,"Registerpage.html")


def login(request):
	if request.method=="POST":
		em=request.POST.get("e")
		pa=request.POST.get("p")
		if Register1.objects.filter(email=em,password=pa).exists():
			request.session['email']=em
			return redirect("homepage")
		else:
			return render(request,"Loginpage.html",{"msg":"invalid credentials"})
	else:
		return render(request,"Loginpage.html")


def myprofile(request):
    user_email = request.session.get('email')
    if not user_email:
        return redirect('/login')
    user_data=Register1.objects.get(email=request.session["email"])
    return render(request,"myprofile.html",{"data":user_data})

def changepassword(request):
    user_email = request.session.get('email')
    if not user_email:
        return redirect('/login')
    if request.method=="POST":
        o=request.POST.get("op")
        n=request.POST.get("np")
        c=request.POST.get("cp")
        if n==c:
            user_data=Register1.objects.get(email=request.session["email"])
            ori=user_data.password
            if o==ori:
                user_data.password=n
                user_data.retype_password=n
                user_data.save()
                return render(request,"changepassword.html",{"msg":"password change Successfully"})
            else:
                return render(request,"changepassword.html",{"msg":"Invalid Password"})
        else:
            return render(request,"changepassword.html",{"msg":"password and confirm password does not match"})
    else:
        return render(request,"changepassword.html")


def editprofile(request):
    user_email = request.session.get('email')
    if not user_email:
        return redirect('/login')
    user_data=Register1.objects.get(email=request.session["email"])
    if request.method=="POST":
        fn=request.POST.get("fn")
        ln=request.POST.get("ln")
        ph=request.POST.get("pn")
        add=request.POST.get("a")
        lm=request.POST.get("lm")
        hn=request.POST.get("hf")
        pc=request.POST.get("p")
        user_data.first_name=fn
        user_data.last_name=ln
        user_data.phone_no=ph
        user_data.address=add
        user_data.landmark=lm
        user_data.house_flat_no=hn
        user_data.pincode=pc
        user_data.save()
        return redirect("/myprofile")
    return render(request,"editprofile.html",{"data":user_data})


def categories(request):
	res=Category.objects.all()
	return render(request,"categories.html",{"data":res})

def showproduct(request, name):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '').strip()

    products_qs = products.objects.filter(category_name=name)

    if query:
        products_qs = products_qs.filter(Title__icontains=query)

    if sort == 'low':
        products_qs = products_qs.order_by('unit_price')
    elif sort == 'high':
        products_qs = products_qs.order_by('-unit_price')

    no_results = not products_qs.exists()

    return render(request, "showproduct.html", {
        "data": products_qs,
        "category_name": name,
        "no_results": no_results
    })



def productdetail(request, name, title):
    product = get_object_or_404(products, Title=title, category_name__category_name=name)

    if request.method == "POST":
        user_email = request.session.get('email')
        if not user_email:
            return redirect('/login')

        user = Register1.objects.get(email=user_email)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('/cart')  # 🔁 Redirect to cart instead of select-shipping

    return render(request, "showdetail.html", {"data": product})




# Add to Cart View (Simple Version)
def add_to_cart(request):
    if request.method == "POST":
        # 1. Get user from session
        user_email = request.session.get('email')
        if not user_email:
            return redirect('/login')  # Redirect to login if not logged in

        user = Register1.objects.get(email=user_email)

        # 2. Get product using Title (you can switch to product id if you want)
        product_title = request.POST.get('product_id')
        product = products.objects.get(Title=product_title)

        # 3. Check if product already in cart, else add new
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        print(cart_item)
        print(created)

        if not created:
            # Already exists, increase quantity
            cart_item.quantity += 1
            cart_item.save()

        return redirect('/cart')  # Redirect to cart page after adding
    else:
        return redirect('/')  # In case someone opens /add_to_cart directly


def view_cart(request):
	user_email = request.session.get('email')
	if not user_email:
		return redirect('/login')

	user = Register1.objects.get(email=user_email)

	# 2. Fetch all cart items for this user
	cart_items = Cart.objects.filter(user=user)
	shipping = ShippingAddress.objects.filter(user=user, is_primary=True).first()

	overall_total = sum(item.product.unit_price * item.quantity for item in cart_items)

	return render(request, 'cart.html', {'cart_items': cart_items, 'overall_total': overall_total, 'shipping': shipping})

def remove_from_cart(request,product_title):
	user_email = request.session.get('email')
	if not user_email:
		return redirect('/login')

	user = Register1.objects.get(email=user_email)
	product = products.objects.get(Title=product_title)

	Cart.objects.filter(user=user, product=product).delete()

	return redirect('/cart')
from django.shortcuts import get_object_or_404

# Increment Quantity
def increment_quantity(request, product_title):
    if request.method == "POST":
        user_email = request.session.get('email')
        if not user_email:
            return redirect('/login')

        user = Register1.objects.get(email=user_email)
        product = products.objects.get(Title=product_title)
        cart_item = get_object_or_404(Cart, user=user, product=product)
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart')


# Decrement Quantity
def decrement_quantity(request, product_title):
    if request.method == 'POST':
        user_email = request.session.get('email')
        if not user_email:
            return redirect('/login')

        user = Register1.objects.get(email=user_email)
        product = products.objects.get(Title=product_title)

        cart_item = get_object_or_404(Cart, user=user, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # if quantity is 1, remove item from cart

    return redirect('/cart')

def clear_cart(request):
	if request.method == "POST":
		user_email = request.session.get('email')
		if not user_email:
			return redirect('/login')

		user = Register1.objects.get(email=user_email)
		Cart.objects.filter(user=user).delete()

	return redirect('/cart')

	    
def sidebar(request):
	return render(request,'sidebar.html')

def logout(request):
	if not request.session.has_key('email'):
		return redirect('/login')
	del request.session['email']
	return redirect('/login')

def forgetpassword(request):
	if request.method == 'POST':
		email = request.POST.get('em')

		# Check if user exists using 'exists()'
		if Register1.objects.filter(email=email).exists():
			user = Register1.objects.get(email=email)
			password = user.password

			# Send Password via Email
			subject = "your password Recovery"
			message = f"Dear User,\n\n Your password is: {future@1226}\n\nPlease keep it secure."
			email_from = setting. EMAIL_HOST_USER	
			recipient_list = [email]
			send_mail(subject, message, email_from, recipient_list)

			return render(request,'forgetpassword.html',{'msg': "your password has been sent to your email"})

		else:
			return render(request,'forgetpassword.html',{'error': "This email is not registered"})

	return render(request,'forgetpassword.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def select_shipping(request):
    user_email = request.session.get("email")
    if not user_email:
        return redirect('/login')

    user = Register1.objects.get(email=user_email)

    if not Cart.objects.filter(user=user).exists():
        return redirect('/cart')

    addresses = ShippingAddress.objects.filter(user=user)

    if request.method == "POST":
        selected_address_id = request.POST.get("address_id")
        if not selected_address_id:
            return render(request, "select_shipping.html", {
                "addresses": addresses,
                "error": "Please select a shipping address."
            })

        request.session["selected_address_id"] = selected_address_id
        return redirect('/create_order/')

    return render(request, "select_shipping.html", {"addresses": addresses})




RAZORPAY_KEY_ID = "rzp_test_q10M6Qqv26cAcF"

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, ""))  # No secret key needed

def create_order(request):
    try:
        user_email = request.session.get("email")
        if not user_email:
            return redirect("/login")

        user = Register1.objects.get(email=user_email)
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return redirect("/cart")

        selected_id = request.session.get("selected_address_id")
        shipping = ShippingAddress.objects.filter(user=user, id=selected_id).first()
        if not shipping:
            return redirect("/select-shipping")

        total_amount = sum(item.product.unit_price * item.quantity for item in cart_items) * 100

        return render(request, "payment.html", {
            "razorpay_key": RAZORPAY_KEY_ID,
            "amount": total_amount // 100,
            "shipping": shipping,
            "cart_items": cart_items  #added this
        })

    except Exception as e:
        return render(request, "error.html", {"message": str(e)})



def save_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = request.session.get("email")
            if not user_email:
                return JsonResponse({"error": "User not logged in"}, status=401)

            user = Register1.objects.get(email=user_email)
            print(user)
            payment_id = data.get("payment_id")
            print(payment_id)
            raw_amount = data.get("amount")  # Razorpay sends in paisa
            status = data.get("status")

            # Convert paisa to rupees safely
            try:
                amount = Decimal(str(raw_amount)) / 100
            except InvalidOperation as e:
                return JsonResponse({"error": f"Invalid amount value: {str(e)}"}, status=400)

            if not all([payment_id, amount, status]):
                return JsonResponse({"error": "Missing payment data"}, status=400)
            print("Hello")
            # Save payment
            payment = Payment.objects.create(
                user=user,
                payment_id=payment_id,
                amount=amount,
                status=status
            )

            # Save cart items to OrderItem
            cart_items = Cart.objects.filter(user=user)
            for item in cart_items:
                OrderItem.objects.create(
                    payment=payment,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price
                )

            # Clear cart
            cart_items.delete()

            return JsonResponse({"message": "Payment and order recorded successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def order_history(request):
    user_email = request.session.get("email")
    if not user_email:
        return redirect('/login')

    user = Register1.objects.get(email=user_email)
    payments = Payment.objects.filter(user=user, status="Success").order_by("-created_at")
    print(payments)

    return render(request, "order_history.html", {"payments": payments})

from django.contrib import messages


def manage_addresses(request):
    user_email = request.session.get("email")
    if not user_email:
        return redirect('/login')

    user = Register1.objects.get(email=user_email)
    next_url = request.GET.get("next")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip_code = request.POST.get("zip_code")
            phone = request.POST.get("phone")
            address_type = request.POST.get("address_type")
            is_primary = request.POST.get("is_primary") == "on"

            if is_primary:
                ShippingAddress.objects.filter(user=user).update(is_primary=False)

            ShippingAddress.objects.create(
                user=user,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                phone=phone,
                address_type=address_type,
                is_primary=is_primary
            )
            messages.success(request, "Address added successfully!")

        elif action == "delete":
            addr_id = request.POST.get("address_id")
            ShippingAddress.objects.filter(id=addr_id, user=user).delete()
            messages.success(request, "Address deleted successfully!")

        elif action == "edit":
            addr_id = request.POST.get("address_id")
            address = ShippingAddress.objects.get(id=addr_id, user=user)
            address.address = request.POST.get("address")
            address.city = request.POST.get("city")
            address.state = request.POST.get("state")
            address.zip_code = request.POST.get("zip_code")
            address.phone = request.POST.get("phone")
            address.address_type = request.POST.get("address_type")
            is_primary = request.POST.get("is_primary") == "on"
            if is_primary:
                ShippingAddress.objects.filter(user=user).update(is_primary=False)
            address.is_primary = is_primary
            address.save()
            messages.success(request, "Address updated successfully!")
        if next_url:
        	return redirect(f"/addresses/?next={next_url}")
        else:
        	return redirect("/addresses/")


    addresses = ShippingAddress.objects.filter(user=user).order_by("-is_primary", "-created_at")
    return render(request, "manage_addresses.html", {"addresses": addresses, "next": next_url})

def homepage(request):
	return render(request,"homepage.html")


def aboutus(request):
	return render(request,"aboutus.html")


def get_bot_response1(user_message):
    print("enter bot function================")
    import google.generativeai as genai
    print("hello")
    genai.configure(api_key="YOUR-API-KEY")
    # Set up the model
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }
    safety_settings = [    {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },]
    model=genai.GenerativeModel(model_name='gemini-1.5-flash', generation_config=generation_config,safety_settings=safety_settings)
    # user_prompt = "\nUser
    convo = model.start_chat()
    convo.send_message(user_message)
    answer=convo.last.text
    print("hello")
    return answer




def chat(request):
    if request.method == 'POST':
        # Parse the JSON content from the request body
        data = json.loads(request.body.decode('utf-8'))
       
        # Access the 'user_input' key from the JSON data
        user_message = data.get('message', '')
       
        # Now you can use user_message in your logic
        print("User Message:", user_message)
       
        #Get bot response based on user input
        bot_response = get_bot_response1(user_message)
        print("================res===========")

        # Save user message to the database
        ChatMessage.objects.create(user='User', message=user_message)
        # Save bot response to the database
        ChatMessage.objects.create(user='Bot', message=bot_response)
        #bot_response=""
        return JsonResponse({'response': bot_response})

   
    messages = ChatMessage.objects.all()
    return render(request, 'chat.html', {'messages': messages})

from django.utils import timezone

def cod_order(request):
    user_email = request.session.get("email")
    if not user_email:
        return redirect("/login")

    user = Register1.objects.get(email=user_email)
    cart_items = Cart.objects.filter(user=user)
    if not cart_items.exists():
        return redirect("/cart")

    selected_id = request.session.get("selected_address_id")
    shipping = ShippingAddress.objects.filter(user=user, id=selected_id).first()
    if not shipping:
        return redirect("/select-shipping")

    # Calculate total
    total_amount = sum(item.product.unit_price * item.quantity for item in cart_items)

    # Create a dummy payment for COD
    payment = Payment.objects.create(
        user=user,
        payment_id=f"COD-{user.id}-{Payment.objects.count() + 1}",
        amount=total_amount,
        status="Success"  # Still marked as success
    )

    # Save items
    for item in cart_items:
        OrderItem.objects.create(
            payment=payment,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.product.unit_price
        )

    # Clear cart
    cart_items.delete()

    return render(request, "thank_you.html")
