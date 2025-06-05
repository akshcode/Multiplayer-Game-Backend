from .rwmodel import RWModel

class TokenData(RWModel):
    username: str = ""

class Token(RWModel):
    access_token: str
    token_type: str