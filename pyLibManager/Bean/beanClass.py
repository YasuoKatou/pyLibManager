# -*- coding utf-8 -*-

class XNoSupportedBeanMapTypeError(Exception):
    def __init__(self, typeList):
        super().__init__('map type error (%s)' % typeList)

class BeanCopy:

    def copy(self, fromBean, toBean, map):
        if isinstance(map, list):
            self.copyByListMap(fromBean, toBean, map)
        else:
            raise XNoSupportedBeanMapTypeError('dict or list')

    def copyByListMap(self, fromBean, toBean, mapList):
        '''
            map param: [
                {'fromTo': ['from key', 'to key'],
                 'convert': {'type': 'date', 'format': 'yyyy/mm/dd'}
                }
            ]
            copy     : toBean['tk1'] = fromBean['fk1']
        '''
        for map in mapList:
            for k, v in map.items():
                ft = map['fromTo']
                toBean[ft[1]] = None if ft[0] not in fromBean else fromBean[ft[0]]

if __name__ == '__main__':
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

    print('unit test end')

#[EOF]