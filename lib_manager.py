# -*- coding utf-8 -*-

import inspect
from importlib import import_module
from inspect import signature

def load_classes(clazzDefInfos):
    '''
        [
            'module': 'xxxxx'      (I)
            'classes' : [          (I)
                {                  (O)
                    'name': 'yyyyy',      # class name
                    'methods': [
                        {
                            'name': 'zzzz',
                            'method': mmmmm
                        }
                    ]
                }
            ]
        ]
    '''
    for clazzDef in clazzDefInfos:
        m = import_module(clazzDef['module'])
        #print(m)
        for a in inspect.getmembers(m, inspect.isclass):
            name = a[0]
            if name.startswith('_'):
                continue
            #print('class name : %s' % (name, ))
            methods = []
            clazzDef['classes'].append({'name': name, 'methods': methods})
            clazz = getattr(m, name)
            instance = clazz()
            for a in inspect.getmembers(instance, inspect.ismethod):
                name = a[0]
                if name.startswith('_'):
                    continue
                #print ('\tmethod name : %s' % (name, ))
                p = signature(a[1]).parameters
                if len(p) == 1:
                    methods.append({
                        'name': name,
                        'method': a[1]
                    })
                    #a[1]('hello')

if __name__ == '__main__':
    clazzDefInfos = [
        {'module': 'test.sample001', 'classes': []}
    ]
    load_classes(clazzDefInfos)
    for clazzDef in clazzDefInfos:
        print('module : %s' % (clazzDef['module']))
        for clazzez in clazzDef['classes']:
            print('\tclass name : %s' % clazzez['name'])
            for method in clazzez['methods']:
                print('\t\tmethod name : %s' % method['name'])
                #method['method']('hello')
#[EOF]