from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render,redirect
from adminapp.models import Category, Tourism
from myapp.models import Bookings, UserInfo, Payment, TouristInfo
# Create your views here.

def homepage(request):
    cats=Category.objects.all() # all objects in Category
    places=Tourism.objects.all()   #all objects in Tourism ( sub categoris)
    return render(request,"master.html",{"cats":cats,"places":places})  #pass that objects in dict format to master.html


def ViewDetails(request,id):
    cats=Category.objects.all() # all objects in Category
    places = Tourism.objects.all()
    place=Tourism.objects.get(id=id) # this for brief details of that place
    return render(request,"ViewDetails.html",{"place":place,"cats":cats,"places":places})

def Login(request):
    places = Tourism.objects.all()
    cats = Category.objects.all()
    if(request.method == "GET"):       # if persons directly goes by url then show him login page
        return render(request,"Login.html",{"places":places,"cats":cats})
    else:
        uname = request.POST["uname"]          # if he goes by clicking on button
        pwd = request.POST["pwd"]                  # ask him login uname and pass
        try:
            user = UserInfo.objects.get(username = uname,password=pwd)         # check in userinfo table for respective uname and pass user
        except:
            return render(request,"Login.html",{"msg":"An account could not be found for the provided loginId and Pass"})  #if user not found then plz singup
        else:
            request.session["uname"]=uname       #if correct uname and pass then save uname in session until it is not logout/time given by session
            return redirect(homepage)

def SignUp(request):
    cats = Category.objects.all()
    places = Tourism.objects.all()
    if(request.method == "GET"):
        return render(request,"SignUp.html",{"cats":cats,"places":places})
    else:
        uname = request.POST["uname"]    #if new user signup
        pwd = request.POST["pwd"]
        email = request.POST["email"]

        user = UserInfo(uname,pwd,email)    # create object of that user in userinfo table
        user.save()       #save that user info in db
        return redirect(homepage)

def showcategory(request,id):
    cats=Category.objects.all() # all objects in Category
    mat=Category.objects.get(id=id)  # particular category id 
    places=Tourism.objects.filter(id=mat)  #finds all the subcategories within that category
    return render(request,"master.html",{"cats":cats,"places":places})   #pass that subcategories and category to the master page

def Logout(request):
    request.session.clear()         # during login clear the session value
    return redirect(homepage)

def BookTheTour(request):
    if(request.method == "POST"):         # by clicking on button book tour
        if("uname" in request.session):       # if login then let in  book the tour
            user = UserInfo.objects.get(username = request.session["uname"])     # find perticular uname bookings added / all the objects of that
            # fetch the uname and place_id from respective details
            tourism = Tourism.objects.get(id = request.POST["place_id"])
            persons = request.POST["persons"]   

            cats=Category.objects.all() # all objects in Category
            places = Tourism.objects.all()
            place=Tourism.objects.get(id=request.POST["place_id"]) # this for brief details of that place
            #Before adding to cart we need to check for duplicate entry
            try:
                book_tour = Bookings.objects.get(user = user,tourism=tourism)
            except:
                #Add item to cart
                book_tour = Bookings()   #create object and add tour with persons
                book_tour.user = user
                book_tour.tourism = tourism
                book_tour.persons = persons
                book_tour.save()
                return redirect(homepage)     #after adding tour in bookings redirect to the homepage
            else:
                return render(request,"ViewDetails.html",{"msg":"tour already added in bookings","cats":cats,"places":places,"place":place})  #if that tour already added  
                               
        else:
            return redirect(Login)     #if not login then login first
    else:
        return redirect(Login)    # if you go on book tour page by url


def ShowAllBookings(request):
    places = Tourism.objects.all()
    uname = request.session["uname"]
    user = UserInfo.objects.get(username = uname)
    if(request.method == "GET"):       
        items = Bookings.objects.filter(user = user)    # using user show only that user bookings
        cats = Category.objects.all()


        total = 0
        for item  in items:
            total += float(item.tourism.price_Rs) * float(item.persons)       # total value of tour calculated
        request.session["total"] = total    #put that total in session so use anywhere
        return render(request,"ShowAllBookings.html",{"items":items,"cats":cats,"places":places,"user":user})  #in items pass user info
    else:
        action = request.POST["action"]   
        place_id = request.POST["place_id"]   #from place id find place name by hidden field
        tourism = Tourism.objects.get(id=place_id)
        date=request.POST['date']
          #from name get the objects of that 

        item = Bookings.objects.get(user=user,tourism=tourism)        #pass that object (place_id) & user on which it is login
        if(action=="update"):
            #fetch value from persons from textbox with name qty
            qty = request.POST["qty"]   #if user click on update button  then fetch qty value from that qty input field
            item.persons = qty     # add that qty in persons of bookings table
            item.save()  #save that data in db
            return redirect(ShowAllBookings)
        else:            
            item.delete()            #if clicked on cancel the tour then delete that objects from db
        return redirect(ShowAllBookings)

    
def MakePayment(request):
    places = Tourism.objects.all()
    uname = request.session["uname"]           
    user = UserInfo.objects.get(username = uname)
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        card_no = request.POST["card_no"]    #fetch the card details from input fields
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        
        try:
            buyer = Payment.objects.get(card_no=card_no,cvv=cvv,expiry=expiry)     #chk if fetched data and data in admin are same
        except:
            return render(request,"MakePayment.html",{"msg":"Invalid card details"})   #if not sane show invalid msg
        else:
            owner = Payment.objects.get(card_no="1111111111111111",cvv="111",expiry="12/2030")     #credit amount to the owners account shown here
            total = request.session["total"]   # fetch total value from session
            if(buyer.balance<=0):     # if users account has insufficient fund then show that msg
                return render(request,"MakePayment.html",{"msg":"Insufficient Fund in Account"})
                #if buyer account balance is less than equal to 0
            else:
                if(total>buyer.balance):
                    return render(request,"MakePayment.html",{"msg":"Account does't have sufficient fund to pay total amount"})
                    # if total amount is greater than buyer account balance
                else:
                    buyer.balance -= total    #deduct that amount from users account
                    owner.balance += total   # and add that amount in owners account
                    buyer.save()   # save that account details in db 
                    owner.save()

            #below code for order master user info saved 
            uname = request.session["uname"]
            items = Bookings.objects.filter(user = request.session["uname"])  #from uname fetch all the objects of that user
            tour_details=[]   #declare empty list which will add user info
            t_persons=[]
            t_price=[]
            
            
            for item  in items:
                tour_details.append(item.tourism.place_name)   #from that objects fetch place_name and add to the list
                t_persons.append(item.persons)      #similarly for persons and tour sub total
                t_price.append(item.persons * item.tourism.price_Rs)


            tour=TouristInfo()   #create object touristinfo
            tour.user_name=request.session["uname"]    #from the session fetch user name
            tour.total_persons=",".join(map(str,t_persons))   #join the persons value by "," in list
            tour.tour_price = ",".join(map(str,t_price)) #map returns map object which can be iterated 
            tour.place_name=",".join(tour_details)
            tour.total_price=request.session['total']
            tour.booked_date=datetime.now()   #get the current time 
            tour.save()   #save  in db
            for item  in items:
                item.delete()                 #Delete the cart items when payment successful
            return render(request,"VisitAgain.html",{})