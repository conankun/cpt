class SubmissionInfo:
    def __init__(self, lang):
        self._lang = lang
        pass

    def setCode(self, code):
        self._code = code

    def getCode(self):
        return self._code

    def getLang(self):
        return self._lang