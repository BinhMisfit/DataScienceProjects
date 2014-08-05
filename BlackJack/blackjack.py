# Name: Nguyen Thanh Binh
# Email: ntbinhptnk@gmail.com
# Project: Black Jack game
# Version: 1.0
# References:
#   + http://www.blackjackinfo.com/blackjack-rules.php
# Rules:
# + The best hand in Blackjack is any card that has a value of 10 and an Ace, this hand is called a Blackjack and pays off 3 to 2.
# + If the dealer and the player both have a Blackjack it is called a push bet, which is a tie.
# + If the dealer and the player both have the same value of points it is also a push.
# + Any other win in Blackjack pays off even money.
# + The player will win the hand if their point value is higher than that of the dealer without going over the point value of 21.
# + If the dealer or player goes over the point value of 21 it is called a bust and they will lose the hand.
# + If the player and the dealer both bust the player will still lose the hand, which is the house advantage in the game of Blackjack.

import os
import random


SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

# define hand class
class Hand:
    def __init__(self):
        self.cards = list()
    def initial(self):
        return "gets: " + str(self.cards[0])+" *"
    def split_condition(self):
        if len(self.cards)==2 and str(self.cards[0].get_rank())==str(self.cards[1].get_rank()):
            return True
        else:
            return False
    def __str__(self):
        return "gets: " + " , ".join([str(i) for i in self.cards])
    def add_card(self, card):
        self.cards.append(card)
    def get_value(self):
        value = 0  # value when using the card A as 1 point.
        aces = 0  # aces counter
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES.get(rank)
            if rank == "A":
                aces += 1
        value_10 = value + (10 * aces) - aces  #value when using the card A as 10 points.
        if value_10 <= 21:
            value = value_10
        return value


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Please do not use invalid card here: ", suit, rank

    def __str__(self):
        return  self.rank+"#"+self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

# define deck class
class Deck:
    def __init__(self):
        self.cards = list()
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards) # creating a random deck for one game!

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        return "Deck contains " + " ".join([str(i) for i in self.cards])
        
def message():
    again = raw_input("Do you want to play again? (Y/N) : ")
    if (again == "Y" or again == "y"):
        game()
    else:
        print "\n\n-------Thank you for playing!--------\n\n"
        exit()

def player_info():
    print "Player "+ str(player.__str__())
    print "Player:"+ str(player.get_value())+" points"
def dealer_info():
    print "Dealer "+ str(dealer.__str__())
    print "Dealer:"+ str(dealer.get_value())+" points"

def hit():
    global player,player_chips, player_bet, end_deal
    player.add_card(deck.deal_card())
    print "Dealer "+ str(dealer.initial())
    player_info()
    if player.get_value() > 21:
        print "Sorry Player! You are busted."
        dealer_info()
        player_info()
        player_chips=player_chips-player_bet
        print "Player only has: "+str(player_chips)+" chips"
        end_deal= True

def double():
    global dealer, player_chips, player_bet, end_deal
    player_bet=player_bet*2 # Double bet!
    if player_bet>player_chips: # your bet is always smaller than your total chips!
        player_bet=player_chips
    player.add_card(deck.deal_card()) # Get one card and then stand!
    if player.get_value() > 21:
        print "Sorry Player! You are busted."
        dealer_info()
        player_info()
        player_chips=player_chips-player_bet
        print "Player only has: "+str(player_chips)+" chips"
        end_deal= True
    else:
        stand()
    
def surrender():
    global player_chips, end_deal
    print "Player has requested for surrendering the current game!"
    print "The request is accepted! Player lost one half of his bet!"
    player_chips=player_chips-float(player_bet/2)
    print "Player only has: "+str(player_chips)+" chips now"
    end_deal=True

def stand():
    global dealer, player_chips, player_bet, end_deal
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
        dealer_info()
        player_info()
        print "****************"
    if dealer.get_value() > 21:
        print "Congrats! Dealer is busted."
        dealer_info()
        player_info()
        player_chips=player_chips+player_bet
        print "Player has: "+str(player_chips)+" chips now"
        end_deal= True
    elif player.get_value() > dealer.get_value():
        print "Congrats! Player won!\n"
        dealer_info()
        player_info()
        player_chips=player_chips+player_bet
        print "Player has: "+str(player_chips)+" chips now"
        end_deal= True
    elif player.get_value() < dealer.get_value():
        print "Player lost!"
        dealer_info()
        player_info()
        player_chips=player_chips-player_bet
        print "Player only has: "+str(player_chips)+" chips"
        end_deal= True
    else:
        print "Push!"
        print "Dealer:"+ str(dealer.get_value())+" points"
        print "Player:"+ str(player.get_value())+" points"
        dealer_info()
        player_info()
        end_deal= True

def game():
    global deck, player, dealer, player_chips, player_bet, continue_game, end_deal
    print "Welcome to my blackjack game!"
    player_chips=100 # initial values
    continue_game='Y'
    while (player_chips>0 and continue_game=='Y'):
        deck=Deck()
        deck.shuffle()
        player = Hand()
        dealer = Hand()
        for i in range(2):
            dealer.add_card(deck.deal_card())
            player.add_card(deck.deal_card())
    
        print "--------------START NEW GAME--------------"
        print "Player has: "+str(player_chips)+" chips"
        player_bet=float(raw_input("How many chips will you bet for this game (at least 1 chip)?: "))
        if player_bet>player_chips:
            print "Only bet this game with a number of chips smaller than the total number of yours!"
            continue_game= raw_input("Do you want to continue (Y/N)?: ")
        else:
            split_request='N'
            if player.split_condition():
                player_info()
                print "Splitting is not supported in this version!"
            if split_request=='Y':
                print "Do something!"
            else:
                print "\n--------------Current Score--------------"
                print "Player has: "+str(player_chips)+" chips"
                print "Player bets: " + str(player_bet)+" chips"
                print "Dealer "+ str(dealer.initial())
                player_info()
            
                end_deal= False
                while not end_deal:
                    if len(player.cards)==2 and player.get_value()==21 and dealer.get_value()<21: # Black jack for player!!!!
                        print "Blackjack!"
                        player_chips=player_chips+player_bet*1.5
                        dealer_info()
                        player_info()
                        print "Player has: "+str(player_chips)+" chips now"
                        break
                    if len(dealer.cards)==2 and dealer.get_value()==21 and player.get_value()<21: # Black jack for dealer!!!!
                        print "Blackjack for dealer! Player lost!"
                        player_chips=player_chips-player_bet
                        dealer_info()
                        player_info()
                        print "Player has: "+str(player_chips)+" chips now"
                        break
                    if player.get_value() > 21:
                        print "Sorry Player! You are busted."
                        dealer_info()
                        player_info()
                        player_chips=player_chips-player_bet
                        print "Player only has: "+str(player_chips)+" chips"
                        end_deal= True
                        break
                    player_choice= raw_input("Player! Do you want to hit or stand or surrender or double (H/S/SD/D): ")
                    print "****************"
                    if player_choice=='H':
                        hit()
                        if len(player.cards)==5 and player.get_value()<21: # Having 5 cards for which the total value of cards is smaller than 21
                            print "Player won!"
                            dealer_info()
                            player_info()
                            player_chips=player_chips+player_bet
                            print "Player has: "+str(player_chips)+" chips now"
                            break
                    if player_choice=='S':
                        stand()
                    if player_choice=='SD':
                        surrender()
                    if player_choice=='D':
                        double()        
            if player_chips>0:
                continue_game= raw_input("Do you want to continue (Y/N)?: ")
            else:
                print "Go back home, man! You are too tired!"


if __name__ =="__main__":
    game()





    