# -*- coding utf-8 -*-

class XNoSupportedBeanMapTypeError(Exception):
    def __init__(self, typeList):
        super().__init__('map type error (%s)' % typeList)

class XNoSupportedConvertTypeError(Exception):
    def __init__(self, convertType):
        super().__init__('convert type error (%s)' % convertType)

class BeanCopy:

    def copy(self, fromBean, toBean, map):
        if isinstance(map, list):
            self.copyByListMap(fromBean, toBean, map)
        else:
            raise XNoSupportedBeanMapTypeError('dict or list')

    def copyMapValue(self, mapValue, copyRoot, toMapPath):
        '''
            copyRoot[toMapPath] = mapValue
            ex) toMapPath : k1.k2.k3
                copyRoot[k1][k2][k3] = mapValue
        '''
        w = copyRoot
        pd = toMapPath.split('.')
        for index in range(len(pd) - 1):
            p = pd[index]
            if p not in w:
                w[p] = {}
            w = w[p]
        w[pd[-1]] = mapValue

    def copyByListMap(self, fromBean, toBean, mapList):
        '''
            map param: [
                {'fromTo': ['from key', 'to key'],
                 'convert': {'type': 'DateTimeString', 'format': '%Y-%m-%d %H:%M:%S'}
                }
            ]
            copy     : toBean['tk1'] = fromBean['fk1']
        '''
        for map in mapList:
            ft = map['fromTo']
            v = None if ft[0] not in fromBean else fromBean[ft[0]]
            if v and ('convert' in map):
                c = map['convert']
                if c['type'] == 'DateTimeString':
                    v = v.strftime(c['format'])
                elif c['type'] == 'Int2String':
                    v = str(v)
                elif c['type'] == 'String2Int':
                    v = int(v)
                else:
                    raise XNoSupportedConvertTypeError(c['type'])

            toBean[ft[1]] = v

    def beanEdit(self, source, editMap):
        def getValue(s, pf):
            w = s
            pd = pf.split('.')
            for index in range(len(pd) - 1):
                p = pd[index]
                if p in w:
                    w = w[p]
                else:
                    return None
            if pd[-1] in w:
                return w[pd[-1]]
            else:
                return None

        r = {}
        for k, v in editMap.items():
            x = getValue(source, k)
            self.copyMapValue(x, r, v)
        return r

if __name__ == '__main__':
    from datetime import datetime as DT
    print('unit test start')
    tc = BeanCopy()

    tn = 'tesst case 1'
    f = {}
    t = {}
    tc.copy(f, t, [])
    assert len(f) == 0, '[%s] コピー元が空でない' % (tn, )
    assert len(t) == 0, '[%s] コピー先が空でない' % (tn, )

    tn = 'tesst case 2'
    f = {'key1': 'value1'}
    t = {}
    tc.copy(f, t, [{'fromTo':['key1', 'key2']}])
    assert len(f) == 1, '[%s] コピー元が空' % (tn, )
    assert len(t) == 1, '[%s] コピー先が空' % (tn, )
    assert 'key2' in t, '[%s] key2 に key1 の内容がコピーされていない' % (tn, )
    assert t['key2'] == 'value1', '[%s] コピー先の値が不正 (%s)' % (tn, str(t['key2']))

    tn = 'tesst case 3'
    f = {'key1': DT.fromisoformat('2022-01-30 15:34:23'), 'key2': 123, 'key3': '456'}
    t = {}
    copyMap = [{'fromTo':['key1', 'key1'], 'convert': {'type': 'DateTimeString', 'format': '%Y/%m/%d %H:%M:%S'}},
               {'fromTo':['key2', 'key2-1'], 'convert': {'type': 'Int2String'}},
               {'fromTo':['key2', 'key2-2']},
               {'fromTo':['key3', 'key3'], 'convert': {'type': 'String2Int'}}]
    tc.copy(f, t, copyMap)
    assert len(f) == 3, '[%s] コピー元が空' % (tn, )
    assert len(t) == 4, '[%s] コピーがただしくない' % (tn, )
    assert 'key1' in t, '[%s] key1 に key1 の内容がコピーされていない' % (tn, )
    assert t['key1'] == '2022/01/30 15:34:23', '[%s] コピー先の値が不正 (%s)' % (tn, str(t['key1']))
    assert t['key2-1'] == '123', '[%s] コピー先の値が不正 (%s)' % (tn, str(t['key2-1']))
    assert t['key2-2'] == 123, '[%s] コピー先の値が不正 (%s)' % (tn, str(t['key2-2']))
    assert t['key3'] == 456, '[%s] コピー先の値が不正 (%s)' % (tn, str(t['key3']))

    tn = 'tesst case 4'
    p1 = {'k1': 1, 'k2': 'abc'}
    p2 = {}
    tc.copyMapValue(p1, p2, 'test')
    assert p1 == p2['test'], '[%s] コピー失敗.' % (tn, )
    p2 = {}
    tc.copyMapValue(p1, p2, 'path1.path2')
    assert p1 == p2['path1']['path2'], '[%s] コピー失敗.' % (tn, )

    tn = 'tesst case 5'
    p1 = {'k1': 1, 'k2': 'abc', 'k3': {'k3-1': 'aaa', 'k3-2': 'bbb'}}
    r = tc.beanEdit(p1, {'k2': 'r1', 'e1': 'r2', 'k3.k3-1': 'r3.r3-1'})
    assert r['r1'] == p1['k2'], '[%s] コピー1失敗.' % (tn, )
    assert r['r2'] == None, '[%s] コピー2失敗.' % (tn, )
    assert isinstance(r['r3'], dict), '[%s] コピー3失敗.' % (tn, )
    assert r['r3']['r3-1'] == p1['k3']['k3-1'], '[%s] コピー4失敗.' % (tn, )

    print('unit test end')

#[EOF]