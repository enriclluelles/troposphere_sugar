#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from decorators import *
from troposphere import Template
from random import randint

class Skel(object):
    def __init__(self, *kwargs):
        self.__dict__.update(self._defaults())
        self.__dict__.update(kwargs)

    def _defaults(self):
        return {
                "template": Template(),
                "_processed": False
                }

    def _get_all_decorated(self, ttype):
        return [prop.__get__(self, self.__class__) for prop in self.__class__.__dict__.values() if isinstance(prop, ttype)]

    @property
    def cfparams(self):
        return self._get_all_decorated(cfparam)

    @property
    def cfresources(self):
        return self._get_all_decorated(cfresource)

    @property
    def cfoutputs(self):
        return self._get_all_decorated(cfoutput)

    def process(self):
        if not self._processed:
            self._processed = True
            [self.template.add_parameter(p) for p in self.cfparams]
            [self.template.add_resource(r) for r in self.cfresources]
            [self.template.add_output(o) for o in self.cfoutputs]


    @property
    def output(self):
        self.process()
        return self.template.to_json()
