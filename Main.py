import json
import sys

from PilvoRestCalls import *


def buisnessLogic(authId, authString):
    """[Cointains the Buisness Logic]
    
    Arguments:
        authId {[str]} -- [User authId]
        authString {[str]} -- [Generated authString]
    """
    try:
        responseText_getAccountDetails = getAccountDetails(authId, authString)
        currentCredits = float(json.loads(
            responseText_getAccountDetails)["cash_credits"])
        print("Pre Operation credit:"+str(currentCredits))

        responseText_listAllRentedNumbers = listAllRentedNumbers(
            authId, authString)

        Numbers = extractNumber(responseText_listAllRentedNumbers, 2)

        responseText_sendSms = sendSms(Numbers, authId, authString)
        msgUuid = json.loads(responseText_sendSms)["message_uuid"][0]

        responseText_getMessageDetails = getMessageDetails(
            msgUuid, authId, authString)
        actualChargedAmount = float(json.loads(responseText_getMessageDetails)[
            "total_amount"])

        country = getCountryOfNumber(responseText_listAllRentedNumbers)

        responseText_getCountryPricing = getCountryPricing(
            country, authId, authString)
        expectedChargedAmount = float(json.loads(responseText_getCountryPricing)[
            "message"]["outbound"]["rate"])

        print("expected Charged Amount: "+str(expectedChargedAmount))
        print("actual Charged Amount: "+str(actualChargedAmount))
        assert expectedChargedAmount == actualChargedAmount
        print("Verified! expected Charged Amount == actual Charged Amount")

        responseText_getAccountDetails = getAccountDetails(authId, authString)
        postOperationCredits = float(json.loads(
            responseText_getAccountDetails)["cash_credits"])
        print("Post Operation credit:"+str(postOperationCredits))

        costDifference = round(currentCredits-postOperationCredits, 4)
        assert costDifference == actualChargedAmount
        print('Verified! Correct amount is deducted from the Account Credits i.e. : '+str(costDifference))
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()



# if __name__ == "__main__":
def test_main():
    """[Provide the User authId and authToken Here]
    """
    authId = "MAODUZYTQ0Y2FMYJBLOW"
    authToken = "Mzk0MzU1Mzc3MTc1MTEyMGU2M2RlYTIwN2UyMzk1"
    authString = genAuthString(authId, authToken)
    buisnessLogic(authId, authString)
