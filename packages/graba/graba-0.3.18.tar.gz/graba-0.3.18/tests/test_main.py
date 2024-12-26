from datetime import datetime
import random

from main import Any


any = Any()
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


def test_anyFloat():
    result = any.anyFloat()
    print(result) # -520.9585233638023

def test_anySentence():
    result = any.sentence()
    print(result) # -520.9585233638023

def test_anyWord():
    result = any.word()
    print(result) # lpiqwzwyvcxuxbsaijdgtnvhhluj

def test_subsetOf():
    result = any.subsetOf(min=1, max=4, items=["a", "b", "c", "d", "e", "f"])
    print(result) # ['d', 'e', 'b']

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

def test_ip():
    print(any.ip()) # 250.127.163.208


def test_filepath():
    print(any.filepath()) # d/gfv/mctk/yjgz.pdf

def test_email():
    print(any.email()) # fivjby@fgs.es