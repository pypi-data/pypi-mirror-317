from python_nicepay.data.builder.snap import builderAccessToken, builderVirtualAccount
from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.service.snapService import SnapService
from python_nicepay.util.utilLogging import Log

log = Log()

class testVirtualAccountInquiry:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    totalAmount = {
        "value": "10000.00",
        "currency": "IDR"
    }

    additionalInfo = {
        "tXidVA": "IONPAYTEST02202411130910178964",
        "totalAmount": totalAmount,
        "trxId": "123",
    }

    bodyInquiryVA = (
        builderVirtualAccount.BuildInquiryVA()
        .setPartnerServiceId("")
        .setCustomerNo("")
        .setVirtualAccountNo("884800040910178964")
        .setInquiryRequestId("")
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyInquiryVA.jsonVAInquiry(),
                                            ConstantsEndpoints.inquiryVA())
