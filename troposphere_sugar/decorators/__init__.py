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

class cflookup(object):
    def __init__(self, stack_name, output_name):
        self.stack_name = stack_name
        self.output_name = output_name

    def __call__(self, f):
        if not isinstance(f, cfparam):
            raise Exception("You can only wrap @cfparam decorated objects with @cflookup")
        self._param = f
        return self

    def __get__(self, inst, owner):
        res = self._param.__get__(inst, inst.__class__)
        return res


class cfresource(cfbase):
    pass

class cfparam(cfbase):
    pass

class cfoutput(cfbase):
    pass

class cfcondition(cfbase):
    pass
