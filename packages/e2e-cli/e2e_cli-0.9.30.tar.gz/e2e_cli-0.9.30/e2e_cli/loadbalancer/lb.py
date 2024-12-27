from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.loadbalancer.lb_services import LBServices


class LBClass:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def caller(self, method):
        function_set = {"create": self.create_lb,
                        "delete": self.delete_lb,
                        "list": self.list_lb,
                        "edit": self.edit_lb
                        }
        return function_set.get(method)


    def list_lb(self):
        alias = self.kwargs["alias"]
        lb_services_object = LBServices(alias)
        lb_service_response_object = lb_services_object.all_lb()
        if lb_service_response_object["message"] == "Valid alias":
            lb_api_response_object = lb_service_response_object["lb_api_response"]
            if "code" in lb_api_response_object:
                if lb_api_response_object["code"] == 200:
                    table = PrettyTable(["LB ID", "LB Name", "LB Status"])
                    for LB_instance in lb_api_response_object["data"]:
                        table.add_row([LB_instance["id"], LB_instance["name"],
                                       LB_instance["status"]])

                    print(table)
                    return 1
            else:
                if "No client" in lb_api_response_object["message"]:
                    print("No client found for the API alias")
                return 0

        else:
            print("Please provide a valid Alias")
            return 0


    def create_lb(self):
        alias = self.kwargs["alias"]
        lb_services_object = LBServices(alias)
        lb_service_response_object = lb_services_object.add_lb()
        if lb_service_response_object["message"] == "Valid alias":
            lb_api_response_object = lb_service_response_object["lb_api_response"]
            if "code" in lb_api_response_object:
                if lb_api_response_object["code"] == 200:
                    lb_api_response_object_data = lb_api_response_object["data"]
                    if lb_api_response_object_data["is_credit_sufficient"]:
                        print("  Load Balancer IP: ", lb_api_response_object_data["IP"])
                        print("To check the state of the LB you can run e2e_cli lb list <alias> ")
                    else:
                        print("Do not have sufficient credits!!")

            else:
                if "No client" in lb_api_response_object["message"]:
                    print("No client found for the API alias")

        else:
            print("Please provide a valid Alias")


    def delete_lb(self):
        return_val = self.list_lb()
        if return_val == 0:
            pass
        else:
            alias = self.kwargs["alias"]
            lb_services_object = LBServices(alias)
            lb_delete_response_object = lb_services_object.delete_lb_sevice()
            if lb_delete_response_object["message"] == "Valid alias":
                print("  Your instance have been deleted")
                print(
                    "To check the state of the LB you can run e2e_cli lb list <alias> "
                )
            elif lb_delete_response_object["message"] == "Aborted":
                print(lb_delete_response_object["message"])
            elif lb_delete_response_object["code"] == 404:
                print("" + lb_delete_response_object["message"])     


    def edit_lb(self):
        return_val = self.list_lb()
        if return_val == 0:
            pass
        else:
            alias = self.kwargs["alias"]
            lb_services_object = LBServices(alias)
            lb_edit_response_object = lb_services_object.edit_lb()
            if lb_edit_response_object["message"] == "Valid alias":
                print("  Your instance have been changed")
                print(
                    "To check the state of the LB you can run e2e_cli lb list <alias> "
                )
            elif lb_edit_response_object["code"] == 404:
                print("" + lb_edit_response_object["message"])
            elif lb_edit_response_object["message"] == "Failure":
                print("It appears you have selected wrong options")
            else:
                print("Please provide a valid Alias")
