from datetime import datetime

from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.data.builder.snap import builderAccessToken, builderQris
from python_nicepay.service.snapService import SnapService
from python_nicepay.util.utilLogging import Log

log = Log()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")


class testQris:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    amount = {
        "value": "1000.00",
        "currency": "IDR"
    }

    additionalInfo = {
        "goodsNm": "Merchant Goods 1",
        "billingNm": "John Doe",
        "billingPhone": "08123456789",
        "billingEmail": "john.doe@example.com",
        "billingAddr": "Jln. Raya Casablanka Kav.88",
        "billingCity": "South Jakarta",
        "billingState": "DKI Jakarta",
        "billingCountry": "Indonesia",
        "billingPostCd": "10200",
        "callBackUrl": "https://www.nicepay.co.id/IONPAY_CLIENT/paymentResult.jsp",
        "dbProcessUrl": "https://webhook.site/e15ef201-98a9-428c-85d4-a0c6458939c3",
        "userIP": "127.0.0.1",
        "cartData": "{\"count\":1,\"item\":[{\"img_url\":\"https://d3nevzfk7ii3be.cloudfront.net/igi/vOrGHXlovukA566A.medium\",\"goods_name\":\"Nokia 3360\",\"goods_detail\":\"Old Nokia 3360\",\"goods_amt\":\"100\",\"goods_quantity\":\"1\"}]}",
        "mitraCd": "QSHP"
    }

    bodyQris = (
        builderQris.BuildQris()
        .setMerchantId("IONPAYTEST")
        .setPartnerReferenceNo("OrdNo" + timestamp)
        .setStoreId("NICEPAY")
        .setValidityPeriod("")
        .setAmount(amount)
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyQris.jsonQris(),
                                            ConstantsEndpoints.qris())
