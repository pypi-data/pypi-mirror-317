from python_nicepay.data.builder.v2.professional import builderCancel
from python_nicepay.data.builder.v2.professional.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay


class testCancel:
    bodyCancel = (
        builderCancel.BuildCancel()
        .setPayMethod("05")
        .setTxid("IONPAYTEST05202411062256225380")
        .setCancelType("1")
        .setCancelMsg("Test Cancel Python V2 Pro - n1tr0")
        .setAmt("1")
        .build()
    )

    response = ServiceNicepay.serviceCancel(DataGenerator.getCancelBody(bodyCancel.jsonCancel()))
