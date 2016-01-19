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
    def execute(self, stack_name, iam_capability=False):
        self.process()
        params = self.parse_args()
        self._runner = Runner(self.template, stack_name=stack_name,
                params=params, iam_capability=iam_capability)
        self._runner.perform()

    def parse_args(self):
        self.args_to_params = {}
        parser = argparse.ArgumentParser(description=self.template.description)
        for p in self.cfparams:
            dashed = camelcase_to_dashed(p.title)
            self.args_to_params[dashed]=p.title
            default = p.properties.get("Default", None)
            required = not bool(default)
            dashed_arg = "--{}".format(dashed)
            parser.add_argument(dashed_arg, help=p.properties["Description"],
                    required=required, default=default)
        args = vars(parser.parse_args())
        return {self.args_to_params[re.sub("_","-",k)]: v for (k,v) in args.items()}
