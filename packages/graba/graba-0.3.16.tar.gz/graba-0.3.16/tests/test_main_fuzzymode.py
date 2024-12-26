from datetime import datetime
import random

from main import Any

any = Any(mode_datadirty=True)
def test_positiveNumber():

    def createData():
        return {
            "age": any.positiveInt(),
            "name": any.word()
        }


    result = any.listOf(
        min=3,
        max=7,
        factoryFunction=createData
    )
    print(result)
    # [
    #     {'age': 7323, 'name': 'vecalmzbdcvdwuqk'},
    #     {'age': 9705, 'name': 'bdqqpgtpgbfbci'},
    #     {'age': 9656, 'name': 'ojizqxl'}
    # ]

def test_boolean():
    result1 = any.bool()
    result2 = any.bool()
    result3 = any.bool()
    print(result1) # 0
    print(result2) # False
    print(result3) # "true

def test_null():
    result1 = any.null()
    result2 = any.null()
    print(result1) # None
    print(result2) # "null"

def test_word():
    result1 = any.word()
    result2 = any.word()
    print(result1) # "ekm"
    print(result2) # " mpxeotfwfxvfnxcagglpk"

def test_sentence():
    result1 = any.sentence()
    result2 = any.sentence()
    print(result1) # "ekm"
    print(result2) # " mpxeotfwfxvfnxcagglpk"

def test_positiveInt():
    result1 = any.positiveInt()
    result2 = any.positiveInt()
    print(result1) # "ekm"
    print(result2) # " mpxeotfwfxvfnxcagglpk"


def test_subsetOf():
    result = any.subsetOf(min=1, max=4, items=["a", "b", "c", "d", "e", "f"])
    result2 = any.subsetOf(items=["a", "b", "c", "d", "e", "f"])
    print(result) # ['d', 'e', 'b']
    print(result2) # ['d', 'e', 'b']

def test_dateTimeBefore():
    result = any.dateTimeBefore(datetime(2015, 12, 25, 10, 30, 45))
    print(result) # 1994-10-22 10:30:45

    result = any.dateTimeBefore("2022-10-10")
    print(result) # 2000-03-16 00:00:00

    result = any.dateTimeBefore("2022-10-10 23:11:05")
    print(result) # 2016-12-28 23:11:05

def test_datetimebetween():
    result = any.datetimeBetween("2023-10-10", "2027-09-09")
    print(result) # 2025-08-10 22:00:19