# -*- coding utf-8 -*-

class Loop1:
    def initListObject(self, list_object):
        for item in list_object:
            yield item

    def next(self, iter):
        if iter:
            return next(iter, None)
        else:
            return None

if __name__ == '__main__':
    c = Loop1()

    ite = c.initListObject([1,2,3,4,5])
    while (obj := c.next(ite)):
        print(obj)

    ite = c.initListObject([])
    assert ite != None, 'test 01, Noneを取得'
    assert c.next(ite) == None, 'test 02, None以外を取得'
#[EOF]