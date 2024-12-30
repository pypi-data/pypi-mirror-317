from python_nicepay.data.builder.snap import builderAccessToken, builderVirtualAccount
from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.service.snapService import SnapService
from python_nicepay.util.utilLogging import Log

log = Log()


class testVirtualAccount:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    totalAmount = {"value": "10000.00",
                   "currency": "IDR"
                   }

    additionalInfo = {"bankCd": "BRIN",
                      "goodsNm": "Merchant Goods 1",
                      "dbProcessUrl": "https://webhook.site/e15ef201-98a9-428c-85d4-a0c6458939c3",
                      "vacctValidDt": "",
                      "vacctValidTm": "",
                      "msId": "",
                      "msFee": "",
                      "msFeeType": "",
                      "mbFee": "",
                      "mbFeeType": ""
                      }

    bodyCreateVA = (
        builderVirtualAccount.BuildCreateVA()
        .setPartnerServiceId("")
        .setCustomerNo("")
        .setVirtualAccountNo("")
        .setVirtualAccountName("John Doe")
        .setTrxId("123")
        .setTotalAmount(totalAmount)
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyCreateVA.jsonVACreate(),
                                            ConstantsEndpoints.createVA())
