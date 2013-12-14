#!/usr/bin/python3

class Register:
    REGISTER_TYPE_INPUT = 0
    REGISTER_TYPE_HOLD  = 1
    def __init__(self,reg_type,address,count = 1):
        self.reg_type = reg_type
        self.address  = address
        self.count    = count
        
if __name__ == '__main__':
    print(Register.REGISTER_TYPE_HOLD)
    Register.REGISTER_TYPE_INPUT = 5
    print(Register.REGISTER_TYPE_INPUT)
        
        
