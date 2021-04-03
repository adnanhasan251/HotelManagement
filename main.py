from __future__ import print_function, absolute_import, with_statement
import pandas as pd
import stdiomask
import cfonts
import db_connect as dbc
from tabulate import tabulate

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


dbc.connect('hotel_t1')

cfonts.say("WELCOME TO HOTEL CALIFORNIA", font='chrome', colors=['candy', 'candy', 'candy'], align='center', space=True)

def guest():
    dbc.create('guest_t2', "'fname', 'lname', 'phone', 'email', 'address', 'adults', 'child', 'stay', 'room_no', 'wifi'")
    # personal info
    fname = input(bcolors.OKGREEN+"First Name:  "+bcolors.ENDC)
    lname = input(bcolors.OKGREEN+"Last Name:  "+bcolors.ENDC)
    # contact
    while True:
        phone = input(bcolors.OKGREEN+"Phone Number:  "+bcolors.ENDC)
        if (phone.isnumeric()) and (8<len(phone)<13) and (" " not in phone):
            break
        else:
            print(bcolors.FAIL+"Invalid phone number"+bcolors.ENDC)

 

    while True:
        email = input(bcolors.OKGREEN+"Email:  "+bcolors.ENDC)
        if "@" in email:
            a=email.partition("@")
            if len(a[0])!=0 and len(a[2])!=0 and "@" not in a[0] and "@" not in a[2]:
                break
            else:
                print(bcolors.FAIL+"Invalid email"+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"Invalid email"+bcolors.ENDC)


            
    while True:
        address = input(bcolors.OKGREEN+"Guest's Address:  "+bcolors.ENDC)
        if address.isalnum() and len(address)!=0:
            break
        else:
            print(bcolors.FAIL+"Invalid"+bcolors.ENDC)
    # reservation info
    while True:
        adults = input(bcolors.OKGREEN+"Number of Adults:  "+bcolors.ENDC)
        if int(adults)>=0 and adults.isnumeric():
            break
        else:
            print(bcolors.FAIL+"Invalid number"+bcolors.ENDC)
    while True:
        child = input(bcolors.OKGREEN+"Number of Children:  "+bcolors.ENDC)
        if int(child)>=0 and child.isnumeric():
            break
        else:
            print(bcolors.FAIL+"Invalid number"+bcolors.ENDC)
    while True:
        stay = input(bcolors.OKGREEN+"Number of Days of stay:  "+bcolors.ENDC)
        if int(stay)>=0 and stay.isnumeric():
            break
        else:
            print(bcolors.FAIL+"Invalid number"+bcolors.ENDC)
    wifi=input(bcolors.OKGREEN+"Wifi access required (y/n):  "+bcolors.ENDC).upper()
    # room
    room_no = input(bcolors.OKGREEN+"Enter the room number to reserve:  "+bcolors.ENDC)
    #insert guest details in database
    data="'"+fname+"', '"+lname+"', "+phone+", '"+email+"', '"+address+"', "+adults+", "+child+", "+stay+", "+room_no+", '"+wifi+"'"
    dbc.insert("guest_t2", data)
    #update room status
    upd_cond = "room_no="+room_no
    dbc.update("rooms", "status='R'", upd_cond)

    #confirmation for room allotment
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

    print(bcolors.BOLD+"\n\n***********  ROOM ALLOTMENT ************\n\n"+bcolors.ENDC)
    print(tabulate(chosen, tablefmt="fancy_grid"))
    con_trans = input(bcolors.OKGREEN+"Do you want to confirm reservation ? [y/n]"+bcolors.ENDC)
    if con_trans in ["y", "Y", "Yes", "YES"]:
        print(bcolors.OKCYAN+"\n\nReservation Successful\n\n"+bcolors.ENDC)

    y_n = input(bcolors.OKGREEN+"\nDo you want to book another room ? [y/n]\n"+bcolors.ENDC)
    if y_n in ["n", "N", "No"]:
        print(bcolors.OKCYAN+"Thank you"+bcolors.ENDC)
        global flag
        flag = False

def check_room():
    beds = input(bcolors.OKGREEN+"Number of beds:  "+bcolors.ENDC)
    ac = input(bcolors.OKGREEN+"AC required (y/n):  "+bcolors.ENDC).upper()
    tv = input(bcolors.OKGREEN+"TV required (y/n):  "+bcolors.ENDC).upper()
    _filter = "beds="+beds+" AND ac="+"'"+ac+"'"+" AND tv="+"'"+tv+"'"+" AND status='NR'"
    available = dbc.get("rooms", "room_no", _filter)
    print(bcolors.UNDERLINE+"ROOMS AVAILABLE:"+bcolors.ENDC)
    for Number in available:
        print(Number[0])
    print(bcolors.OKCYAN+'''Please select an option
    1. Reserve a room
    2. Check another room'''+bcolors.ENDC)
    opt=int(input(bcolors.OKGREEN+"(1/2):  "+bcolors.ENDC))
    if opt==1:
        guest()
    elif opt==2:
        check_room()

def check_out():
    roomno=input(bcolors.OKGREEN+"Enter the room number to check out:  "+bcolors.ENDC)
    stay=int(input(bcolors.OKGREEN+"Days stayed?:  "+bcolors.ENDC))
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

    #generating bill

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

    co=input(bcolors.WARNING+"Do you want to check out? (y/n)"+bcolors.ENDC)
    if co.lower()=="y":
        #Print BILL
        print(bcolors.BOLD+"\n\n***********  INVOICE ************\n\n"+bcolors.ENDC)
        print(tabulate(inv, tablefmt="fancy_grid"))
        con_trans = input(bcolors.OKGREEN+"Do you want to confirm transaction ? [y/n]"+bcolors.ENDC)
        if con_trans in ["y", "Y", "Yes", "YES"]:
            print(bcolors.OKCYAN+"\n\nTransaction Successful\n\n"+bcolors.ENDC)

        y_n = input(bcolors.OKGREEN+"\nDo you want to book another room ? [y/n]\n"+bcolors.ENDC)
        if y_n in ["n", "N", "No"]:
            print(bcolors.OKCYAN+"Thank you"+bcolors.ENDC)
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
    print(bcolors.OKCYAN+'''Please select an option:
    1. See all the room status
    2. See guests details (admin only)
    3. Back to Main Menu'''+bcolors.ENDC)
    opt=int(input(bcolors.OKGREEN+"Enter (1/2/3):  "+bcolors.ENDC))
    if opt==1:
        print(bcolors.UNDERLINE+"ROOMS:"+bcolors.ENDC)
        print(room_)
    elif opt==2:
        if adm==True:
            print(bcolors.UNDERLINE+"GUESTS:"+bcolors.ENDC)
            print(guest_)
        else:
            print(bcolors.WARNING+"You need admin priviledge to view the data"+bcolors.ENDC)
            opt=input(bcolors.OKGREEN+"Do you want to login as admin? (y/n)"+bcolors.ENDC).lower()
            if opt=='y':
                log = False
                login()
    elif opt==3:
        print(bcolors.UNDERLINE+"Main Menu:"+bcolors.ENDC)
    else:
        print(bcolors.FAIL+"Please select from one of the given options!"+bcolors.ENDC)
        room_status()


def rate():
    global log
    rate=dbc.seetable("rate")
    rate_=pd.DataFrame(rate, columns=['Item', 'Rate per day'])
    print(rate_)
    opt=input(bcolors.OKGREEN+"Do you want to change rates (admin only)? (y/n)"+bcolors.ENDC).lower()
    if opt=='y':
        if adm==True:
            print(bcolors.OKCYAN+'''Which rate do you want to change?
            1. Charge of 'n' bed per day
            2. Charge of AC/TV/Wifi per day'''+bcolors.ENDC)
            opt2=int(input(bcolors.OKGREEN+"Enter (1/2):  "+bcolors.ENDC))
            if opt2==1:
                nbed=int(input(bcolors.OKGREEN+"Enter the number of beds (1/2/3) of which you wish to change rates:  "+bcolors.ENDC))
                item="item='"+str(nbed)+" bed'"
                crate=dbc.get("rate","rpd", item)[0][0]
                print("Current rate is Rs."+str(crate))
                nrate=int(input("Enter the new rate (Rs.):  "))
                uptr="rpd="+str(nrate)
                dbc.update('rate', uptr, item)
                print("The new is set to Rs."+str(nrate))
            if opt2==2:
                print(bcolors.OKCYAN+'''Please select one of the options:
                1. TV, 2. AC, 3. Wifi'''+bcolors.ENDC)
                opt3=int(input(bcolors.OKGREEN+"Enter (1/2/3:  "+bcolors.ENDC))
                items=['tv', 'ac', 'wifi']
                item="item='"+items[(opt3)-1]+"'"
                crate=dbc.get("rate","rpd", item)[0][0]
                print("Current rate is Rs."+str(crate))
                nrate=int(input(bcolors.OKGREEN+"Enter the new rate (Rs.):  "+bcolors.ENDC))
                uptr="rpd="+str(nrate)
                dbc.update('rate', uptr, item)
                print(bcolors.OKCYAN+"The new is set to Rs."+str(nrate)+bcolors.ENDC)
        else:
                print(bcolors.WARNING+"You need admin priviledge to change the rates"+bcolors.ENDC)
                opt=input(bcolors.OKGREEN+"Do you want to login as admin? (y/n)"+bcolors.ENDC).lower()
                if opt=='y':
                    log = False
                    login()

def interf():
    global log
    global adm
    print(bcolors.OKCYAN+'''Please choose a option:
    1. Reserve a room
    2. Check out
    3. Check all room status
    4. Check rates
    5. Logout'''+bcolors.ENDC)
    initial_opt=int(input(bcolors.OKGREEN+"Enter (1/2/3/4/5):  "+bcolors.ENDC))
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
        print(bcolors.FAIL+"Please select from one of the given options!"+bcolors.ENDC)


log=False
adm=False
def login():
    global log
    global adm
    if log==True:
        interf()
    else:
        user=input(bcolors.OKGREEN+"Enter username:  "+bcolors.ENDC)
        passwd=stdiomask.getpass(prompt=bcolors.OKGREEN+"Enter password:  "+bcolors.ENDC)
        auser=dbc.seetable("cred")[0][0]
        apass=dbc.seetable("cred")[0][1]
        suser=dbc.seetable("cred")[1][0]
        spass=dbc.seetable("cred")[1][1]


        #user=staff passwd=hotelstaff123
        if user==suser: 
            if passwd==spass:
                log = True
            else:
                print(bcolors.FAIL+"Values do not match the record, try again!"+bcolors.ENDC)
        #user=admin passwd=hoteladmin123
        elif user==auser:
            if passwd==apass:
                log = True
                adm = True
            else:
                print(bcolors.FAIL+"Values do not match the record, try again!"+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"Values do not match the record, try again!"+bcolors.ENDC)
            log = False

flag = True
while flag:
    login()
