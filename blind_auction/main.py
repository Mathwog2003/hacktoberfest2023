from replit import clear
from art import logo
print(logo)

biddings = {}
bidders_alive = True
def highest_bidder(biddings):
    winner_name = ""
    bidding_amount = 0
    for key in biddings:
        price = biddings[key]
        if bidding_amount >= price :
            bidding_amount = bidding_amount
            winner_name = winner_name
        elif bidding_amount < price:
            bidding_amount = biddings[key]
            winner_name = key
    print(f"The winner is {winner_name} and their bid price is {bidding_amount}.")
    

while bidders_alive:
    name = input(" Enter Name : ")
    bid_price = int(input(" Enter Price : "))
    
    biddings[name] = bid_price
    response = input(" is there any other bidders 'yes' or 'no' : ")
    if response == 'no':
        highest_bidder(biddings)
        bidders_alive = False
    else: 
       clear()