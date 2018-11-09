import base64
import sys
import traceback

import requests

import json



def doRestOperation(method, url, authString, payload=""):
    """[Performs REST operations]
    
    Arguments:
        method {[str]} -- [Rest HTTP metod ]
        url {[url]} -- [The REST url]
        authString {[str]} -- [Base64 string of AuthId and AuthToken]
    
    Keyword Arguments:
        payload {json} -- Tthe JSON Payload] (default: {""})
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        base_url = "https://api.plivo.com/v1/"
        headers = {'content-type': "application/json"}
        headers.update({"authorization": "Basic %s" % authString})
        print(method, base_url+url)
        response = requests.request(
            method, base_url + url, headers=headers, data=payload)
        print(response.text, response.status_code)
        return response.text, response.status_code
    except Exception as ex:
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def genAuthString(authId, authToken):
    """[Generates Base64 AuthString]
    
    Arguments:
        authId {[str]} -- [User authId]
        authToken {[str]} -- [User authToken]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        authId_token = authId+':'+authToken
        authString = base64.b64encode(authId_token.encode())
        return "".join(authString.decode().split())
    except Exception as ex:
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def listAllRentedNumbers(authId, authString):
    """[GET all the Numbers in the Pilvo account
    https://www.plivo.com/docs/api/number/]
    
    Arguments:
        authId {[str]} -- [User authId]
        authString {[str]} -- [Generated authString]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        expectedStatusCode = 200
        url = "Account/{0}/Number/".format(authId)
        method = "GET"
        responseText, responseStatusCode = doRestOperation(
            method, url, authString)
        if expectedStatusCode == responseStatusCode:
            return responseText
        else:
            raise Exception(sys._getframe().f_code.co_name +
                            " Status code didn't match. Expected- {Expected} Actual- {Actual}".format(Actual=responseStatusCode,Expected=expectedStatusCode))
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def extractNumber(responseText, no):
    """[Extracts number from responseText]
    
    Arguments:
        responseText {[str]} -- [response of method listAllRentedNumbers]
        no {[int]} -- [Total number to be extracted from responseText]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        jsonObj = json.loads(responseText)
        Numbers = []
        for i in range(no):
            num = jsonObj["objects"][i]["number"]
            Numbers.append(num)
        return Numbers
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def sendSms(Numbers, authId, authString):
    """[Send Sms
    https://www.plivo.com/docs/api/message/#send-a-message]
    
    Arguments:
        Numbers {[Array]} -- [Array of two numbers]
        authId {[str]} -- [User authId]
        authString {[str]} -- [Generated authString]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        expectedStatusCode = 202
        url = "Account/{0}/Message/".format(authId)
        method = "POST"
        payload = {}
        payload["src"] = Numbers[0]
        payload["dst"] = Numbers[1]
        msg = "Hello World!"
        payload["text"] = msg

        responseText, responseStatusCode = doRestOperation(
            method, url, authString, json.dumps(payload))
        if expectedStatusCode == responseStatusCode:
            return responseText
        else:
            raise Exception(sys._getframe().f_code.co_name +
                            "Status code did not match. Expected- {Expected} Actual- {Actual}'.format(Actual=responseStatusCode,Expected=expectedStatusCode)")
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def getMessageDetails(uuid, authId, authString):
    """[Fetches the message details from the  Uuid
    https://www.plivo.com/docs/api/message/]
    
    Arguments:
        uuid {[str]} -- [Message Uuid]
        authId {[str]} -- [User authId]
        authString {[str]} -- [Generated authString]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        expectedStatusCode = 200
        url = "/Account/{authId}/Message/{uuid}/".format(
            authId=authId, uuid=uuid)
        method = "GET"
        responseText, responseStatusCode = doRestOperation(
            method, url, authString)
        if expectedStatusCode == responseStatusCode:
            return responseText
        else:
            raise Exception(sys._getframe().f_code.co_name +
                            "Status code did not match. Expected- {Expected} Actual- {Actual}'.format(Actual=responseStatusCode,Expected=expectedStatusCode)")
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def getCountryPricing(country, authId, authString):
    """[Get the Pilvo Pricing according to the country
    https://www.plivo.com/docs/api/pricing/]
    
    Arguments:
        country {[str]} -- [Country code]
        authId {[str]} -- [User authId]
        authString {[str]} -- [Generated authString]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        expectedStatusCode = 200
        url = "Account/{authId}/Pricing/?country_iso={country}".format(
            authId=authId, country=country)
        method = "GET"
        responseText, responseStatusCode = doRestOperation(
            method, url, authString)
        if expectedStatusCode == responseStatusCode:
            return responseText
        else:
            raise Exception(sys._getframe().f_code.co_name +
                            "Status code did not match. Expected- {Expected} Actual- {Actual}'.format(Actual=responseStatusCode,Expected=expectedStatusCode)")
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def getCountryOfNumber(responseText):
    """[Gives the country code of the number]
    
    Arguments:
        responseText {[str]} -- [response of method listAllRentedNumbers ]
    """
    try:
        jsonObj = json.loads(responseText)
        countryDict = {"United States": "US"}
        for element in jsonObj["objects"]:
            country = countryDict[element["country"]]
        return country
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')


def getAccountDetails(authId, authString):
    """[fetches the User Account Details
    https://www.plivo.com/docs/api/pricing/]
    
    Arguments:
        authId {[str]} -- [User authId]
        authString {[str]} -- [Generated authString]
    """
    try:
        print(sys._getframe().f_code.co_name + ': Starting')
        expectedStatusCode = 200
        url = "Account/{authId}".format(authId=authId)
        method = "GET"
        responseText, responseStatusCode = doRestOperation(
            method, url, authString)
        if expectedStatusCode == responseStatusCode:
            return responseText
        else:
            raise Exception(sys._getframe().f_code.co_name +
                            "Status code did not match. Expected- {Expected} Actual- {Actual}'.format(Actual=responseStatusCode,Expected=expectedStatusCode)")
    except Exception as ex:
        print(str(ex))
        traceback.print_exc()
    finally:
        print(sys._getframe().f_code.co_name + ': Exiting')

