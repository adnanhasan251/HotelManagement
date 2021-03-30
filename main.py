from __future__ import print_function, absolute_import, with_statement
import pandas as pd
import cfonts
import db_connect as dbc
from tabulate import tabulate

dbc.connect('hotel_t1')

cfonts.say("WELCOME TO HOTEL CALIFORNIA", font='chrome', colors=['candy', 'candy', 'candy'], align='center', space=True)

def guest():
    dbc.create('guest_t2', "'fname', 'lname', 'phone', 'email', 'address', 'adults', 'child', 'stay', 'room_no', 'wifi'")
    #check_room()
    # personal info
    fname = input("First Name:  ")
    lname = input("Last Name:  ")
    # contact
    while True:
        phone = input("Phone Number:  ")
        if (phone.isnumeric()) and (8<len(phone)<13) and (" " not in phone) and (phone.startswith("9") or phone.startswith("7")  or phone.startswith("8") or phone.startswith("91")):
            break
        else:
            print("Invalid phone number")

 

    while True:
        email = input("Email:  ")
        if "@" in email:
            a=email.partition("@")
            if len(a[0])!=0 and len(a[2])!=0 and "@" not in a[0] and "@" not in a[2]:
                break
            else:
                print("Invalid email")
        else:
            print("Invalid email")


            
    while True:
        address = input("Guest's Address:  ")
        if address.isalnum() and len(address)!=0:
            break
        else:
            print("Invalid")
    # reservation info
    while True:
        adults = input("Number of Adults:  ")
        if int(adults)>=0 and adults.isnumeric():
            break
        else:
            print("Invalid number")
    while True:
        child = input("Number of Children:  ")
        if int(child)>=0 and child.isnumeric():
            break
        else:
            print("Invalid number")
    while True:
        stay = input("Number of Days of stay:  ")
        if int(stay)>=0 and stay.isnumeric():
            break
        else:
            print("Invalid number")
    wifi=input("Wifi access required (y/n):  ").upper()
    # room
    room_no = input("Enter the room number to reserve:  ")
    #insert guest details in database
    data="'"+fname+"', '"+lname+"', "+phone+", '"+email+"', '"+address+"', "+adults+", "+child+", "+stay+", "+room_no+", '"+wifi+"'"
    dbc.insert("guest_t2", data)
    #update room status
    upd_cond = "room_no="+room_no
    dbc.update("rooms", "status='R'", upd_cond)

    chosen = [
                ["First name", fname],
                ["Last name", lname],
                ["Phone no", phone],
                ["Email ID", email],
                ["Address", address],
                ["No. of Adults", adults],
                ["No. of children", child],
                ["No. of days", stay],
                ["Room Number", room_no],

             ]

    print("\n\n***********  ROOM ALLOTMENT ************\n\n")
    print(tabulate(chosen, tablefmt="fancy_grid"))
    con_trans = input("Do you want to confirm reservation ? [y/n]")
    if con_trans in ["y", "Y", "Yes", "YES"]:
        print("\n\nReservation Successful\n\n")

    y_n = input("\nDo you want to book another room ? [y/n]\n")
    if y_n in ["n", "N", "No"]:
        print("Thank you")
        global flag
        flag = False

def check_room():
    beds = input("Number of beds:  ")
    ac = input("AC required (y/n):  ").upper()
    tv = input("TV required (y/n):  ").upper()
    _filter = "beds="+beds+" AND ac="+"'"+ac+"'"+" AND tv="+"'"+tv+"'"+" AND status='NR'"
    available = dbc.get("rooms", "room_no", _filter)
    print("ROOMS AVAILABLE:")
    for Number in available:
        print(Number[0])
    print("Please select an option:")
    print("1. Reserve a room")
    print("2. Check another room")
    opt=int(input("(1/2):  "))
    if opt==1:
        guest()
    elif opt==2:
        check_room()

def check_out():
    roomno=input("Enter the room number to check out:  ")
    stay=int(input("Days stayed?:  "))
    dat="fname, lname, phone, room_no, wifi"
    _filter="room_no="+roomno
    roominf=dbc.get("guest_t2",dat,_filter)
    roominf_=pd.DataFrame(roominf, columns=['First Name', 'Last Name', 'Phone', 'Room No','Wifi'])
    print(roominf_)
    fname=roominf[0][0]
    lname=roominf[0][1]
    phone=roominf[0][2]
    wifi=roominf[0][4]

    dat2="beds, ac, tv"
    facility=dbc.get("rooms", dat2, _filter)
    beds=facility[0][0]
    ac=facility[0][1]
    tv=facility[0][2]


    item1="'"+ str(beds)+" bed" +"'"
    _filter3="item="+item1
    r_1=dbc.get("rate", "rpd", _filter3)[0][0]

    if ac=="Y":
        item2="'ac'"
        _filter4="item="+item2
        r_2=dbc.get("rate", "rpd", _filter4)[0][0]
    else:
        r_2=0
    
    if tv=="Y":
        item3="'tv'"
        _filter5="item="+item3
        r_3=dbc.get("rate", "rpd", _filter5)[0][0]
    else:
        r_3=0
    
    if wifi=="Y":
        item4="'ac'"
        _filter6="item="+item4
        r_4=dbc.get("rate", "rpd", _filter6)[0][0]
    else:
        r_4=0

    total=(r_1+r_2+r_3+r_4)*stay

    inv = [
                ["First name", fname],
                ["Last name", lname],
                ["Phone no", phone],
                ["No. of days", stay],
                ["Room per day", "Rs."+str(r_1)],
                ["TV per day", "Rs."+str(r_3)],
                ["AC per day", "Rs."+str(r_2)],
                ["Wifi per day", "Rs."+str(r_4)],
                ["Total ", "Rs."+str(total)],
                ["Room Number", roomno],

             ]

    co=input("Do you want to check out? (y/n)")
    if co.lower()=="y":
        #BILL
        print("\n\n***********  INVOICE ************\n\n")
        print(tabulate(inv, tablefmt="fancy_grid"))
        con_trans = input("Do you want to confirm transaction ? [y/n]")
        if con_trans in ["y", "Y", "Yes", "YES"]:
            print("\n\nTransaction Successful\n\n")

        y_n = input("\nDo you want to book another room ? [y/n]\n")
        if y_n in ["n", "N", "No"]:
            print("Thank you")
            global flag
            flag = False
        cond="room_no="+roomno
        dbc.delt("guest_t2", cond)
        upd_cond = "room_no="+roomno
        dbc.update("rooms", "status='NR'", upd_cond)
    elif co.lower()=="n":
        interf()

def room_status():
    global log
    rooms=dbc.seetable("rooms")
    guests=dbc.seetable("guest_t2")
    room_ = pd.DataFrame(rooms, columns=['Room no', 'Status','No of Beds','AC', 'TV'])
    guest_= pd.DataFrame(guests, columns=['First name', 'Last name', 'Phone No', 'Email', 'Address', 'No of Adults', 'No of Child', 'Days of Stay', 'Room No', 'Wifi Access'])
    print("Please select an option:")
    print("1. See all the room status")
    print("2. See guests details (admin only)")
    print("3. Back to Main Menu")
    opt=int(input("Enter (1/2/3):  "))
    if opt==1:
        print("ROOMS:")
        print(room_)
    elif opt==2:
        if adm==True:
            print("GUESTS:")
            print(guest_)
        else:
            print("You need admin priviledge to view the data")
            opt=input("Do you want to login as admin? (y/n)").lower()
            if opt=='y':
                log = False
                login()
    elif opt==3:
        print("Main Menu:")
    else:
        print("Please select from one of the given options!")
        room_status()


def rate():
    global log
    rate=dbc.seetable("rate")
    rate_=pd.DataFrame(rate, columns=['Item', 'Rate per day'])
    print(rate_)
    opt=input("Do you want to change rates (admin only)? (y/n)").lower()
    if opt=='y':
        if adm==True:
            print('''Which rate do you want to change?
            1. Charge of 'n' bed per day
            2. Charge of AC/TV/Wifi per day''')
            opt2=int(input("Enter (1/2):  "))
            if opt2==1:
                nbed=int(input("Enter the number of beds (1/2/3) of which you wish to change rates:  "))
                item="item='"+str(nbed)+" bed'"
                crate=dbc.get("rate","rpd", item)[0][0]
                print("Current rate is Rs."+str(crate))
                nrate=int(input("Enter the new rate (Rs.):  "))
                uptr="rpd="+str(nrate)
                dbc.update('rate', uptr, item)
                print("The new is set to Rs."+str(nrate))
            if opt2==2:
                print('''Please select one of the options:
                1. TV, 2. AC, 3. Wifi''')
                opt3=int(input("Enter (1/2/3:  "))
                items=['tv', 'ac', 'wifi']
                item="item='"+items[(opt3)-1]+"'"
                crate=dbc.get("rate","rpd", item)[0][0]
                print("Current rate is Rs."+str(crate))
                nrate=int(input("Enter the new rate (Rs.):  "))
                uptr="rpd="+str(nrate)
                dbc.update('rate', uptr, item)
                print("The new is set to Rs."+str(nrate))
        else:
                print("You need admin priviledge to change the rates")
                opt=input("Do you want to login as admin? (y/n)").lower()
                if opt=='y':
                    log = False
                    login()

def interf():
    global log
    global adm
    print("Please choose a option:")
    print("1. Reserve a room")
    print("2. Check out")
    print("3. Check all room status")
    print("4. Check rates")
    print("5. Logout")
    initial_opt=int(input("Enter (1/2/3/4/5):  "))
    if initial_opt==1:
        check_room()
    elif initial_opt==2:
        check_out()
    elif initial_opt==3:
        room_status()
    elif initial_opt==4:
        rate()
    elif initial_opt==5:
        log = False
        adm = False
    else:
        print("Please select from one of the given options!")


log=False
adm=False
def login():
    global log
    global adm
    if log==True:
        interf()
    else:
        user=input("Enter username:  ")
        passwd=input("Enter password:  ")
        auser=dbc.seetable("cred")[0][0]
        apass=dbc.seetable("cred")[0][1]
        suser=dbc.seetable("cred")[1][0]
        spass=dbc.seetable("cred")[1][1]


        #user=staff passwd=qazxsw@hotel@calif
        if user==suser: 
            if passwd==spass:
                log = True
            else:
                print("Values do not match the record, try again!")
        #user=admin passwd=admin@pwd@753
        elif user==auser:
            if passwd==apass:
                log = True
                adm = True
            else:
                print("Values do not match the record, try again!")
        else:
            print("Values do not match the record, try again!")
            log = False

flag = True
while flag:
    login()
