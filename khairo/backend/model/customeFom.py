import inspect
from typing import Type
from fastapi import Depends
from khairo.model.userModel.accountMixin import AccountManager
from fastapi import Form
from pydantic import BaseModel, EmailStr, Field


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls

# def is_admin(user:dict = Depends(AccountManager.authenticate_user)):
#    def validate(user):
#      if user["admin"]:
#        return  user
#      return {"error":"error validating user"}