from __future__ import print_function
import boto3
import sys
import time
import botocore.exceptions

class Runner(object):
    def __init__(self, template, stack_name, params=[], iam_capability=False, session=None):
        self.stack_name = stack_name
        self.iam_capability = iam_capability
        self.params = params
        self.session = session if session else boto3.session.Session()
        self.client = self.session.client('cloudformation')
        self.template_output = template.to_json()

    def find_stack(self):
        stacks = []
        try:
            stacks = self.client.describe_stacks(StackName=self.stack_name)["Stacks"]
        except botocore.exceptions.ClientError:
            pass
        return stacks


    def perform(self):
        stacks = self.find_stack()
        if len(stacks) == 0:
            self.create()
        else:
            self.update()
        self.wait()

    def processed_params(self):
        res = []
        for key, value in self.params.iteritems():
            param_struct = {
                    "ParameterKey": key,
                    "ParameterValue": value,
                    "UsePreviousValue": False
            }
            res.append(param_struct)
        return res

    def capabilities(self):
        if self.iam_capability:
            return ["CAPABILITY_IAM"]
        else:
            return []

    def stack_operation_args(self):
        return {
                "StackName": self.stack_name,
                "TemplateBody": self.template_output,
                "Parameters": self.processed_params(),
                "Capabilities": self.capabilities()
                }


    def create(self):
        print(self.stack_operation_args())
        self.client.create_stack(**self.stack_operation_args())

    def update(self):
        try:
            self.client.update_stack(**self.stack_operation_args())
        except botocore.exceptions.ClientError, e:
            if "No updates are to be performed" not in str(e):
                raise

    def wait(self):
        stack_status = ""
        count = 0
        while stack_status not in ["UPDATE_COMPLETE", "CREATE_COMPLETE"] and count < 10:
            count += 1
            print(".", end="")
            sys.stdout.flush()
            time.sleep(5)
            stacks = self.client.describe_stacks(StackName=self.stack_name)
            stack_status = stacks["Stacks"][0]["StackStatus"]
        if count == 20:
            print("\nError: {0}".format(stack_status))
            return
        print("\nSuccess: {0}".format(stack_status))
