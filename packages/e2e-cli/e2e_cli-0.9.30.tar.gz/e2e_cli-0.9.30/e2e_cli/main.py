import argparse
import re
# import argcomplete working on auto-complete now 

from e2e_cli.commands_routing import CommandsRouting
# from e2e_cli.logs.logs_service import save_to_logs
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import constants, show_messages
from e2e_cli.faas.helper_service import regex_type, timeout_range
from e2e_cli.faas.constants import (LANGUAGE_OPTIONS, LANGUAGE_OPTIONS_STR,
                                    MEMORY_CHOICES, VALIDATE_NAME_REGEX, COMPUTE_TYPE_CHOICES)
from e2e_cli.core.alias_service import get_default_value
from e2e_cli.core.constants import LOCATION_OPTION
PARSING_ERROR_MSG=[]

class Main:
    # main class made for sub-commands/actions and formatting their usage
    def __init__(self):
        pass

    def FormatUsage(self, parser, action):
        if(action=="alias"):
            format_string = "e2e_cli" + " alias" + " [-h]" + " {add, add_file, delete, view, set}  "
        else:
            format_string = "e2e_cli" + " --alias"+ " " + action + " [-h] " + action+"-command/--action  inputs... "
        parser.usage = format_string

    # def FormatUsageCommand(self, parser, action, command):
    #     format_string = "e2e_cli" + " alias=" + "<alias_name>"+ " " + action + " [-h] " + command
    #     parser.usage = format_string

    def alias(self, parser):
        alias_sub_parser = parser.add_subparsers(title="Alias Commands", metavar="", dest="alias_commands")
        alias_add_sub_parser = alias_sub_parser.add_parser("add", help="To add api key and auth token")
        alias_file_sub_parser = alias_sub_parser.add_parser("add_file", help="To add api key and auth token via file")
        alias_delete_sub_parser = alias_sub_parser.add_parser("delete", help="To delete api key and auth token")
        alias_view_sub_parser = alias_sub_parser.add_parser("view", help="To view all alias and credentials")
        alias_set_default_sub_parser = alias_sub_parser.add_parser("set", help="To set default alias for system")
        # self.FormatUsageCommand(alias_add_sub_parser, "alias", "add")
        # self.FormatUsageCommand(alias_file_sub_parser, "alias", "add_file")
        # self.FormatUsageCommand(alias_delete_sub_parser, "alias", "delete")
        # self.FormatUsageCommand(alias_view_sub_parser, "alias", "view")
        # self.FormatUsageCommand(alias_set_default_sub_parser, "alias", "set")

    def node(self, parser):
        node_sub_parser = parser.add_subparsers(title="Node Commands", metavar="", dest="node_commands")
        node_action=parser.add_argument('-action', '--action', choices=constants.NODE_ACTIONS, metavar="", help="Actions on node are : "+constants.NODE_ACTIONS_STR)
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node", formatter_class=show_messages.cli_formatter())
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node", formatter_class=show_messages.cli_formatter())
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes", formatter_class=show_messages.cli_formatter())
        node_get_sub_parser = node_sub_parser.add_parser("get", help="To get a list of all nodes", formatter_class=show_messages.cli_formatter())
        # self.FormatUsageCommand(node_action, "node", "actions")
        # self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        # self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        # self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        # self.FormatUsageCommand(node_get_sub_parser, "node", "get")

    def faas(self, parser):
        faas_sub_parser = parser.add_subparsers(title="FaaS Commands", metavar="", dest="faas_commands")
        faas_init = faas_sub_parser.add_parser("init", help="To setup e2e functions on your system", formatter_class=show_messages.cli_formatter())
        faas_init.add_argument('--lang', choices=LANGUAGE_OPTIONS, metavar="", help=f"language options allowed are - {LANGUAGE_OPTIONS_STR}", required=True)
        faas_init.add_argument('--name', metavar="", type=regex_type(VALIDATE_NAME_REGEX), help=f"This is your function name.", required=True)
        faas_init.add_argument('-t', '--timeout', type=timeout_range, metavar="", help="This is timeout for the function. range : [1,600]", default=15)
        faas_init.add_argument('-m', '--memory', choices=MEMORY_CHOICES, type=int, help=f"This is Memory for the function.", default=512)
        faas_init.add_argument('--compute-type', choices=COMPUTE_TYPE_CHOICES, type=str, help=f"Type of the compute hardware to be used.", default='cpu')
        faas_deploy = faas_sub_parser.add_parser("deploy", help="To create the e2e function", formatter_class=show_messages.cli_formatter())
        faas_deploy.add_argument('--name', metavar="", help=f"This is your function name.", required=True)
        faas_redeploy = faas_sub_parser.add_parser("redeploy", help="To update the existing function", formatter_class=show_messages.cli_formatter())
        faas_redeploy.add_argument('--name', metavar="", help=f"This is your function name.", required=True)
        faas_sub_parser.add_parser("list", help="To list all e2e functions", formatter_class=show_messages.cli_formatter())
        faas_destroy = faas_sub_parser.add_parser("destroy", help="To delete the function", formatter_class=show_messages.cli_formatter())
        faas_destroy.add_argument('--name', metavar="", help=f"This is your function name.", required=True)
        
        faas_get = faas_sub_parser.add_parser("get", help="To get the detail of a function", formatter_class=show_messages.cli_formatter())
        faas_get.add_argument('--name', metavar="", help=f"This is your function name", required=True)
        
        faas_invoke = faas_sub_parser.add_parser("invoke", help="To invoke a function", formatter_class=show_messages.cli_formatter())
        faas_invoke.add_argument('--name', metavar="", help=f"This is your function name.", required=True)
        faas_invoke.add_argument('--payload', metavar="", help="JSON payload for the POST API (e.g., '{\"key\": \"value\"}')", default='{}')

    def image(self, parser):
        image_sub_parser = parser.add_subparsers(title="Image Commands", metavar="", dest="image_commands")
        # image_list=parser.add_argument('--list_by', help="attribute/property by which you want to list images")
        image_create_sub_parser = image_sub_parser.add_parser("create", help="To create a new image")
        image_delete_sub_parser = image_sub_parser.add_parser("delete", help="To delete a specific image")
        image_list_sub_parser = image_sub_parser.add_parser("list", help="To get a list of all image")
        image_get_sub_parser = image_sub_parser.add_parser("rename", help="To rename a specific image")
        # self.FormatUsageCommand(image_list, "image", "list_by")
        # self.FormatUsageCommand(image_create_sub_parser, "image", "create")
        # self.FormatUsageCommand(image_delete_sub_parser, "image", "delete")
        # self.FormatUsageCommand(image_list_sub_parser, "image", "list")
        # self.FormatUsageCommand(image_get_sub_parser, "image", "rename")

    def lb(self, parser):
        node_sub_parser = parser.add_subparsers(title="LB Commands", metavar="", dest="lb_commands")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node", formatter_class=show_messages.cli_formatter())
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node", formatter_class=show_messages.cli_formatter())
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes", formatter_class=show_messages.cli_formatter())
        node_edit_sub_parser = node_sub_parser.add_parser("edit", help="To get a list of all nodes", formatter_class=show_messages.cli_formatter())
        # self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        # self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        # self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        # self.FormatUsageCommand(node_edit_sub_parser, "node", "edit")

    def bucket(self, parser):
        bucket_sub_parser = parser.add_subparsers(title="Bucket Commands", metavar="", dest="bucket_commands")
        bucket_action=parser.add_argument('-action', '--action', choices=constants.BUCKET_ACTIONS, metavar="", help="Actions on bucket are : "+constants.BUCKET_ACTIONS_STR)
        bucket_create_sub_parser = bucket_sub_parser.add_parser("create", help="To create a new bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("delete", help="To delete a specific bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("list", help="To get a list of all buckets")
        # self.FormatUsageCommand(bucket_action, "bucket", "actions")
        # self.FormatUsageCommand(bucket_create_sub_parser, "bucket", "create")
        # self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "delete")
        # self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "list")    

    def autoscaling(self, parser):
        autoscaling_sub_parser = parser.add_subparsers(title="Autoscaling Commands", metavar="", dest="autoscaling_commands")
        autoscaling_create_sub_parser = autoscaling_sub_parser.add_parser("create", help="To create a new bucket")
        autoscaling_delete_sub_parser = autoscaling_sub_parser.add_parser("delete", help="To delete a specific bucket")
        autoscaling_delete_sub_parser = autoscaling_sub_parser.add_parser("list", help="To get a list of all buckets")
        # self.FormatUsageCommand(autoscaling_create_sub_parser, "autoscaling", "create")
        # self.FormatUsageCommand(autoscaling_delete_sub_parser, "autoscaling", "delete")
        # self.FormatUsageCommand(autoscaling_delete_sub_parser, "autoscaling", "list")

    def vpc(self, parser):
        vpc_sub_parser = parser.add_subparsers(title="VPC Commands", metavar="", dest="vpc_commands")
        vpc_create_sub_parser = vpc_sub_parser.add_parser("create", help="To create a new bucket")
        vpc_delete_sub_parser = vpc_sub_parser.add_parser("delete", help="To delete a specific bucket")
        vpc_delete_sub_parser = vpc_sub_parser.add_parser("list", help="To get a list of all buckets")
        # self.FormatUsageCommand(vpc_create_sub_parser, "vpc", "create")
        # self.FormatUsageCommand(vpc_delete_sub_parser, "vpc", "delete")
        # self.FormatUsageCommand(vpc_delete_sub_parser, "vpc", "list")

    def cdn(self, parser):
        cdn_sub_parser = parser.add_subparsers(title="CDN Commands", metavar="", dest="cdn_commands")
        cdn_action=parser.add_argument('-action', '--action', choices=constants.CDN_ACTIONS, metavar="", help="Actions on CDN are : "+constants.CDN_ACTIONS_STR)
        cdn_create_sub_parser = cdn_sub_parser.add_parser("create", help="To create a new cdn")
        cdn_delete_sub_parser = cdn_sub_parser.add_parser("delete", help="To delete a specific cdn")
        cdn_delete_sub_parser = cdn_sub_parser.add_parser("list", help="To get a list of all cdn")
        # self.FormatUsageCommand(cdn_action, "cdn", "actions")
        # self.FormatUsageCommand(cdn_create_sub_parser, "cdn", "create")
        # self.FormatUsageCommand(cdn_delete_sub_parser, "cdn", "delete")
        # self.FormatUsageCommand(cdn_delete_sub_parser, "cdn", "list")

    def volumes(self, parser):
        volumes_sub_parser = parser.add_subparsers(title="Volume Commands", metavar="", dest="volumes_commands")
        volumes_action=parser.add_argument('-action', '--action', help="Type of action to be performed your volumes")
        volumes_create_sub_parser = volumes_sub_parser.add_parser("create", help="To create a new volumes")
        volumes_delete_sub_parser = volumes_sub_parser.add_parser("delete", help="To delete a specific volumes")
        volumes_delete_sub_parser = volumes_sub_parser.add_parser("list", help="To get a list of all volumes")
        # self.FormatUsageCommand(volumes_action, "volumes", "actions")
        # self.FormatUsageCommand(volumes_create_sub_parser, "volumes", "create")
        # self.FormatUsageCommand(volumes_delete_sub_parser, "volumes", "delete")
        # self.FormatUsageCommand(volumes_delete_sub_parser, "volumes", "list")
           
    def dbaas(self, parser):
        dbaas_sub_parser = parser.add_subparsers(title="DBaaS Commands", metavar="", dest="dbaas_commands")
        dbaas_action=parser.add_argument('-action', '--action', choices=constants.DBAAS_ACTIONS, metavar="", help="Actions on dbaas are : "+constants.DBAAS_ACTIONS_STR)
        dbaas_create_sub_parser = dbaas_sub_parser.add_parser("create", help="To launch a new dbaas")
        dbaas_delete_sub_parser = dbaas_sub_parser.add_parser("delete", help="To delete a created dbaas")
        dbaas_list_sub_parser = dbaas_sub_parser.add_parser("list", help="To list all of your dbaas")
        # self.FormatUsageCommand(dbaas_action, "dbaas", "actions")
        # self.FormatUsageCommand(dbaas_create_sub_parser, "dbaas", "create")
        # self.FormatUsageCommand(dbaas_list_sub_parser, "dbaas", "list")
        # self.FormatUsageCommand(dbaas_delete_sub_parser, "dbaas", "delete")
    
    def logs(self, parser):
        logs_sub_parser = parser.add_subparsers(title="logs Commands", metavar="", dest="log_commands")
        logs_view_sub_parser = logs_sub_parser.add_parser("view", help="To view a user logs")
        logs_delete_sub_parser = logs_sub_parser.add_parser("clear", help="To delete a user logs")
        # logs_search_sub_parser = logs_sub_parser.add_parser("search", help="To serch your logs")


class Namespace(argparse._AttributeHolder):
    """Simple object for storing attributes.
    copied and over-written/modified here for getting unrecognised commands/inputs
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__


class ArgPaser(argparse.ArgumentParser):
    """Custom argparse for our E2E CLI
    Specifically modified to collect API inputs needed"""

    # used to collect input values
    # input format is like, --key=value or --key="value"
    def inputs_list(self, argv):
        inputs=dict()
        for element in argv:
            if element.startswith('--') and (not element[2]=="="):
                position=element.find("=")
                key=""
                value=""
                if(position != -1):
                    for i in range(2, position):
                        key=f"{key}{element[i]}"
                    for i in range(position+1, len(element)):   
                        value=f"{value}{element[i]}"
                    inputs[key]=value
                else:
                    inputs[element.lstrip('-')]= True
        return inputs    
        
    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = argparse._('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        # here args is used for routing to service and inputs as input to service
        return Namespace(args=args, inputs=self.inputs_list(argv))

    def error(self, message):
        args = {'prog': self.prog, 'message': message}
        if("unrecognized arguments" not in args["message"]):
                        PARSING_ERROR_MSG.append( args["message"])


def commanding(parser):
    sub_parsers = parser.add_subparsers(title="Commands", metavar="", dest="command")
    parser.usage="e2e_cli [-h] [-v] [--info] [--alias ALIAS] [--location LOCATION] [--project_id PROJECT_ID]  Command  ..."
    
    sub_parsers.add_parser("help", help="To view man doc", formatter_class=argparse.RawTextHelpFormatter)
    alias_parser = sub_parsers.add_parser("alias", help="To add delete tokens", formatter_class=argparse.RawTextHelpFormatter)
    node_parser = sub_parsers.add_parser("node", help="To apply crud operations over Nodes", formatter_class=argparse.RawTextHelpFormatter)
    lb_parser = sub_parsers.add_parser("lb", help="To apply operations over Load-Balancer", formatter_class=argparse.RawTextHelpFormatter)
    bucket_parser = sub_parsers.add_parser("bucket", help="To create/delete/list buckets of the user", formatter_class=argparse.RawTextHelpFormatter)
    dbaas_parser = sub_parsers.add_parser("dbaas", help="To perform operations over DBaaS service provided", formatter_class=argparse.RawTextHelpFormatter)
    image_parser = sub_parsers.add_parser("image", help="To perform operations over Image service provided", formatter_class=argparse.RawTextHelpFormatter)
    autoscaling_parser= sub_parsers.add_parser("autoscaling", help="To create/delete/list autoscaling for the user", formatter_class=argparse.RawTextHelpFormatter)
    vpc_parser= sub_parsers.add_parser("vpc", help="To create/delete/list vpc for the user", formatter_class=argparse.RawTextHelpFormatter)
    cdn_parser= sub_parsers.add_parser("cdn", help="To create/delete/list cdn for the user", formatter_class=argparse.RawTextHelpFormatter)
    volumes_parser= sub_parsers.add_parser("volume", help="To create/delete/list volume for the user", formatter_class=argparse.RawTextHelpFormatter)
    logs_parser= sub_parsers.add_parser("logs", help="To videw/delete/search logs for the user", formatter_class=argparse.RawTextHelpFormatter)
    faas_parser = sub_parsers.add_parser("faas", help="To perform operation over e2e functions", formatter_class=argparse.RawTextHelpFormatter)
    security_groups_parser= sub_parsers.add_parser("security_groups", help="To view security_groups for user")
    
    m = Main()
    m.alias(alias_parser)
    m.bucket(bucket_parser)
    m.node(node_parser)
    m.dbaas(dbaas_parser)
    m.lb(lb_parser)
    m.image(image_parser)
    m.autoscaling(autoscaling_parser)
    m.vpc(vpc_parser)
    m.cdn(cdn_parser)
    m.volumes(volumes_parser)
    m.logs(logs_parser)
    m.faas(faas_parser)

    m.FormatUsage(alias_parser, "alias")
    m.FormatUsage(node_parser, "node")
    m.FormatUsage(lb_parser, "lb")
    m.FormatUsage(image_parser, "image")
    m.FormatUsage(bucket_parser, "bucket")
    m.FormatUsage(dbaas_parser, "dbaas")
    m.FormatUsage(autoscaling_parser, "autoscaling")
    m.FormatUsage(vpc_parser, "vpc")
    m.FormatUsage(cdn_parser, "cdn")
    m.FormatUsage(volumes_parser, "volumes")
    m.FormatUsage(logs_parser, "logs")
    m.FormatUsage(faas_parser, "faas")

def project_id_type(value):
    if not re.match(r"^[1-9]\d*$", value):
        raise argparse.ArgumentTypeError("Invalid project_id: Must be a positive integer.")
    return value

def run_main_class():
    default_project_id, default_location = get_default_value("project_id"), get_default_value("location")
    parser = ArgPaser(description="E2E CLI", formatter_class=argparse.RawTextHelpFormatter)

    #version, info, and alias to be taken first else default
    parser.add_argument("-v", "--version", action='store_true', help="To view version Info")
    parser.add_argument( "--info", action='store_true', help="To view package Info")
    parser.add_argument("--alias", default="default", type=str, help="The name of your access credentials")
    parser.add_argument("-location", "--location", default=default_location, choices=LOCATION_OPTION, help="The region where your resource is located.")
    parser.add_argument("--project_id", default=default_project_id, type=project_id_type, help="The project ID you want to access this resource from.")
    # parsing our commands for routing
    # breakpoint()
    commanding(parser)
    args = parser.parse_args()
    commands_route = CommandsRouting(args)
    commands_route.route(PARSING_ERROR_MSG)
