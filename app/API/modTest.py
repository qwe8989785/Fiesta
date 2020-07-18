import os
import os.path
import sys

from .Mod.authModel import FiestaDbModel
mod  = FiestaDbModel()
def code():
    data = {
        'userId':'yang_eddie',
        'userPassword':'qwertyuiop'
    }
    res = mod.getAccountData(data)
    print(str(res))

def newfunc():
    print("i have create a new function")

if __name__ == "__main__":
    code()
    newfunc()

