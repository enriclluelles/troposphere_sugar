# -*- coding: utf-8 -*-
import boto3
try:
    from itertools import imap as map, filter
except ImportError:
    pass

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
    cache = {}

    @classmethod
    def get_default_session(cls):
        if not hasattr(cls, '_default_session'):
            cls._default_session = boto3.session.Session()
        return cls._default_session

    def __init__(self, stack_name, output_name, session=None):
        self.stack_name = stack_name
        self.output_name = output_name
        s = None
        if session is None:
            s = self.__class__.get_default_session()
        else:
            s = session
        self.session = s

    def __call__(self, f):
        if not isinstance(f, cfparam):
            raise Exception("You can only wrap @cfparam decorated objects with @cflookup")
        self._param = f
        self.fget = f.fget
        return self

    def __get__(self, inst, owner):
        if not hasattr(self, 'cached_result'):
            res = self._param.__get__(inst, inst.__class__)
            res.Default = self._get_default()
            self.cached_result = res
        return self.cached_result

    def _get_default(self):
        outputs = self.__class__.get_ouputs(self.session, self.stack_name)
        m = map(lambda o: o["OutputValue"], filter(lambda o: o["OutputKey"] == self.output_name, outputs))
        return next(m, '')

    @classmethod
    def get_ouputs(self, session, stack):
        stacks_data = self.cache.get(session, None)
        if stacks_data is None:
            stacks_data = {}
            self.cache[session] = stacks_data
        outputs = stacks_data.get(stack, None)
        if outputs is None:
            client = session.client("cloudformation")
            outputs = client.describe_stacks(StackName=stack)["Stacks"][0]["Outputs"]
            stacks_data[stack] = outputs
        return outputs




class cfresource(cfbase):
    pass

class cfparam(cfbase):
    pass

class cfoutput(cfbase):
    pass

class cfcondition(cfbase):
    pass
