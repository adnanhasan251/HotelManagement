from db_connect import *
import cfonts

connect('hotel_t1')

cfonts.say("WELCOME TO HOTEL CALIFORNIA", font='chrome', colors=['candy', 'candy', 'candy'], align='center', space=True)

def guest():
    create('guest_t2', "'fname', 'lname', 'phone', 'email', 'address', 'adults', 'child', 'stay', 'room_no'")
    check_room()
    #personal info
    fname=input("First Name:  ")
    lname=input("Last Name:  ")
    #contact
    phone=input("Phone Number:  ")
    email=input("Email:  ")
    address=input("Guest's Address:  ")
    #reservation info
    adults=input("Number of Adults:  ")
    child=input("Number of Children:  ")
    stay=input("Number of Days of stay:  ")
    #room
    room_no=input("Enter the room number to reserve:  ")
    data="'"+fname+"', '"+lname+"', "+phone+", '"+email+"', '"+address+"', "+adults+", "+child+", "+stay+", "+room_no
    insert("guest_t2", data)
    upd_cond="room_no="+room_no
    update("rooms", "status='R'", upd_cond)

def check_room():
    beds=input("Number of beds:  ")
    ac=input("AC required (y/n):  ").upper()
    tv=input("TV required (y/n):  ").upper()
    wifi=input("WIFI required (y/n):  ").upper()
    filter = "beds="+beds+" AND ac="+"'"+ac+"'"+" AND tv="+"'"+tv+"'"
    available=get("rooms", "room_no", filter)
    print("ROOMS AVAILABLE:")
    for Number in available:
        print(Number[0])
guest()
