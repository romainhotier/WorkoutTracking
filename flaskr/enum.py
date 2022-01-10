""" Define App's Enums """
from enum import Enum


class Msg(Enum):
    """ Used in Response.msg """
    Success = "success"
    BadRequest = "badRequest"
    NotFound = "notFound"
    NotAllowed = 'notAllowed'


class ErrorMsg(Enum):
    """ Used in validator """
    MethodIsNotAllowed = "The method is not allowed for the requested URL."
    IsRequired = "Is Required"
    DoesntExist = "Doesn't exist"
    MustBeAnObjectId = "Must be an ObjectId"
    MustBeAString = "Must be a String"
    MustBeAStringNotEmpty = "Must be a String not empty"
    MustBeAList = "Must be a List"
    MustBeInWorkShopCategory = "Must be in ['cardio', 'fitness', 'strength']"
