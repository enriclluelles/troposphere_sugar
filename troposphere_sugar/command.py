#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from skel import Skel
import argparse
import re

#Shameless copy
#http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
def camelcase_to_dashed(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    return "--{}".format(s2)

class Command(Skel):
    def execute(self):
        self.process()
        self.args_to_params = {}
        parser = argparse.ArgumentParser(description=self.template.description)
        for p in self.cfparams:
            dashed = camelcase_to_dashed(p.title)
            self.args_to_params[dashed]=p.title
            has_default = not bool(p.properties.get("Default", False))
            parser.add_argument(dashed, help=p.properties["Description"],
                    required=has_default)
        parser.parse_args()
        print(self.args_to_params)

