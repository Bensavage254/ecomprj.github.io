import base64
import datetime
import json
import re
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
import requests
from taggit.models import Tag
from django.db.models import Avg
from core.models import Product, Category,Vendor, CartOrder, CartOrderItems ,ProductImages,ProductReview, Wishlist_model, Address
from core.forms import ProductReviewForm, PaymentForm
from django.template.loader import render_to_string 
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from http.client import HTTPResponse
from django.http import JsonResponse, HttpResponse
from django_daraja.mpesa.core import MpesaClient

def index(request):
    #products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(product_status='published', featured=True)


    context = {
        "products": products,
    }
    return render(request, "core/index.html", context)

def product_list_view(request): 
    products = Product.objects.filter(product_status='published')

    context = {
        "products": products,
    }
    return render(request, "core/product-list.html", context)

def category_list_view(request): 
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "core/category-list.html", context)

def category_product_list_view(request,  cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "core/category-product-list.html", context)

def vendor_list_view(request): 
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, "core/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter(vendor = vendor, product_status='published')
    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    products = Product.objects.filter(category= product.category).exclude(pid=pid)

    #Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    #getting average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    #product review form
    review_form = ProductReviewForm()

    make_review =True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False

    p_image = product.p_images.all()

    context = {
        "p": product,
        'make_review': make_review,
        'review_form': review_form,
        'p_image': p_image,
        'average_rating': average_rating,
        'reviews': reviews,
        'products': products,
    }
    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):

    products = Product.objects.filter(product_status='published').order_by('-id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag,
    }
    return render(request, "core/tag.html", context)

def ajax_add_review(request , pid):
    product = Product.objects.get(pk = pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    context ={
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_reviews': average_reviews
        }
    )

def search_views(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    context = {
        "products": products,
        'query': query
    }
    return render(request, "core/search.html", context)

def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(product_status='published').order_by('-id').distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    
    data = render_to_string('core/async/product-list.html',{"products": products})
    return JsonResponse({'data': data})

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        "title": request.GET['title'],
        "price": request.GET['price'],
        "qty": request.GET['qty'],
        "image": request.GET['image'],
        "pid": request.GET['pid'],

    }

    if "cart_data_obj" in request.session:
        if str(request.GET["id"]) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)

            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], "totalcartitems" : len(request.session["cart_data_obj"])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item['price'])

        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems" : len(request.session["cart_data_obj"]), "cart_total_amount": cart_total_amount})
    else:
        messages.warning(request,'Your cart is empty')
        return redirect('core:index')

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session["cart_data_obj"]
            del request.session['cart_data_obj'][product_id]
            request.session["cart_data_obj"] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item['price'])

        context = render_to_string("core/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], "totalcartitems" : len(request.session["cart_data_obj"]), "cart_total_amount": cart_total_amount})
        return JsonResponse({"data": context, "totalcartitems" : len(request.session["cart_data_obj"])})
    
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session["cart_data_obj"]
            cart_data[str(request.GET["id"])]['qty'] = product_qty
            request.session["cart_data_obj"] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item['price'])

        context = render_to_string("core/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], "totalcartitems" : len(request.session["cart_data_obj"]), "cart_total_amount": cart_total_amount})
        return JsonResponse({"data": context, "totalcartitems" : len(request.session["cart_data_obj"])})
    
def checkout_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            cart_total_amount += int(item["qty"]) * float(item['price'])

        return render(request, "core/checkout.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems" : len(request.session["cart_data_obj"]), "cart_total_amount": cart_total_amount})
    

# def payment_completed_view(request):
#     return render(request, "core/payment-completed.html")

def payment_failed_view(request):
    return render(request, "core/payment-failed.html")


# Retrieve variables from the environment
CONSUMER_KEY = ("af1SPPvRRxboCc7v4Uc8seAnWei8WpVuw5XyX0FWa46TxSji")
CONSUMER_SECRET = ("AMeLG8mrE74N7BIGqyAYWoAmnOywTeEIeYTjGHPCcL53xsGvt2408qOVu7N7rGF3")
MPESA_PASSKEY = ("bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919")

MPESA_SHORTCODE = ("174379")
CALLBACK_URL = ("CALLBACK_URL")
MPESA_BASE_URL = ("https://MPESA_BASE_URL/oauth/v1/generate?grant_type=client_credentials?")

# Phone number formatting and validation
def format_phone_number(phone):
    phone = phone.replace("+", "")
    if re.match(r"^254\d{9}$", phone):
        return phone
    elif phone.startswith("0") and len(phone) == 10:
        return "254" + phone[1:]
    else:
        raise ValueError("Invalid phone number format")


# Generate M-Pesa access token
def generate_access_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers,
        ).json()

        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Access token missing in response.")

    except requests.RequestException as e:
        raise Exception(f"Failed to connect to M-Pesa: {str(e)}")
        

# Initiate STK Push and handle response
def initiate_stk_push(phone, amount):
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "account",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=request_body,
            headers=headers,
        ).json()

        return response

    except Exception as e:
        print(f"Failed to initiate STK Push: {str(e)}")
        return e

# Payment View
def payment_view(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                phone = format_phone_number(form.cleaned_data["phone_number"])
                amount = int(form.cleaned_data["amount"])
                response = initiate_stk_push(phone, amount)
                print(response)

                if response.get("ResponseCode") == "0":
                    checkout_request_id = response["CheckoutRequestID"]
                    return render(request, "core/pending.html", {"checkout_request_id": checkout_request_id})
                else:
                    error_message = response.get("errorMessage", "Failed to send STK push. Please try again.")
                    return render(request, "core/payment_form.html", {"form": form, "error_message": error_message})

            except ValueError as e:
                return render(request, "core/payment_form.html", {"form": form, "error_message": str(e)})
            except Exception as e:
                return render(request, "core/payment_form.html", {"form": form, "error_message": f"An unexpected error occurred: {str(e)}"})

    else:
        form = PaymentForm()

    return render(request, "core/payment_form.html", {"form": form})


# Query STK Push status
def query_stk_push(checkout_request_id):
    print("Quering...")
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
            json=request_body,
            headers=headers,
        )
        print(response.json())
        return response.json()

    except requests.RequestException as e:
        print(f"Error querying STK status: {str(e)}")
        return {"error": str(e)}

# View to query the STK status and return it to the frontend
def stk_status_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            checkout_request_id = data.get('checkout_request_id')
            print("CheckoutRequestID:", checkout_request_id)

            # Query the STK push status using your backend function
            status = query_stk_push(checkout_request_id)

            # Return the status as a JSON response
            return JsonResponse({"status": status})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt  # To allow POST requests from external sources like M-Pesa
def payment_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed")

    try:
        callback_data = json.loads(request.body)  # Parse the request body
        result_code = callback_data["Body"]["stkCallback"]["ResultCode"]

        if result_code == 0:
            # Successful transaction
            checkout_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
            metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

            amount = next(item["Value"] for item in metadata if item["Name"] == "Amount")
            mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
            phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

            # Save transaction to the database
            Transaction.objects.create(
                amount=amount, 
                checkout_id=checkout_id, 
                mpesa_code=mpesa_code, 
                phone_number=phone, 
                status="Success"
            )
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment successful"})

        # Payment failed
        return JsonResponse({"ResultCode": result_code, "ResultDesc": "Payment failed"})

    except (json.JSONDecodeError, KeyError) as e:
        return HttpResponseBadRequest(f"Invalid request data: {str(e)}")

@login_required
def wishlist_view(request):
    wishlist = Wishlist_model.objects.all()
    context = {
        "w": wishlist,
    }
    return render(request, 'core/wishlist.html', context)

def add_to_wishlist(request):
    product_id = request.GET["id"]
    product = Product.objects.get(id=product_id)

    context ={}

    wishlist_count = Wishlist_model.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context ={
            "bool": True,
        }

    else:
        new_wishlist = Wishlist_model.objects.create(product=product, user=request.user)

        context = {
            "bool": True,
        }

    return JsonResponse(context)




def mpesaapi(request):
    client = MpesaClient()
    phone_number = '254745919342'
    amount = 1
    account_reference = 'ShopOn'
    transaction_desc = 'Payment for eccomerse shopping'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = client.stk_push (phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


    
    



        






