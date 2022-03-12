# -*- coding utf-8 -*-

import inspect
from importlib import import_module
from inspect import signature
import logging
import logging.config

class XNoMethodError(Exception):
    pass

class XNoClassError(Exception):
    pass

class XNoModuleError(Exception):
    pass

_logger = logging.getLogger(__name__)
def setLogConfig(log_conf):
    logging.config.dictConfig(log_conf)
    _logger = logging.getLogger(__name__)

def load_classes(appDef, defPrint=False, newCallback=None):
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
                _logger.info('class name : %s [%s]' % (name, mName, ))
            methods = []
            clazzDef['classes'].append({'name': name, 'methods': methods})
            clazz = getattr(m, name)
            instance = clazz()
            if newCallback:
                newCallback(instance)
            for a in inspect.getmembers(instance, inspect.ismethod):
                name = a[0]
                if name.startswith('_'):
                    continue
                p = signature(a[1]).parameters
                if defPrint:
                    _logger.info('\tmethod name : %s' % (name, ))
                methods.append({
                    'name': name,
                    'method': a[1]
                })

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
    def _getParamItem(item):
        r = None
        for w in item.split('.'):
            if r:
                r = r[w]
            else:
                r = appDef[w]
        return r

    if 'param' not in methodDef:
        return None
    if not methodDef['param']:
        return None
    if type(methodDef['param']) is list:
        r = []
        for item in methodDef['param']:
            r.append(_getParamItem(item))
        return tuple(r)
    else:
        return _getParamItem(methodDef['param'])

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
    for methodDef in appDef['app']['config']:
        m = _getMethod(appDef, methodDef)
        #print(m)
        p = _getParam(appDef, methodDef)
        #print(p)
        if p:
            if type(p) is tuple:
                r = m(*p)
            else:
                r = m(p)
        else:
            r = m()
        if 'result' in methodDef:
            _makeDto(appDef, methodDef['result'], r)

if __name__ == '__main__':
    print('このモジュールから起動しないで下さい ...')

#[EOF]