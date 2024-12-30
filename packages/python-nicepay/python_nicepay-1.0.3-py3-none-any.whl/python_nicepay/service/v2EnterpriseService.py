import json

from python_nicepay.config.apiClient import apiClient
from python_nicepay.constants.constantsEndpoint import ConstantsEndpoints
from python_nicepay.constants.constantsGeneral import ConstantsGeneral
from python_nicepay.data.builder.v2.enterprise.dataGenerator import DataGenerator
from python_nicepay.util.utilLogging import Log

log = Log()
host = ConstantsGeneral.getSandboxBaseUrl()  # Environment

class ServiceNicepay:
    log.headers("Initialization")

    # REGISTRATION REQUEST
    @staticmethod
    def serviceRequest(body):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.registration()
        data = apiClient.send(host,
                              headers,
                              body,
                              endpoint)

        response = json.dumps(data)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(body))
        log.info("Response Data : " + json.dumps(data))
        return response

    # PAYMENT REQUEST
    @staticmethod
    def servicePayment(data):
        endpoint = ConstantsEndpoints.payment()
        response = apiClient.get(host,
                                 data,
                                 endpoint)
        # a = json.dumps(response)
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))
        # log.info(response)
        return response

    # CANCEL REQUEST
    @staticmethod
    def serviceCancel(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.cancel()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        # a = json.dumps(response)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))
        # log.info(response)
        return response

    # INQUIRY REQUEST
    @staticmethod
    def serviceInquiry(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.inquiry()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT REGISTRATION REQUEST
    @staticmethod
    def servicePayoutReg(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutRegistration()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT APPROVE REQUEST
    @staticmethod
    def servicePayoutApprove(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutApprove()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT REJECT REQUEST
    @staticmethod
    def servicePayoutReject(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutReject()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT INQUIRY REQUEST
    @staticmethod
    def servicePayoutInquiry(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutInquiry()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT CANCEL REQUEST
    @staticmethod
    def servicePayoutCancel(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutCancel()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT BALANCE INQUIRY REQUEST
    @staticmethod
    def servicePayoutBalanceInquiry(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutBalanceInq()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # PAYOUT TRANSACTION HISTORY INQUIRY REQUEST
    @staticmethod
    def servicePayoutTransHistInq(data):
        headers = DataGenerator.getTransactionHeader()
        endpoint = ConstantsEndpoints.payoutTransHistInq()
        response = apiClient.send(host,
                                  headers,
                                  data,
                                  endpoint)
        log.info("Headers : " + json.dumps(headers))
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # VA FIXED OPEN REGISTRATION REQUEST
    @staticmethod
    def serviceVAFixedOpenRegist(data):
        endpoint = ConstantsEndpoints.vaFixedOpenRegist()
        response = apiClient.sendUrl(host,
                                     data,
                                     endpoint)
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # VA FIXED OPEN CUSTOMER INQUIRY
    @staticmethod
    def serviceVAFixedOpenCustInq(data):
        endpoint = ConstantsEndpoints.vaFixedOpenCustInq()
        response = apiClient.sendUrl(host,
                                     data,
                                     endpoint)
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # VA FIXED OPEN DEPOSIT INQUIRY
    @staticmethod
    def serviceVAFixedOpenDepositInq(data):
        endpoint = ConstantsEndpoints.vaFixedOpenDepositInq()
        response = apiClient.sendUrl(host,
                                     data,
                                     endpoint)
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))

    # VA FIXED OPEN UPDATE
    @staticmethod
    def serviceVAFixedOpenUpdate(data):
        endpoint = ConstantsEndpoints.vaFixedOpenCustUpdate()
        response = apiClient.sendUrl(host,
                                     data,
                                     endpoint)
        log.info("Request Data : " + json.dumps(data))
        log.info("Response Data : " + json.dumps(response))
