from yta_general_utils.programming.enum import YTAEnum as Enum


class EditionManualTermContext(Enum):
    """
    This is the context we will be able to apply to our
    edition terms to be applied only on those segments
    related to that context.
    """
    ANY = 'any'
    """
    The term will be applied always, in any context.
    """
    @classmethod
    def get_default(cls):
        """
        Returns the item that acts as the one by default.
        """
        return cls.ANY