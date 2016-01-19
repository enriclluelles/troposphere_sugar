from boto import cloudformation
from boto import exception

class TemplateRunner(object):
    def __init__(self, template, account_name, stack_name):
        self._account_name = account_name
        self._stack_name = stack_name
        self._template_output = template.to_json()
        self._cf = cloudformation.connect_to_region('eu-west-1',profile_name=account_name)

    def perform(self):
        all_stacks = self.find_stack(self._stack_name)
        if len(all_stacks) == 0:
            self.create()
        else:
            self.update()
        self.wait()

    def create(self):
        self._cf.create_stack(self._stack_name, self._template_output)

    def update(self):
        try:
            self._cf.update_stack(self._stack_name, self._template_output)
        except exception.BotoServerError as e:
            if e.message != "No updates are to be performed.":
                print("\nError: {0}".format(e.message))
                raise
            else:
                print("\nSuccess: {0}".format(e.message))

    def wait(self):
        stack_status = ""
        count = 0
        while stack_status not in ["UPDATE_COMPLETE", "CREATE_COMPLETE"] and count < 10:
            count += 1
            print(".", end="")
            time.sleep(5)
            stack_status = self._cf.describe_stacks(stack_name_or_id=self._stack_name)[0].stack_status
        if count == 20:
            print("\nError: {0}".format(stack_status))
            return
        print("\nSuccess: {0}".format(stack_status))

    def find_stack(self, stack_name):
         return [stack for stack in self._cf.describe_stacks() if stack.stack_name == stack_name]
