# -*- coding: utf-8 -*-
from troposphere_sugar.decorators import *
from troposphere import Template
from random import randint

class Skel(object):
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults())
        self.__dict__.update(kwargs)

    def _defaults(self):
        return {
                "template": Template(),
                "_processed": False
                }

    def _get_all_decorated_for_class(self, clazz, *ttypes):
        all = list(clazz.__dict__.values())
        for base_clazz in clazz.__bases__:
            all += self._get_all_decorated_for_class(base_clazz, *ttypes)
        return [prop for prop in all if any(isinstance(prop, ttype) for ttype in ttypes)]

    def _get_all_decorated(self, *ttypes):
        ds = [prop for prop in self._get_all_decorated_for_class(self.__class__, *ttypes)]
        return [[prop.__get__(self, self.__class__), prop.fget.__name__] for prop in ds]

    @property
    def cfparams(self):
        r = self._get_all_decorated(cfparam, cflookup)
        return r

    @property
    def cfresources(self):
        return self._get_all_decorated(cfresource)

    @property
    def cfoutputs(self):
        return self._get_all_decorated(cfoutput)

    @property
    def cfconditions(self):
        return self._get_all_decorated(cfcondition)

    def process(self):
        if not self._processed:
            self._processed = True
            [self.template.add_parameter(p[0]) for p in self.cfparams]
            [self.template.add_resource(r[0]) for r in self.cfresources]
            [self.template.add_output(o[0]) for o in self.cfoutputs]
            [self.template.add_condition(c[1], c[0]) for c in self.cfconditions]

    @property
    def output(self):
        self.process()
        return self.template.to_json()
