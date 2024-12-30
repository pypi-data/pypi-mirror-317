from datetime import datetime

from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.data.builder.snap import builderAccessToken, builderDirectDebit
from python_nicepay.service.snapService import SnapService
from python_nicepay.util.utilLogging import Log

log = Log()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")


class testDirectDebitInquiry:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    amount = {
        "value": "1.00",
        "currency": "IDR"
    }

    additionalInfo = {}

    bodyDirectDebitInquiry = (
        builderDirectDebit.BuildDirectDebitInquiry()
        .setMerchantId("IONPAYTEST")
        .setSubMerchantId("")
        .setOriginalPartnerReferenceNo("OrdNo20241113140616")
        .setOriginalReferenceNo("IONPAYTEST05202411131406163958")
        .setServiceCode("54")
        .setTransactionDate(timestamp)
        .setAmount(amount)
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyDirectDebitInquiry.jsonDirectDebitInquiry(),
                                            ConstantsEndpoints.inquiryDirectDebit())
