#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from skel import Skel
import argparse

class Command(Skel):
    def exec(self):
        print(self.template)
        parser = argparse.ArgumentParser(description='Create dmz security groups')
