class BaseEntitie:

    class DoesExists(Exception):
        
        def __init__(self, message: str=None) -> None:
            self.message = message
            

    def get_key(self) -> str:
        raise NotImplemented