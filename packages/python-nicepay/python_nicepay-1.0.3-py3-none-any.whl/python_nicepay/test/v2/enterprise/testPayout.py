from python_nicepay.data.builder.v2.enterprise import builderPayout
from python_nicepay.data.builder.v2.enterprise.dataGenerator import DataGenerator
from python_nicepay.service.v2EnterpriseService import ServiceNicepay


class testPayout:
    bodyPayout = (
        builderPayout.BuildPayout()
        .setAccountNo("5345000060")
        .setBenefNm("John Doe")
        .setBenefPhone("012345678910")
        .setBenefStatus("1")
        .setBenefType("1")
        .setBankCd("BMRI")
        .setPayoutMethod("1")
        .setReferenceNo("NITRO0001X")
        .setReservedDt("20241104") # Mandatory for CANCEL
        .setReservedTm("120000") # Mandatory for CANCEL
        .setAmt("10000")
        .setDescription("Testing Payout - n1tr0")
        .build()
    )

    response = ServiceNicepay.servicePayoutReg(DataGenerator.getPayoutRegBody(bodyPayout.jsonPayout()))
