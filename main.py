from __future__ import print_function, absolute_import, with_statement

import cfonts
import db_connect as dbc

dbc.connect('hotel_t1')

cfonts.say("WELCOME TO HOTEL CALIFORNIA", font='chrome', colors=['candy', 'candy', 'candy'], align='center', space=True)

def guest():
    dbc.create('guest_t2', "'fname', 'lname', 'phone', 'email', 'address', 'adults', 'child', 'stay', 'room_no'")
    check_room()
    # personal info
    fname = input("First Name:  ")
    lname = input("Last Name:  ")
    # contact
    while True:
        phone = input("Phone Number:  ")
        if (phone.isnumeric()) and (8<len(phone)<12) and (" " not in phone) and (phone.startswith("09") or phone.startswith("07") or phone.startswith("91")):
        #if all( [phone.isnumeric(), 8<len(phone.strip())<=12, phone.startswith( ("09","07" ,"91") ) ] ) :
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
            
    address = input("Guest's Address:  ")
    # reservation info
    adults = input("Number of Adults:  ")
    child = input("Number of Children:  ")
    stay = input("Number of Days of stay:  ")
    # room
    room_no = input("Enter the room number to reserve:  ")
    upd_cond = "room_no="+room_no
    dbc.update("rooms", "status='R'", upd_cond)
    y_n = input("Do you want to continue ? [y/n]")
    if y_n in ["n", "N", "No"]:
        print("Thank you")
        global flag
        flag = False

def check_room():
    beds = input("Number of beds:  ")
    ac = input("AC required (y/n):  ").upper()
    tv = input("TV required (y/n):  ").upper()
    wifi = input("WIFI required (y/n):  ").upper()
    _filter = "beds="+beds+" AND ac="+"'"+ac+"'"+" AND tv="+"'"+tv+"'"
    available = dbc.get("rooms", "room_no", _filter)
    print("ROOMS AVAILABLE:")
    for Number in available:
        print(Number[0])

flag = True
while flag:
    guest()
