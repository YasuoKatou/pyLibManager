# -*- coding utf-8 -*-

import inspect
from importlib import import_module
from inspect import signature

class XNoMethodError(Exception):
    pass

class XNoClassError(Exception):
    pass

class XNoModuleError(Exception):
    pass

def load_classes(appDef, defPrint=False):
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
    for clazzDef in appDef['clazzDef']:
        mName = clazzDef['module']
        m = import_module(mName)
        #print(m)
        for a in inspect.getmembers(m, inspect.isclass):
            name = a[0]
            if name.startswith('_'):
                continue
            if defPrint:
                print('class name : %s [%s]' % (name, mName, ))
            methods = []
            clazzDef['classes'].append({'name': name, 'methods': methods})
            clazz = getattr(m, name)
            instance = clazz()
            for a in inspect.getmembers(instance, inspect.ismethod):
                name = a[0]
                if name.startswith('_'):
                    continue
                p = signature(a[1]).parameters
                if len(p) <= 1:
                    # 引数は１つ以上
                    if defPrint:
                        print ('\tmethod name : %s' % (name, ))
                    methods.append({
                        'name': name,
                        'method': a[1]
                    })
                    #a[1]('hello')

def _getMethod(appDef, methodDef):
    mn = methodDef['method']
    c = methodDef['fqdn'].rsplit('.', 1)
    for clazzDef in appDef['clazzDef']:
        if clazzDef['module'] == c[0]:
            for clazz in clazzDef['classes']:
                if clazz['name'] == c[1]:
                    for method in clazz['methods']:
                        if method['name'] == mn:
                            return method['method']
                    raise XNoMethodError('[%s] method not found' % (mn, ))
            raise XNoClassError('[%s] class not found' % (c[1], ))
    raise XNoModuleError('[%s] module not found' % (c[0], ))

def _getParam(appDef, methodDef):
    if 'param' not in methodDef:
        return None
    if not methodDef['param']:
        return None
    r = None
    for w in methodDef['param'].split('.'):
        if r:
            r = r[w]
        else:
            r = appDef[w]
    return r

def _makeDto(appDef, path, result):
    r = appDef
    parent = None
    for p in path.split('.'):
        if p not in r:
            r[p] = {}
        parent = r
        r = r[p]
    parent[p] = result

def run_lib_manager(appDef):
    for methodDef in appDef['app']:
        m = _getMethod(appDef, methodDef)
        #print(m)
        p = _getParam(appDef, methodDef)
        #print(p)
        if p:
            r = m(p)
        else:
            r = m()
        if 'result' in methodDef:
            _makeDto(appDef, methodDef['result'], r)

if __name__ == '__main__':
    print('このモジュールから起動しないで下さい ...')

#[EOF]