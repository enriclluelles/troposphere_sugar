#!/usr/bin/env python2
# -*- coding: utf-8 -*-
class cache(object):
    def __init__(self, func):
        self.original_get = func

    def __get__(self, inst, owner):
        if not hasattr(self, 'cached_result'):
            self.cached_result = self.original_get(owner)
        return self.cached_result

class cfbase(cache):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, inst, owner):
        if not hasattr(self, 'cached_result'):
            self.cached_result = self.fget(inst)
        return self.cached_result

class cfresource(cfbase):
    pass

class cfparam(cfbase):
    pass

class cfoutput(cfbase):
    pass

class cfcondition(cfbase):
    pass
