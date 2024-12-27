from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.cdn.cdn_crud import helpers


class CdnCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_cdn,
                        "delete": self.delete_cdn,
                        "list": self.list_cdn
                        }
        return function_set.get(method)


    def create_cdn(self):
        print("Currently not integrated")
        # my_payload= {}
        # cdn_name=input("input name of your new cdn : ")
        # while(Checks.cdn_name_validity(cdn_name)):
        #         cdn_name=input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")

        # API_key=self.API_key
        # Auth_Token=self.Auth_Token
        # url =  "api/v1/storage/cdns/"+ cdn_name +"/?apikey="+API_key+"&location=Delhi"
        # req="POST"
        # status=Request(url, Auth_Token, my_payload, req).response.json()

        # if Checks.status_result(status, req):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at"]
        #         x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
        #         print(x)
        #     except Exception as e:
        #               Checks.show_json(status, e)
        #               return

        # Checks.show_json(status)


    def delete_cdn(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.cdn_delete_helper(self.kwargs["inputs"])
        my_payload = {}
        query = dict()
        query['domain_id'] = self.kwargs["inputs"]["domain_id"]
        url = "api/v1/cdn/distributions/?apikey="+API_key
        req = "DELETE"
        status = Request(url, Auth_Token, my_payload,
                         req, query=query).response.json()

        if Checks.status_result(status, req):
            print("CDN Successfully deleted")
            print(
                "use following command -> e2e_cli <alias> cdn list to check if cdn has been deleted")
        Checks.show_json(status)


    def list_cdn(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        my_payload = {}
        url = "api/v1/cdn/distributions/?apikey=" + API_key
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, req):
        #         print("Your cdns : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "user_domain_name", "Created at", "domain_id"]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['user_domain_name'], element['created_at'], element['domain_id']])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #             print("Errors : ", e)
        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
