class Cancel:
    def __init__(self,
                 payMethod,
                 tXid,
                 cancelType,
                 cancelMsg,
                 amt):
        self.payMethod = payMethod
        self.tXid = tXid
        self.cancelType = cancelType
        self.cancelMsg = cancelMsg
        self.amt = amt

    def jsonCancel(self):
        return ({
            "payMethod": self.payMethod,
            "tXid": self.tXid,
            "cancelType": self.cancelType,
            "cancelMsg": self.cancelMsg,
            "amt": self.amt
        })

class BuilderCancel:
    def __init__(self):
        self.payMethod = None
        self.tXid = None
        self.cancelType = None
        self.cancelMsg = None
        self.amt = None

    def setPayMethod(self, payMethod):
        self.payMethod = payMethod
        return self

    def setTxid(self, tXid):
        self.tXid = tXid
        return self


    def setCancelType(self, cancelType):
        self.cancelType = cancelType
        return self

    def setCancelMsg(self, cancelMsg):
        self.cancelMsg = cancelMsg
        return self

    def setAmt(self, amt):
        self.amt = amt
        return self


class BuildCancel(BuilderCancel):
    def build(self):
        return Cancel(
            self.payMethod,
            self.tXid,
            self.cancelType,
            self.cancelMsg,
            self.amt
        )
