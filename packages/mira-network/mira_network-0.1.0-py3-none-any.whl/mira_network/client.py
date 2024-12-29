class MiraNetwork:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def generate(self) -> dict:
        # check if the api key is valid
        if not self.api_key:
            raise ValueError("API key is required")
