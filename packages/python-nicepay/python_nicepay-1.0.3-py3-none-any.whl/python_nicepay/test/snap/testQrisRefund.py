from datetime import datetime

from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.data.builder.snap import builderAccessToken, builderQris
from python_nicepay.service.snapService import SnapService
from python_nicepay.util.utilLogging import Log

log = Log()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
class testQrisRefund:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    refundAmount = {
        "value": "1000.00",
        "currency": "IDR"
    }

    additionalInfo = {
        "cancelType": "1"
    }

    bodyQrisInquiry = (
        builderQris.BuildQrisRefund()
        .setMerchantId("IONPAYTEST")
        .setExternalStoreId("NICEPAY")
        .setOriginalReferenceNo("IONPAYTEST08202411140055296692")
        .setOriginalPartnerReferenceNo("OrdNo20241114005529")
        .setPartnerRefundNo("51")
        .setRefundAmount(refundAmount)
        .setReason("Test Refund QRIS SNAP")
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyQrisInquiry.jsonQrisRefund(),
                                            ConstantsEndpoints.refundQris())
    