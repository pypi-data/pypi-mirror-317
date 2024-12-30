from datetime import datetime

from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.data.builder.snap import builderAccessToken, builderQris
from python_nicepay.service.snapService import SnapService
from python_nicepay.util.utilLogging import Log

log = Log()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")


class testQrisInquiry:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    additionalInfo = {

    }

    bodyQrisInquiry = (
        builderQris.BuildQrisInquiry()
        .setMerchantId("IONPAYTEST")
        .setExternalStoreId("NICEPAY")
        .setOriginalReferenceNo("IONPAYTEST08202411131421334722")
        .setOriginalPartnerReferenceNo("OrdNo20241113142133")
        .setServiceCode("51")
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyQrisInquiry.jsonQrisInquiry(),
                                            ConstantsEndpoints.inquiryQris())
