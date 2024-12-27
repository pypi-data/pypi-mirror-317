import json

from prettytable import PrettyTable
from colorama import Fore, init as init_colorama

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request
from e2e_cli.core.helper_service import Checks
from e2e_cli.node.node_crud.helpers import node_create_helper, node_delete_helper, node_get_helper
from e2e_cli.node.node_crud.node_listing_service import Nodelisting

init_colorama(autoreset=True)

class NodeCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.location = kwargs.get('location', None)
        self.project_id = kwargs.get('project_id', None)
        
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_node,
                        "delete": self.delete_node,
                        "get": self.get_node_by_id,
                        "list": self.list_node
                        }
        return function_set.get(method)

    def create_node(self):
        print("Creating")
        my_payload = node_create_helper(self.kwargs)
        url = f"api/v1/nodes/?apikey={self.API_key}&location={self.location}&project_id={self.project_id}"
        req = "POST"
        if ('auto' in self.kwargs["inputs"]):
            user_agent = 'cli_python'
        else:
            user_agent = 'cli-e2e'
        my_payload = my_payload.__dict__

        status = Request(url, self.Auth_Token, json.dumps(
            my_payload), req, user_agent).response.json()

        # if Checks.status_result(status,req):
        #     try :
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at", "disk", "Status", "Plan"]
        #         x.add_row([status['data']['id'], status['data']['name'],
        #               status['data']['created_at'], status['data']['disk'], status['data']['status'], status['data']['plan']])
        #         print(x)
        #     except Exception as e:
        #             print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
        Checks.status_result(status)
        Checks.show_json(status)


    def delete_node(self):
        my_payload = {}
        node_delete_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        if(node_id<0):
            print(f"{Fore.RED}Error: Invalid Node ID")
            return
        url = f"api/v1/nodes/{str(node_id)}/?apikey={self.API_key}&location={self.location}&project_id={self.project_id}"
        req = "DELETE"

        confirmation = input(
            "are you sure you want to delete press y for yes, else any other key : ")
        if (confirmation.lower() == "y"):
            status = Request(url, self.Auth_Token, my_payload, req).response.json()
            if Checks.status_result(status, req):
                print("Node Successfully deleted")
                print(
                    "use following command -> e2e_cli <alias> node list to check if bucket has been deleted")

            # if('json' in self.kwargs["inputs"]):
            #     Checks.show_json(status)
            Checks.show_json(status)
        else:
            print("deletion cancelled!!")


    def get_node_by_id(self):
        my_payload = {}
        node_get_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        if(node_id<0):
            print(f"{Fore.RED}Error: Invalid Node ID")
            return
        url = f"api/v1/nodes/{str(node_id)}/?apikey={self.API_key}&project_id={self.project_id}&location={self.location}"
        req = "GET"
        status = Request(url, self.Auth_Token, my_payload, req).response.json()

        # if Checks.status_result(status, req):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["VM id", "Name", "Created at", "disk", "Plan", "Public IP", "Status"]
        #         x.add_row([ status['data']['vm_id'], status['data']['name'], status['data']['created_at'], status['data']['disk'],  status['data']['plan'], status['data']['public_ip_address'], status['data']['status'] ])
        #         print(x)
        #     except Exception as e:
        #                 print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
        Checks.status_result(status)
        Checks.show_json(status)


    def list_node(self, parameter=0):
        my_payload = {}
        url = f"api/v1/nodes/?apikey={self.API_key}&location={self.location}&project_id={self.project_id}"
        req = "GET"
        status = Request(url, self.Auth_Token, my_payload, req).response.json()

        if parameter == 0:
            # if Checks.status_result(status, req):
            #     list=status['data']
            #     try:
            #         i = 1
            #         x = PrettyTable()
            #         x.field_names = ["index", "ID", "Name", "Plan", "Status"]
            #         for element in list:
            #             x.add_row([i, element['id'], element['name'],
            #                       element['plan'],  element['status']])
            #             i = i+1
            #         print(x)
            #     except Exception as e:
            #             print("Errors : ", e)

            #     if('json' in self.kwargs["inputs"]):
            #         Checks.show_json(status)
            Checks.status_result(status)
            Checks.show_json(status)

        elif parameter == 1:
            return status['data']


    def update_node(self):
        
        print("update call")
