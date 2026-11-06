class InvalidSummaryInputError(Exception):
    pass


class LLMProviderError(Exception):
    def __init__(self, message: str = "Summary generation service unavailable") -> None:
        super().__init__(message)
        self.message = message
