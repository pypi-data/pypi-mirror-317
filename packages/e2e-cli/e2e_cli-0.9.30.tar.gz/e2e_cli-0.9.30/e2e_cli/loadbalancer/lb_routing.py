import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import show_messages 
from e2e_cli.loadbalancer.lb import LBClass


class LBRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_Errors):
        if self.arguments.args.lb_commands is None:
            show_messages.show_parsing_error(Parsing_Errors)
            subprocess.call(['e2e_cli', 'lb', '-h'])


        elif(self.arguments.args.lb_commands is not None):
            lb_class_object = LBClass(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            operation = lb_class_object.caller(
                    self.arguments.args.lb_commands)
            if operation:
                try:
                    operation()
                except KeyboardInterrupt:
                    print(" ")
                