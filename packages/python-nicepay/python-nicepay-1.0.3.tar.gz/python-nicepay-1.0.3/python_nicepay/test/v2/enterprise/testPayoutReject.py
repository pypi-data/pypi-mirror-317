from python_nicepay.data.builder.v2.enterprise import builderPayout
from python_nicepay.data.builder.v2.enterprise.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay


class testPayoutReject:
    bodyPayoutReject = (
        builderPayout.BuildPayoutReject()
        .setTxid("IONPAYTEST07202410110001153231")
        .build()
    )

    response = ServiceNicepay.servicePayoutReject(DataGenerator.getPayoutReject(
        bodyPayoutReject.jsonPayoutReject()))
