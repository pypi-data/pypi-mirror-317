from python_nicepay.data.builder.v2.professional import builderInquiry
from python_nicepay.data.builder.v2.professional.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay


class testInquiry:
    bodyInquiry = (
        builderInquiry.BuildInquiry()
        .setTxid("IONPAYTEST00202411091903501068")
        .setReferenceNo("OrdNo20241109190350")
        .setAmt("10000")
        .build()
    )

    response = ServiceNicepay.serviceInquiry(DataGenerator.getInquiryBody(bodyInquiry.jsonInquiry()))
