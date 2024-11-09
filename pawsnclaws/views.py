from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseBadRequest
from .models import register,ads,pay,Purchase,Address,DeliveryRequest,complaints
import razorpay
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import re,json
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings


def open(request):
    return render(request,'home.html')
def afterorder(request):
    return render(request,'index.html')
def ap(request):
    return render(request,'index.html')
def first(request):
    return render(request, 'login.html')
def orderstatus(request):
    if 'uid' in request.session:
        data = request.session['uid']
        pdata = Purchase.objects.filter(bname=data)
    return render(request,'orderstatus.html',{'b':pdata})

def reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        ph = request.POST['uph']
        uname = request.POST['uname']
        umail = request.POST['umail']
        upassword = request.POST['upass']
        upurpose = request.POST['upur']

        # Validate the received data
        if not (name and ph and uname and umail and upassword and upurpose):
            return render(request, 'login.html', {'error_message': 'All fields are required.'})

        if register.objects.filter(username=uname).exists():
            return render(request, 'login.html', {'error_message': 'Username is already taken. Please choose another one.'})
        
        if register.objects.filter(phone=ph).exists():
            return render(request, 'login.html', {'error_message': 'The entered number is already taken. Please choose another one.'})
        
        phone_pattern = re.compile(r'^\d{10}$')
        if not phone_pattern.match(ph):
            return render(request, 'login.html', {'error_message': 'Invalid phone number. Please enter a valid 10-digit phone number.'})
        
        try:
            EmailValidator(umail)
        except ValidationError:
            return render(request, 'login.html', {'error_message': 'Invalid email address. Please enter a valid email.'})
        
        
        if len(upassword) < 8 or not any(c.isnumeric() for c in upassword) or not any(c.isalpha() for c in upassword) or not any(not c.isalnum() for c in upassword):
            return render(request, 'login.html', {
                'error_message': 'Password must have a minimum of 8 characters, including at least one number, one letter, and one symbol.'
            })

        register.objects.create(
            Name=name,
            phone=ph,
            username=uname,
            mail=umail,
            password=upassword,
            purpose=upurpose
        )
        
        return render(request, 'index.html', {'success_message': 'Registration successful.'})
    
    
    
    return render(request, 'home.html')
def forget(request):
    return render(request, 'forget.html', {'step': '1'})

def change_password(request):
    if request.method == 'POST':
        step = request.POST.get('step', '1')  # Default to '1' if no step is provided

        if step == '1':
            phone_number = request.POST['num']

            # Validate phone number (example pattern for 10 digits)
            phone_pattern = re.compile(r'^\d{10}$')
            if not phone_pattern.match(phone_number):
                return render(request, 'forget.html', {
                    'error_message': 'Invalid phone number. Please enter a valid 10-digit phone number.',
                    'step': '1'
                })

            # Check if the phone number is associated with any account
            if not register.objects.filter(phone=phone_number).exists():
                return render(request, 'forget.html', {
                    'error_message': 'Phone number not found. Please check and try again.',
                    'step': '1'
                })

            # Proceed to the next step
            return render(request, 'forget.html', {
                'success_message': 'Phone number verified. Please enter your new password.',
                'step': '2',
                'num': phone_number
            })

        elif step == '2':
            phone_number = request.POST['num']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if new_password != confirm_password:
                return render(request, 'forget.html', {
                    'error_message': 'Passwords do not match. Please try again.',
                    'step': '2',
                    'num': phone_number
                })
                
            if len(new_password) < 8 or not any(c.isnumeric() for c in new_password) or not any(c.isalpha() for c in new_password) or not any(not c.isalnum() for c in new_password):
                return render(request, 'forget.html', {
                'error_message': 'Password must have a minimum of 8 characters, including at least one number, one letter, and one symbol.'
            })
            # Update the user's password
            user = register.objects.get(phone=phone_number)
            user.password = new_password
            user.save()

            return render(request, 'login.html', {
                'success_message': 'Password has been reset successfully.'
            })

    return render(request, 'forget.html', {'step': '1'})
def login(request):
    if request.method =='POST':
        lu = request.POST['luser']
        lp = request.POST['lpass']
        adminuser = "admin"
        adminpass = "admin123"
        data = register.objects.filter(username=lu,password=lp) 
        if data.filter(purpose='buy'):
           #return render(request,'index.html')
             request.session['uid'] = lu
             return redirect(profile)
        
        
    
        elif data.filter(purpose='sell'):
            #return render(request,'shop.html' )
            request.session['sid'] = lu
            return redirect(profile)
  
        elif lu ==adminuser and lp == adminpass:
            #return render(request,'admin.html')
             request.session['aid'] = lu
             return redirect(profile)
        
        else:
            return HttpResponse('<script>alert("Incorrect username or password"); window.history.back();</script>')
def profile(request):
    if 'uid' in request.session:
        data = request.session['uid']
        data1 = register.objects.filter(username=data)
        return render(request, 'index.html', )
    elif 'sid' in request.session:
        data = request.session['sid']
        data2 = register.objects.filter(username=data)
        return render(request, 'shopinter.html',)
    elif 'aid' in request.session:
        data = request.session['aid']
        data3 = register.objects.filter(username=data)
        tsell = register.objects.filter(purpose='sell').count()
        tbuy = register.objects.filter(purpose='buy').count()
        total_cash = 0
        for payment in pay.objects.all():
            total_cash += payment.cash
            tcash = total_cash/100
            
        print(total_cash)
        dreq = DeliveryRequest.objects.all()
        return render(request, 'admin.html', {'ts': tsell, 'tb': tbuy, 'tc':tcash,'dr':dreq})
      
    else:
        return HttpResponse("Invalid account")

def opro(request):
    if 'uid' in request.session:
        data = request.session['uid']
        data1 = register.objects.filter(username=data)
        pdata = Purchase.objects.filter(bname=data)
        return render(request,'profile.html', {'r':data1,'b':pdata}) 
    elif 'sid' in request.session:
        data = request.session['sid']
        data2 = register.objects.filter(username=data)
        return render(request,'sprofile.html', {'r':data2}) 
    elif 'aid' in request.session:
        data = request.session['aid']
        data3 = register.objects.filter(username=data)
        return render(request,'profile.html', {'r':data3}) 
    return render(request,'index.html')
    
def logout(request):
    if 'uid' in request.session:
        request.session.flush()
        return render(request,'login.html')
    elif 'sid' in request.session:
        request.session.flush()
        return render(request,'login.html')
    elif 'aid' in request.session:
        request.session.flush()
        return render(request,'login.html')
        
        
def adreg(request):
    # Ensure the request method is POST
    if request.method == 'POST':
        if 'sid' in request.session:
            uname = request.session['sid']
            
            # Get form data from POST request
            owname = request.POST.get('name')
            ph = request.POST.get('num')
            loca = request.POST.get('location')
            pri = request.POST.get('price')
            type = request.POST.get('type')
            breed = request.POST.get('breed')
            age = request.POST.get('age')
            color = request.POST.get('color')
            
            # Get uploaded files from POST request
            i1 = request.FILES.get('img1')
            i2 = request.FILES.get('img2')
            i3 = request.FILES.get('img3')

            # Create and save new ad entry to the database
            data = ads.objects.create(
                owusername=uname,
                ownername=owname,
                phone=ph,
                location=loca,
                price=pri,
                pet_type=type,
                pet_breed=breed,
                pet_age=age,
                pet_color=color,
                pet_image1=i1,
                pet_image2=i2,
                pet_image3=i3
            )
            data.save()
            return render(request, 'shopinter.html')
    else:
        # Handle the case where the request method is not POST
        return render(request, 'login.html')  # Replace with your form template

    # Optionally handle other request methods or redirect if necessary
    return render(request, 'login.html.html')

def adplace(request):
    username = request.session.get('sid')
    db = pay.objects.filter(pname=username)
    for i in db:
        if i.cash >0:
            return render(request,'adplace.html')
        
    return render(request, 'shop.html')
        

def payment(request):
    if request.method == 'POST' or 'GET':
        payment_id = request.POST.get('payment_id')
        username = request.session.get('sid')  # Retrieve username from session
        print("Username:", username)
        
        if username:
            amount = 50000  # Hardcoded amount for demonstration, you can replace this with the actual amount
            
            # Call Razorpay to create the order
            client = razorpay.Client(auth=("rzp_test_25QMSu2wWe3zbI", "oczP6DqWLp1biAN7GHWQjE4d"))
            try:
                payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                order_id = payment['id']
                
                # Save payment details to your database
                payment_record = pay.objects.create(cash=amount, pname=username)
                payment_record.save()
                
                # Redirect to success page or do something else
                return render(request, "adplace.html")
                
            except Exception as e:
                return HttpResponse(f"Error occurred: {str(e)}")
                
        else:
            return HttpResponse('<script>alert("You need to login first"); window.location.href = "";</script>')

            
   
    return HttpResponse('<script>alert("You need to login first"); window.location.href = "/";</script>')



def shopreg(request):
    return render (request,'adplace.html')
def ser(request):
    # Fetch all locations from Ads model and convert to a set to remove duplicates
    locations_set = set(ads.objects.values_list('location', flat=True))

    # Convert the set back to a list to maintain order if needed
    locations = list(locations_set)

    context = {
        'locations': locations
    }
    return render(request, 'search.html', context)

def show(request):
    if request.method=='POST':
        type = request.POST['type']
        print(type)
        breed = request.POST['breed']
        print(breed)
        loca = request.POST['location']
        print(loca)
        data = ads.objects.filter(pet_type=type, pet_breed=breed, location=loca)
        print(data)
        
        return render(request,'list.html',{'r': data})
        


# def tuser(request):
#     tsell = register.objects.filter(purpose='sell').count()
#     tbuy = register.objects.filter(purpose='buy').count()
#     return render(request, 'admin.html', {'ts': tsell, 'tb': tbuy})
@csrf_exempt
def make_payment(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        payment_id = request.POST.get('payment_id')

        print(f'Received POST request with item_id: {item_id} and payment_id: {payment_id}')

        try:
            # item = get_object_or_404(ads, id=item_id)
            item = DeliveryRequest.objects.get(id=item_id)
            print(f'Found item: {item}')
            
            

            if 'uid' in request.session:
                data = request.session['uid']
                print(f'Session UID: {data}')
                
                uname = register.objects.filter(username=data).values_list('username', flat=True).first()
                print(f'Found user: {uname}')

                # if item:
                #     # Extract item information
                #     oname = item.ownername
                #     itemname = item.pet_type
                #     cash = item.price
                #     breed = item.pet_breed
                #     print(f'Owner: {oname}, Item: {itemname}, Price: {cash}, Breed: {breed}')
                if item:
    # Extract item information
                    owner_name = item.item.ownername
                    address = item.address.address
                    item_name = item.item.pet_type
                    item_price = item.item.price
    # Add more fields as needed
    
                    print(f'Owner: {owner_name}, Address: {address}, Item Name: {item_name}, Price: {item_price}')
                    # Create Purchase record
                    purchase = Purchase.objects.create(
                        bname=uname, 
                        owname=owner_name, 
                        itemname=item_name, 
                        cash=item_price, 
                        # itembreed=breed, 
                        payment_id=payment_id
                    )
                    purchase.save()
                    print('Purchase record created')

                    # Delete the item after purchase
                    item.item.delete()  
                    item.delete()
                    print('Item deleted')

                    return JsonResponse({'success': True})
                else:
                    print('User not found in the session')
                    return JsonResponse({'success': False, 'message': 'User not found in the session'})
            else:
                print('User not authenticated')
                return JsonResponse({'success': False, 'message': 'User not authenticated'})
        except ads.DoesNotExist:
            print('Item not found in database')
            return JsonResponse({'success': False, 'message': 'Item not found'})
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred'})
    else:
        print('Invalid request method')
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
def tsell(request):
    sellers_with_reviews = []  # Initialize a list to hold sellers with their bad reviews count

    if request.method == 'GET':
        sellers = register.objects.filter(purpose='sell')
        for seller in sellers:
            bad_reviews_count = complaints.objects.filter(complaintname=seller.Name, rating='bad').count()
            sellers_with_reviews.append({
                'seller': seller,
                'bad_reviews_count': bad_reviews_count
            })
            
    return render(request, 'ts.html', {'ts': sellers_with_reviews})
def tbuy(request):
    if request.method=='GET':
        tbu = register.objects.filter(purpose='buy')
    return render(request,'tb.html',{'tb':tbu})
def ad(request):
    if request.method == 'GET':
        tads = ads.objects.all()
    return render(request, 'ads.html', {'tads': tads})
@csrf_exempt
def delete_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            # Check if the item exists in the Register model
            item = register.objects.get(Name=name)
            # If it exists, delete it
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully'})
        except register.DoesNotExist:
            return JsonResponse({'message': 'Item does not exist'})
    else:
        return JsonResponse({'message': 'Invalid request method'})
def adr(request):
    if 'uid' in request.session:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            if item_id:
                print('1st item:', item_id)
                request.session['selected_item_id'] = item_id
                print('2nd item:', item_id)
                
                username = request.session['uid']
                user = get_object_or_404(register, username=username)
                print('User data:', user)
                
                addresses = Address.objects.filter(user=user)
                return render(request, 'uadress.html', {'addresses': addresses})
            else:
                return HttpResponseBadRequest("Item ID not provided")
        else:
            return HttpResponseBadRequest("Invalid request method")
    else:
        return render(request, 'login.html')
def adadress(request):
    return render(request,'adadress.html')
def add_address(request):
    if 'uid' in request.session:
        username = request.session['uid']
        user = get_object_or_404(register, username=username)
        
        if request.method == 'POST':
            name = request.POST['firstname']
            email = request.POST['email']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            if len(pincode)!=6:
                return HttpResponse('<script>alert("ENter a valid pincode"); window.history.back();</script>')
           
           
            Address.objects.create(
                user=user,
                name=name,
                email=email,
                address=address,
                city=city,
                state=state,
                pincode=pincode
            )
            addresses=Address.objects.filter(user=user)
            return render(request,'uadress.html',{'addresses': addresses})
    else:
        return render(request, 'login.html')
    return HttpResponse('<script>alert("ENter a valid pincode"); window.history.back();</script>')
def send_request(request, address_id):
    if 'uid' in request.session:
        username = request.session['uid']
        item_id = request.session.get('selected_item_id')
        print('this is uid', username)
        print('item id', item_id)

        if not item_id:
            return render(request, 'index.html')  # or some error page

        user = get_object_or_404(register, username=username)
        print('user', user)
        
        # Retrieve the first address associated with the user
        try:
           address = get_object_or_404(Address, id=address_id, user=user)
           print('address', address)
        except Address.DoesNotExist:
            return render(request, 'login.html', {'message': 'No address found for user.'})
        
        item = get_object_or_404(ads, id=item_id)
        print('item', item)
        owner = get_object_or_404(register, username=item.owusername)
        owner_email = owner.mail
        print('owner email', owner_email)

        delivery_request =DeliveryRequest.objects.create(
            user=user,
            address=address,
            item=item,
            status="pending"
        )
        send_mail(
            subject='New Delivery Request',
            message=f'A new delivery request has been created:\n\nUser: {user.username}\nAddress: {address}\nItem: {item.pet_type}\nStatus: {delivery_request.status}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[owner_email],  # Replace with the actual shop email address
            fail_silently=False,
        )

        return render(request, 'succ.html', {'address': address, 'item': item})
    else:
        return render(request, 'login.html')  # Redirect to login page if not logged in

def ure(request):
    user_id = request.session['uid']
    user = get_object_or_404(register, username=user_id)
    purchase_requests = DeliveryRequest.objects.filter(user=user)
    return render(request, 'userreq.html', {'purchase_requests': purchase_requests})
   
def sreq(request):
    if 'sid' in request.session:
        shop_id = request.session['sid']
        print('shopid is',shop_id)
        user = register.objects.get(username=shop_id)
        
        print(user)
        delivery_requests = DeliveryRequest.objects.filter(item__ownername=user)
        print('delreq',delivery_requests)
        return render(request, 'shoprequest.html', {'delivery_requests': delivery_requests})
    else:
        return render(request, 'login.html') 
        
@csrf_exempt
def accept_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        try:
            delivery_request = DeliveryRequest.objects.get(id=request_id)
            delivery_request.status = 'confirmed'
            delivery_request.save()
            return JsonResponse({'status': 'success'})
        except DeliveryRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Request not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def reject_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        print('reqid',request_id)
        try:
            delivery_request = DeliveryRequest.objects.get(id=request_id)
            delivery_request.delete()
            return JsonResponse({'status': 'success'})
        except DeliveryRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Request not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def complaint(request):
     users = register.objects.filter(purpose='sell').values('id', 'Name')
     return render(request, 'complaint.html', {'users': users})
 
 
def submit_complaint(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        user_id = request.POST.get('user')
        rating = int(request.POST.get('rating'))  # Convert rating to integer
        complaint_desc = request.POST.get('complaint')
        
        compname = get_object_or_404(register,id = user_id)
        
        # Check if user is logged in (assuming 'uid' is the session key for user ID)
        if 'uid' in request.session:
            user = request.session['uid']
        else:
            # Return error if user is not logged in
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
        # Determine the rating category
        if rating >= 7:
            rating_category = 'good'
        elif rating >= 5:
            rating_category = 'average'
        else:
            rating_category = 'bad'

        # Save the complaint to the database
        complaint_obj = complaints.objects.create(
            user=user,
            rating=rating_category,
            complaintname=compname,
            complaintdesc=complaint_desc
        )
    

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Complaint submitted successfully!'})
    else:
        # If the request method is not POST, return an error
        return JsonResponse({'error': 'Invalid request method'}, status=400)
 
def feedback(request):
    return render(request,'feedback.html')

@csrf_exempt
def send_warning(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_name = data.get('item_name')

            if not item_name:
                raise ValueError('Item name not provided')

            # Fetch the logged-in user's email from the Register model
            user = register.objects.get(id=request.user.id)
            user_email = user.mail

            # Send email
            send_mail(
                subject='Warning',
                message=f'Warning: Your item {item_name} has received more than 5 bad reviews. '
                        'If this continues, we will terminate your account and delete all posts associated with it. '
                        '\n\nYours respectfully,\nPAWSNCLAWS.',
                from_email=settings.EMAIL_HOST_USER,  # From email
                recipient_list=[user_email],  # To email
                fail_silently=False,
            )

            return JsonResponse({'message': 'Warning email sent successfully'}, status=200)
        except register.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=404)
        except ValueError as ve:
            return JsonResponse({'message': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
def showadd(request):
    if 'sid' in request.session:
        sid = request.session['sid']
        data = ads.objects.filter(owusername = sid)
        print(data)
    return render(request,'showadd.html',{'data':data})


def remove_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        print('this is uid',user_id)
        # Perform the logic to remove the user with the given ID from your database
        # For example:
        try:
            user = register.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User removed successfully'}, status=200)
        except register.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
def shfulladd(request):
    data = ads.objects.all()
    return render(request,'fullad.html',{'data':data})

@csrf_exempt
def delete_ad(request):
    if request.method == 'POST':
        ad_id = request.POST.get('id')
        print('id is',ad_id)
        if ad_id:
            try:
                ad = ads.objects.get(id=ad_id)
                ad.delete()
                return JsonResponse({'message': 'Ad deleted successfully'}, status=200)
            except ads.DoesNotExist:
                return JsonResponse({'message': 'Ad not found'}, status=404)
        return JsonResponse({'message': 'ID not provided'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)
        
                
                