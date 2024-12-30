"""
This file contains commonly used pydantic models.
"""

from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel

# This is a Generic type that can be used to define a type that is a
# subclass of BaseModel
DataT = TypeVar("DataT", bound=BaseModel)


class FunctionResp(BaseModel, Generic[DataT]):
    """
    TODO
    """

    status: bool
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    response_type: Optional[str] = None
    data: Optional[DataT] = (
        # This DataT type can be defined as ex. FunctionResp[UserModel] or
        # FunctionResp[str]
        None
    )
    status_code: Optional[int] = None

    class Config:
        """
        TODO
        """

        arbitrary_types_allowed = True