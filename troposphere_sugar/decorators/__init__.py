# -*- coding: utf-8 -*-
import boto3
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
    @classmethod
    def get_default_session(cls):
        if not hasattr(cls, '_default_session'):
            cls._default_session = boto3.session.Session()
        return cls._default_session

    def __init__(self, stack_name, output_name, session=None):
        self.stack_name = stack_name
        self.output_name = output_name
        self.client = session.client("cloudformation") if session is not None else get_default_session.client("cloudformation")

    def __call__(self, f):
        if not isinstance(f, cfparam):
            raise Exception("You can only wrap @cfparam decorated objects with @cflookup")
        self._param = f
        return self

    def __get__(self, inst, owner):
        if not hasattr(self, 'cached_result'):
            res = self._param.__get__(inst, inst.__class__)
            res.Default = self._obtain_default()
            self.cached_result = res
        return self.cached_result

    def _obtain_default(self):
        stack = self.cf_client.describe_stacks("StackName")["Stacks"][0]
        return stack["Outputs"][self.output_name]



class cfresource(cfbase):
    pass

class cfparam(cfbase):
    pass

class cfoutput(cfbase):
    pass

class cfcondition(cfbase):
    pass
