from python_nicepay.data.builder.v2.enterprise import builderInquiry
from python_nicepay.data.builder.v2.enterprise.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay


class testInquiry:
    bodyInquiry = (
        builderInquiry.BuildInquiry()
        .setTxid("IONPAYTEST08202411031727220880")
        .setReferenceNo("OrdNo20241103172721")
        .setAmt("10000")
        .build()
    )

    response = ServiceNicepay.serviceInquiry(DataGenerator.getInquiryBody(bodyInquiry.jsonInquiry()))
