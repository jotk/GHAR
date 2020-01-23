#!/usr/bin/env python3

import realEstateAPI
import sys
import string
import APIconnectToDB

def fixMyAdressFromCL(address):
    for index in range(0,len(address)): #removes common punctuation from command line input
        address[index] = address[index].strip(',').strip('.')
        if address[index] == "": #removes any punctuation on own
            address.pop(index)


def main():
    suc = False
    while suc is False:
        address = input("Enter address in same format as 1234 Innovation Dr., Boulder, CO: \n ").split(' ')
        fixMyAdressFromCL(address)
        myCall = realEstateAPI.homeInfo(address)  # realEstateAPI API for given address
        suc = True
        # try:
        #      myCall = realEstateAPI.homeInfo(address) #realEstateAPI API for given address
        #      suc = True
        # except Exception as e:
        #     print(e)
    print("Name of owner: ", myCall.ownerName)
    print("Year built of property: ", myCall.year_built)
    print("Price bought: ", myCall.price)
    print("Current Value: ", myCall.value)
    print("Market Growth on Record: ", myCall.market_value_change_year)
    print("Forecasted Value: ", myCall.forecast_year)
    print("Suggested Rental: ", myCall.suggested_rental)




if __name__ == "__main__" :
    main()
