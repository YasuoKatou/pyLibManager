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

    def isEmpty(self, val):
        return False if val else True

    def isNotEmpty(self, val):
        return not self.isEmpty(val)

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

    assert c.isEmpty(0), '数値[0]が空でないと判定された.'
    assert c.isEmpty(1) == False, '数値[1]が空と判定された.'
    assert c.isEmpty(''), '空文字列[""]が空でないと判定された.'
    assert c.isEmpty('1') == False, '文字列["1"]が空と判定された.'
    assert c.isEmpty(None), 'Noneが空でないと判定された.'

    assert c.isNotEmpty(0) == False, '数値[0]が空と判定された.'
    assert c.isNotEmpty(1), '数値[1]が空でないと判定された.'
    assert c.isNotEmpty('') == False, '空文字列[""]が空と判定された.'
    assert c.isNotEmpty('1'), '文字列["1"]が空でないと判定された.'
    assert c.isNotEmpty(None) == False, 'Noneが空と判定された.'

    print('test is all OK !!')
#[EOF]