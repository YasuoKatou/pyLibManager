# -*- coding utf-8 -*-

from pyLibManager.lib_manager import load_classes

clazzDefInfos = [
    {'module': 'test.sample001', 'classes': []}
]

load_classes(clazzDefInfos)

clazzDefInfos[0]['classes'][0]['methods'][0]['method']('hello')

#[EOF]