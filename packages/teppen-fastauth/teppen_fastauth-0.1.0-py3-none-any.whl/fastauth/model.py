from pydantic import BaseModel
from typing import Optional


class AccessTokenPayload(BaseModel):
    id: int
    employee_num: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    phs_number: Optional[str]
    email: str
    validated: bool
    initialized: bool
    organization_id: Optional[int]
    organization_name: Optional[str]
    organization_full_name: Optional[str]
    iss: str
    aud: str
    iat: int
    exp: int
