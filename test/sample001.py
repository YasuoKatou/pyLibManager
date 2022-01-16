# -*- coding utf-8 -*-

class _TestBase:
    def __init__(self):
        #print('_TestBase.__init__')
        pass
    def printHelloBase(self, msg1):
        print('start printHelloBase message : %s' % (msg1, ))

class TestClass(_TestBase):
    def __init__(self):
        super().__init__()
        #print('TestClass.__init__')
    def printHello(self, msg2):
        print('start printHello message : %s' % (msg2, ))

if __name__ == '__main__':
    c = TestClass()
    print(c)
#[EOF]