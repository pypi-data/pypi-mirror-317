from python_nicepay.data.builder.v2.enterprise import builderPayout
from python_nicepay.data.builder.v2.enterprise.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay


class testPayoutCancel:
    bodyPayoutCancel = (
        builderPayout.BuildPayoutCancel()
        .setTxid("IONPAYTEST07202411031722390627")
        .build()
    )

    response = ServiceNicepay.servicePayoutCancel(DataGenerator.getPayoutCancel(bodyPayoutCancel.jsonPayoutCancel()))
