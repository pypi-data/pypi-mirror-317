class ConstantsGeneral:

    _SANDBOX_BASE_URL = "https://dev.nicepay.co.id/nicepay"
    _STAGING_BASE_URL = "https://staging.nicepay.co.id/nicepay"
    _PRODUCTION_BASE_URL = "https://www.nicepay.co.id/nicepay"

    # SNAP
    _PRIVATE_KEY = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAInJe1G22R2fMchIE6BjtYRqyMj6lurP" \
                   "/zq6vy79WaiGKt0Fxs4q3Ab4ifmOXd97ynS5f0JRfIqakXDcV/e2rx9bFdsS2HORY7o5At7D5E3tkyNM9smI" \
                   "/7dk8d3O0fyeZyrmPMySghzgkR3oMEDW1TCD5q63Hh/oq0LKZ/4Jjcb9AgMBAAECgYA4Boz2NPsjaE" \
                   "+9uFECrohoR2NNFVe4Msr8/mIuoSWLuMJFDMxBmHvO" \
                   "+dBggNr6vEMeIy7zsF6LnT32PiImv0mFRY5fRD5iLAAlIdh8ux9NXDIHgyera" \
                   "/PW4nyMaz2uC67MRm7uhCTKfDAJK7LXqrNVDlIBFdweH5uzmrPBn77foQJBAMPCnCzR9vIfqbk7gQa" \
                   "A0hVnXL3qBQPMmHaeIk0BMAfXTVq37PUfryo+80XXgEP1mN/e7f10GDUPFiVw6Wfwz38CQQC0L+xoxraftGnw" \
                   "FcVN1cK/MwqGS+DYNXnddo7Hu3+RShUjCz5E5NzVWH5yHu0E0Zt3sdYD2t7u7HSr9wn96OeDAkEApzB6eb0JD1kDd3P" \
                   "eilNTGXyhtIE9rzT5sbT0zpeJEelL44LaGa/pxkblNm0K2v/ShMC8uY6Bbi9oVqnMbj04uQJAJDIgTmfkla5bPZRR/zG6n" \
                   "kf1jEa/0w7i/R7szaiXlqsIFfMTPimvRtgxBmG6ASbOETxTHpEgCWTMhyLoCe54WwJATmPDSXk4APUQNvX5rr5OSfGWEOo67c" \
                   "KBvp5Wst+tpvc6AbIJeiRFlKF4fXYTb6HtiuulgwQNePuvlzlt2Q8hqQ=="
    _CLIENT_KEY = "IONPAYTEST"
    # _CLIENT_KEY = "NORMALTEST"
    _CLIENT_SECRET = "33F49GnCMS1mFYlGXisbUDzVf2ATWCl9k3R++d5hDd3Frmuos/XLx8XhXpe+LDYAbpGKZYSwtlyyLOtS/8aD7A=="
    # _CLIENT_SECRET = "1cdc38d0c296e4427d8bd7ebe3b585834a7392fb919ebd482f71b28ec64bdb7a"
    # _CLIENT_SECRET = "1af9014925cab04606b2e77a7536cb0d5c51353924a966e503953e010234108a"

    #V2
    _I_MID = "IONPAYTEST"  # AUTO_PAID_VA
    # _I_MID = "FIXOPEN001" #FIX_OPEM
    # _I_MID = "NORMALTEST" #NORMAL_TEST
    _MERCHANT_KEY = "33F49GnCMS1mFYlGXisbUDzVf2ATWCl9k3R++d5hDd3Frmuos/XLx8XhXpe+LDYAbpGKZYSwtlyyLOtS/8aD7A=="
    _PAY_METHOD_CREDIT_CARD = "01"
    _PAY_METHOD_VIRTUAL_ACCOUNT = "02"
    _PAY_METHOD_CONVENIENCE_STORE = "03"
    _PAY_METHOD_DIRECT_DEBIT = "04"
    _PAY_METHOD_E_WALLET = "05"
    _PAY_METHOD_PAYLOAN = "06"
    _PAY_METHOD_PAYOUT = "07"
    _PAY_METHOD_QRIS = "08"
    _PAY_METHOD_GPN = "09"
    _CURRENCY = "IDR"
    _CALLBACK_URL = "https://dev.nicepay.co.id/IONPAY_CLIENT/paymentResult.jsp"
    _DB_PROCESS_URL = "https://webhook.site/e15ef201-98a9-428c-85d4-a0c6458939c3"
    _USER_IP = "127.0.0.1"
    _USER_SESSION_ID = ""
    _USER_AGENT = ""
    _USER_LANGUAGE = ""
    _SHOP_ID = "NICEPAY"

    # Getter
    @staticmethod
    def getSandboxBaseUrl():
        return ConstantsGeneral._SANDBOX_BASE_URL

    @staticmethod
    def getStagingBaseUrl():
        return ConstantsGeneral._STAGING_BASE_URL

    @staticmethod
    def getProductionBaseUrl():
        return ConstantsGeneral._PRODUCTION_BASE_URL

    @staticmethod
    def getPrivateKey():
        return ConstantsGeneral._PRIVATE_KEY

    @staticmethod
    def getClientKey():
        return ConstantsGeneral._CLIENT_KEY

    @staticmethod
    def getClientSecret():
        return ConstantsGeneral._CLIENT_SECRET

    #V2
    @staticmethod
    def getImid():
        return ConstantsGeneral._I_MID

    @staticmethod
    def getMerchantKey():
        return ConstantsGeneral._MERCHANT_KEY

    @staticmethod
    def getPayMethodCreditCard():
        return ConstantsGeneral._PAY_METHOD_CREDIT_CARD

    @staticmethod
    def getPayMethodVirtualAccount():
        return ConstantsGeneral._PAY_METHOD_VIRTUAL_ACCOUNT

    @staticmethod
    def getPayMethodConvenienceStore():
        return ConstantsGeneral._PAY_METHOD_CONVENIENCE_STORE

    @staticmethod
    def getPayMethodDirectDebit():
        return ConstantsGeneral._PAY_METHOD_DIRECT_DEBIT

    @staticmethod
    def getPayMethodEWallet():
        return ConstantsGeneral._PAY_METHOD_E_WALLET

    @staticmethod
    def getPayMethodPayloan():
        return ConstantsGeneral._PAY_METHOD_PAYLOAN

    @staticmethod
    def getPayMethodPayout():
        return ConstantsGeneral._PAY_METHOD_PAYOUT

    @staticmethod
    def getPayMethodQris():
        return ConstantsGeneral._PAY_METHOD_QRIS

    @staticmethod
    def getPayMethodGpn():
        return ConstantsGeneral._PAY_METHOD_GPN

    @staticmethod
    def getCurrency():
        return ConstantsGeneral._CURRENCY

    @staticmethod
    def getCallbackUrl():
        return ConstantsGeneral._CALLBACK_URL

    @staticmethod
    def getDbProcessUrl():
        return ConstantsGeneral._DB_PROCESS_URL

    @staticmethod
    def getUserIp():
        return ConstantsGeneral._USER_IP

    @staticmethod
    def getShopId():
        return ConstantsGeneral._SHOP_ID

    # Setter
    @staticmethod
    def setSandboxBaseUrl(value):
        ConstantsGeneral._SANDBOX_BASE_URL = value

    @staticmethod
    def setStagingBaseUrl(value):
        ConstantsGeneral._STAGING_BASE_URL = value

    @staticmethod
    def setProductionBaseUrl(value):
        ConstantsGeneral._PRODUCTION_BASE_URL = value

    @staticmethod
    def setPrivateKey(value):
        ConstantsGeneral._PRIVATE_KEY = value

    @staticmethod
    def setClientKey(value):
        ConstantsGeneral._CLIENT_KEY = value

    @staticmethod
    def setClientSecret(value):
        ConstantsGeneral._CLIENT_SECRET = value

    @staticmethod
    def setImid(value):
        ConstantsGeneral._I_MID = value

    @staticmethod
    def setMerchantKey(value):
        ConstantsGeneral._MERCHANT_KEY = value

    @staticmethod
    def setPayMethodCreditCard(value):
        ConstantsGeneral._PAY_METHOD_CREDIT_CARD = value

    @staticmethod
    def setPayMethodVirtualAccount(value):
        ConstantsGeneral._PAY_METHOD_VIRTUAL_ACCOUNT = value

    @staticmethod
    def setPayMethodConvenienceStore(value):
        ConstantsGeneral._PAY_METHOD_CONVENIENCE_STORE = value

    @staticmethod
    def setPayMethodDirectDebit(value):
        ConstantsGeneral._PAY_METHOD_DIRECT_DEBIT = value

    @staticmethod
    def setPayMethodEWallet(value):
        ConstantsGeneral._PAY_METHOD_E_WALLET = value

    @staticmethod
    def setPayMethodPayloan(value):
        ConstantsGeneral._PAY_METHOD_PAYLOAN = value

    @staticmethod
    def setPayMethodPayout(value):
        ConstantsGeneral._PAY_METHOD_PAYOUT = value

    @staticmethod
    def setPayMethodQris(value):
        ConstantsGeneral._PAY_METHOD_QRIS = value

    @staticmethod
    def setPayMethodGpn(value):
        ConstantsGeneral._PAY_METHOD_GPN = value

    @staticmethod
    def setCurrency(value):
        ConstantsGeneral._CURRENCY = value

    @staticmethod
    def setCallbackUrl(value):
        ConstantsGeneral._CALLBACK_URL = value

    @staticmethod
    def setDbProcessUrl(value):
        ConstantsGeneral._DB_PROCESS_URL = value

    @staticmethod
    def setUserIp(value):
        ConstantsGeneral._USER_IP = value

    @staticmethod
    def setShopId(value):
        ConstantsGeneral._SHOP_ID = value

    # Setter for merchant
    @staticmethod
    def setNonSnapConfiguration(imId, merchantKey, dbProcessUrl, callbackUrl):
        ConstantsGeneral._I_MID = imId
        ConstantsGeneral._MERCHANT_KEY = merchantKey
        ConstantsGeneral._DB_PROCESS_URL = dbProcessUrl
        ConstantsGeneral._CALLBACK_URL = callbackUrl

    @staticmethod
    def setSnapConfiguration(clientKey, clientSecret, privateKey):
        ConstantsGeneral._CLIENT_KEY = clientKey
        ConstantsGeneral._CLIENT_SECRET = clientSecret
        ConstantsGeneral._PRIVATE_KEY = privateKey