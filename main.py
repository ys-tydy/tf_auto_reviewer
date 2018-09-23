# coding: UTF-8
import hcl
import yaml
import re
import codecs
import pprint
import glob

pp = pprint.PrettyPrinter(indent=4, width=30, depth=1)
result_global = ""
pass_num_global = 0
alert_num_global = 0


class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


def failed(resource_dict, review_dict, text):
    global result_global, alert_num_global
    alert_num_global += 1
    result_global += pycolor.RED
    result_global += "[ALERT] " + review_dict['title'] + " : " + text + "\n"
    result_global += pp.pformat(resource_dict) + "\n"
    result_global += pycolor.END


def passed(resource_dict, review_dict, text):
    global result_global, pass_num_global
    pass_num_global += 1
    result_global += pycolor.YELLOW
    result_global += "[PASS] " + review_dict['title'] + " : " + text + "\n"
    result_global += pycolor.END


def key_value_check(resource_dict, review_dict):
    if "value" not in review_dict:
        review_dict["value"] = ".*"
    if review_dict["key"] not in resource_dict:
        _text = review_dict["key"] + " not use"
        failed(resource_dict, review_dict, _text)
        return False, _text
    if not re.match(review_dict["value"], str(resource_dict[review_dict["key"]])):
        _text = "value not matched " + review_dict["value"] + " " + str(resource_dict[review_dict["key"]])
        failed(resource_dict, review_dict, _text)
        return False, _text
    passed(resource_dict, review_dict, "passed")
    return True, ""


def review_cycle(resource_dict, review_dict):
    flg, res = key_value_check(resource_dict, review_dict)
    if not flg:
        return False, res
    if review_dict["mode"] == "nested":
        if type(review_dict["nest"]) is list:
            for tmp_review_dict in review_dict["nest"]:
                flg, res = review_cycle(resource_dict[review_dict["key"]], tmp_review_dict)
                return flg, res
        else:
            flg, res = review_cycle(resource_dict[review_dict["key"]], review_dict["nest"])
            return flg, res
    elif review_dict["mode"] == "if":
        if type(review_dict["nest"]) is list:
            for tmp_review_dict in review_dict["nest"]:
                flg, res = review_cycle(resource_dict, tmp_review_dict)
                return flg, res
        else:
            flg, res = review_cycle(resource_dict, review_dict["nest"])
            return flg, res
    return flg, res


if __name__ == '__main__':
    file_path_list = glob.glob("./terraform/**", recursive=True)
    for file_path in file_path_list:
        if not re.match('.*.tf\Z', file_path):
            continue
        print(file_path)
        with codecs.open(file_path, 'r', 'utf-8') as fp:
            obj = hcl.load(fp)
        if not "resource" in obj:
            continue
        obj = obj["resource"]

        with codecs.open('./review_book/s3.yaml', 'r', 'utf-8') as fp2:
            review_book = yaml.load(fp2)

        for resource_name in obj.keys():
            for obj_name in obj[resource_name].keys():
                result_global += "\n==========================================================\n"
                result_global += "RESOURCE " + pycolor.UNDERLINE
                result_global += resource_name.upper() + "." + obj_name.upper() + "\n"
                result_global += pycolor.END
                result_global += "==========================================================\n"
                if not resource_name in review_book:
                    continue
                for review_dict in review_book[resource_name]:
                    flg, res = review_cycle(obj[resource_name][obj_name], review_dict)
    result_global += "\n\n==========================================================\n"
    result_global += "PASS NUM : " + str(pass_num_global) + "\n"
    result_global += "ALERT NUM : " + str(alert_num_global) + "\n"
    result_global += "==========================================================\n"
    print(result_global)
