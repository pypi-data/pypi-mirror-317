from Crypto.SelfTest.IO.test_PKCS8 import clear_key

from python_nicepay.constants.constantsGeneral import ConstantsGeneral
from python_nicepay.data.builder.v2.enterprise import builderCartData, builderEwallet
from python_nicepay.data.builder.v2.enterprise.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay

class testEwallet:
    # Set the internal merchant configuration
    imid = "IONPAYTEST"
    merchantKey = "33F49GnCMS1mFYlGXisbUDzVf2ATWCl9k3R++d5hDd3Frmuos/XLx8XhXpe+LDYAbpGKZYSwtlyyLOtS/8aD7A=="
    callbackUrl = "https://dev.nicepay.co.id/IONPAY_CLIENT/paymentResult.jsp"
    dbProcessUrl = "https://webhook.site/e15ef201-98a9-428c-85d4-a0c6458939c3"

    ConstantsGeneral.setNonSnapConfiguration(imid, merchantKey, dbProcessUrl, callbackUrl)

    amt = 10000
    itemCartData = {
        "img_url": "https://cdn.eraspace.com/pub/media/catalog/product/i/p/iphone_13_pro_max_silver_1_5.jpg",
        "goods_name": "iPhone13ProMax",
        "goods_detail": "1TB-White",
        "goods_amt": amt,
        "goods_quantity": "1"
    }

    bodyCartData = (
        builderCartData.BuildCartData()
        .setCount("1")
        .setItem(itemCartData)
        .build()
    )

    bodyEwallet = (
        builderEwallet.BuildEwallet()
        .setPayMethod(ConstantsGeneral.getPayMethodEWallet())
        .setMitraCd("ESHP")
        .setUserIp(ConstantsGeneral.getUserIp())
        .setAmt(amt)
        .build()
    )

    response = ServiceNicepay.serviceRequest(DataGenerator.getTransactionBody(bodyEwallet.jsonEwallet(),
                                                                              bodyCartData.jsonCartData()))
