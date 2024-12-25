from api import API

class blackboxai:
    def __init__(
            self
    ):
        self.titel =  """Generate response from www.blackboxai.com"""

    def chat(
            self,
            message: str,
            module: str
        ):

        return API.generate(
            message=message,
            module=module
            )

class CodeConvert:
    def __init__(
            self
        ):

        self.web = """Generate response from www.codeconvert.ai/free-code-generator"""

    def Convert(
                self,
                message: str,
                module : str
        ):
        
        return API.Convert(
                message=message,
                module=module
            )