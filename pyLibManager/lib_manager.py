# -*- coding utf-8 -*-

import inspect
import importlib.util
from importlib import import_module
from inspect import signature
import logging
import logging.config
from math import fabs
import os
import pathlib
import sys

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

def _findModule(fqcn):
    '''
        環境変数[LIB_MANAGER_PATH]をベースに指定のfqcnのモジュールをロードする.
        環境変数[LIB_MANAGER_PATH]は、os.pathsep(posix:':', windows:';')で区切り、複数指定可能.
    '''
    ep = os.environ.get('LIB_MANAGER_PATH')
    if ep:
        ep = ep.split(os.pathsep)
        for p in ep:
            if p not in sys.path:
                sys.path.append(p)
    else:
        _logger.info('LIB_MANAGER_PATH not defined ...')
    ep = sys.path
    #_logger.debug('module search path : %s' % (ep))
    rp = '%s.py' % (fqcn.replace('.', '/'), )
    for p in ep:
        fp = pathlib.Path(p) / rp
        _logger.debug('module search path : %s' % (str(fp)))
        if fp.exists():
            _logger.info('load : %s' % (str(fp)))
            spec = importlib.util.spec_from_file_location(fp.stem, str(fp))
            modulevar = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulevar)
            return modulevar
    assert False, '[%s] not found ...' % (fqcn, )

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
        m = _findModule(mName)
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
        p = _getParamItem(methodDef['param'])
        if p == None:
            p = (p, )
        elif isinstance(p, list):
            p = (p, )
        return p

def _makeDto(appDef, path, result):
    r = appDef
    parent = None
    for p in path.split('.'):
        if p not in r:
            r[p] = {}
        parent = r
        r = r[p]
    parent[p] = result

def _execute_method2(appDef, methodDef):
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

    return m, r

def _execute_method(appDef, methodDef):
    m, r = _execute_method2(appDef, methodDef)
    if m.__name__.startswith('is'):
        if r:
            if 'true' in methodDef:
                run_lib_manager(appDef, methodDef['true'])
            else:
                _logger.info('none true action at %s' % (m.__name__, ))
        else:
            if 'false' in methodDef:
                run_lib_manager(appDef, methodDef['false'])
            else:
                _logger.info('none false action at %s' % (m.__name__, ))

def _execute_loop(appDef, methodDef):
    if 'loop-init' in methodDef:
        _execute_method2(appDef, methodDef['loop-init'])

    while True:
        m, r = _execute_method2(appDef, methodDef['loop-next'])
        m, r = _execute_method2(appDef, methodDef['loop-check'])
        if r:
            run_lib_manager(appDef, methodDef['do-loop'])
        else:
            break

def run_lib_manager(appDef, app_config = None):
    appConfig = app_config if app_config else appDef['app']['config']
    for methodDef in appConfig:
        if 'do-loop' in methodDef:
            _execute_loop(appDef, methodDef)
        else:
            _execute_method(appDef, methodDef)

if __name__ == '__main__':
    #_findModule('pyLibManager.DBs.PostgreSQL.pgClass')
    assert False , 'このモジュールから起動しないで下さい ...'

#[EOF]