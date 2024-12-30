"""Definition of custom exceptions."""

class ParsingError(Exception):
    """
    Exception raised of for any reason the LLM response cannot be parsed.
    """
    def __init__(self, message):
        super().__init__(message)
