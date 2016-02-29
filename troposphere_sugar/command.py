#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from skel import Skel
from runner import Runner
import argparse
import re

#Shameless copy
#http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
def camelcase_to_dashed(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

class Command(object):
    def execute(self, stack_name, iam_capability=False, session=None):
        self.process()
        params = self.params_args_dict
        self._runner = Runner(self.template, stack_name=stack_name,
                params=params, iam_capability=iam_capability, session=session)
        self._runner.perform()

    @property
    def parser(self):
        if not hasattr(self, "_parser"):
            self._parser = argparse.ArgumentParser(description=self.template.description)
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parsed_args(self):
        self.set_params_args_in_parser()
        return vars(self.parser.parse_args())

    @property
    def params_args_dict(self):
        result = {}
        for (k,v) in self.parsed_args.items():
            altk = re.sub("_","-",k)
            title = self.args_to_params.get(altk, None)
            if title:
                result[title] = v
        return result

    @staticmethod
    def param_to_dict(p):
        default = p.properties.get("Default", None)
        required = not bool(default)
        help=p.properties["Description"]
        return dict(default=p.properties.get("Default", None),
                required=not(bool(default)),
                help=help)

    def set_params_args_in_parser(self):
        if not getattr(self, "args_to_params", None):
            self.args_to_params = {}

        for p in self.cfparams:
            dashed = camelcase_to_dashed(p.title)
            self.args_to_params[dashed]=p.title
            dashed_arg = "--{}".format(dashed)
            self.parser.add_argument(dashed_arg, **self.param_to_dict(p))
