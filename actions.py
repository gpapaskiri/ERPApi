import requests
import yaml


class ERP:
    def __init__(self):
        with open("config.yaml") as f:
            self.__config = yaml.safe_load(f.read())
            f.close()
        self.__url = self.__config["erp"]["url"]
        self.__key = self.__config["erp"]["key"]

    def check_dict_key_sensitive(self, keys):
        return 'data' if 'data' in keys else 'Data'

    def comment_add(self, params: dict):
        params.update({"key": self.__key, "cat": "task", "action": "comment_add"})
        r = requests.get(self.__url, params=params)
        return r.json()

    def add_task(self, params: dict):
        params.update({"key": self.__key, "cat": "task", "action": "add"})
        r = requests.get(self.__url, params=params)
        return r.json()

    def edit_task(self, params: dict):
        params.update({"key": self.__key, "cat": "task", "action": "edit"})
        r = requests.get(self.__url, params=params)
        return r.json()

    def new_connect(self, params: dict):
        r = requests.get(self.__url, params={"key": self.__key, "cat": "task", "action": "get_list",
                                             "type_id": params["work_typer"],
                                             "state_id": "1,3,4,7,8,9,10,11,13,14,15,16"})
        task_list = r.json()["list"]
        if task_list == "":
            return self.add_task(params)
        else:
            r = requests.get(self.__url, params={"key": self.__key, "cat": "task", "action": "show", "id": task_list})
            data = r.json()[self.check_dict_key_sensitive(r.json().keys())]
            if ',' not in task_list:
                data = {data["id"]: data}
            for key, item in data.items():
                if item["additional_data"].get("43") is None:
                    continue
                if item["customer"]["fullName"] == params["fio"] and item["additional_data"]["1"]["value"] == params[
                    "dopf_1"] and item["additional_data"]["42"]["value"] == params["dopf_42"]:
                    if item["additional_data"]["45"]["value"] == params["dopf_45"]:
                        self.comment_add({"id": key, "comment": f"Абонент обращается повторно"})
                        return {"Result": "OK", "Id": key}
                    else:
                        self.comment_add({"id": key,
                                          "comment": f"Абонент обращается повторно, указав другой тариф {params['dopf_45']}"})
                        return {"Result": "OK", "Id": key}
                elif item["customer"]["fullName"] != params["fio"] and item["additional_data"]["1"]["value"] != params[
                    "dopf_1"]:
                    continue
                else:
                    updates = {}
                    if item["customer"]["fullName"] != params["fio"]:
                        updates.update({"ФИО": params["fio"]})
                    if item["additional_data"]["1"]["value"] != params["dopf_1"]:
                        updates.update({"Номер": params["dopf_1"]})
                    if item["additional_data"]["42"]["value"] != params["dopf_42"]:
                        updates.update({"Адрес": params["dopf_42"]})
                    if item["additional_data"]["45"]["value"] != params["dopf_45"]:
                        updates.update({"Тариф": params["dopf_45"]})
                    comment = f"Абонент обращается повторно, указав другие данные: " + ', '.join(
                        [f'{k.capitalize()} - {v}' for k, v in updates.items()])
                    self.comment_add({"id": key, "comment": comment})
                    return {"Result": "OK", "Id": key}
            return self.add_task(params)

    def new_service(self, params: dict):
        r = requests.get(self.__url, params={"key": self.__key, "cat": "task", "action": "get_list",
                                             "type_id": params["work_typer"],
                                             "state_id": "1,3,4,7,8,9,10,11,13,14,15,16"})
        task_list = r.json()["list"]
        if task_list == "":
            return self.add_task(params)
        else:
            r = requests.get(self.__url, params={"key": self.__key, "cat": "task", "action": "show", "id": task_list})
            data = r.json()[self.check_dict_key_sensitive(r.json().keys())]
            if ',' not in task_list:
                data = {data["id"]: data}
            for key, item in data.items():
                print(f"ITEM is --> {item}")
                if item["additional_data"].get("43") is None:
                    continue
                if item["customer"]["fullName"] == params["fio"] and \
                        item["additional_data"]["1"]["value"] == params["dopf_1"]:
                    self.comment_add({"id": key, "comment": f"Абонент обращается повторно"})
                    return {"Result": "OK", "Id": key}
                elif item["customer"]["fullName"] != params["fio"] and \
                        item["additional_data"]["1"]["value"] != params["dopf_1"]:
                    continue
                else:
                    updates = {}
                    if item["customer"]["fullName"] != params["fio"]:
                        updates.update({"ФИО": params["fio"]})
                    if item["additional_data"]["1"]["value"] != params["dopf_1"]:
                        updates.update({"Номер": params["dopf_1"]})
                    comment = f"Абонент обращается повторно, указав другие данные: " + ', '.join(
                        [f'{k} - {v}' for k, v in updates.items()])
                    self.comment_add({"id": key, "comment": comment})
                    return {"Result": "OK", "Id": key}
            return self.add_task(params)

    def check_task(self, params: dict):
        if params["work_typer"] in [1, 2, 3, 4]:
            return self.new_connect(params)
        else:
            return self.new_service(params)

    @property
    def config(self):
        return self.__url, self.__key
