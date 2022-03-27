# -*- coding utf-8 -*-

class Condition1:
    def isZero(self, value):
        if isinstance(value, int):
            return value == 0
        elif isinstance(value, float):
            return value == 0.0
        elif isinstance(value, str):
            try:
                return float(value.strip()) == 0.0
            except ValueError:
                try:
                    return int(value.strip(), 0) == 0   #2進数、8進数、16進数
                except ValueError:
                    return False
        return False

    def isOne(self, value):
        if isinstance(value, int):
            return value == 1
        elif isinstance(value, float):
            return value == 1.0
        elif isinstance(value, str):
            try:
                return float(value.strip()) == 1.0
            except ValueError:
                try:
                    return int(value.strip(), 0) == 1   #2進数、8進数、16進数
                except ValueError:
                    return False
        return False

if __name__ == '__main__':
    c = Condition1()

    assert c.isZero(0), '整数[0]が正しく判定されていない.'
    assert c.isZero(1) == False, '整数[1]が正しく判定されていない.'
    assert c.isZero(0.0), '実数[0.0]が正しく判定されていない.'
    assert c.isZero(.1) == False, '実数[0.1]が正しく判定されていない.'
    assert c.isZero('0'), '文字["0"]が正しく判定されていない.'
    assert c.isZero('0.00'), '文字["0.00"]が正しく判定されていない.'
    assert c.isZero('0.00e-0'), '文字["0.00e-0"]が正しく判定されていない.'
    assert c.isZero('0x00'), '文字["0x00"]が正しく判定されていない.'

    assert c.isOne(1), '整数[1]が正しく判定されていない.'
    assert c.isOne(0) == False, '整数[0]が正しく判定されていない.'
    assert c.isOne(1.0), '実数[1.0]が正しく判定されていない.'
    assert c.isOne(.1) == False, '実数[0.1]が正しく判定されていない.'
    assert c.isOne('1'), '文字["1"]が正しく判定されていない.'
    assert c.isOne('1.00'), '文字["1.00"]が正しく判定されていない.'
    assert c.isOne('1.00e-0'), '文字["1.00e-0"]が正しく判定されていない.'
    assert c.isOne('0x01'), '文字["0x01"]が正しく判定されていない.'

#[EOF]