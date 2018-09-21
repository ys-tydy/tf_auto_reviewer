# coding: UTF-8
import hcl
import yaml
import re
import codecs


def key_value_check(resource_dict, review_dict):
    if "value" not in review_dict:
        review_dict["value"] = ".*"
    if review_dict["key"] not in resource_dict:
        return False, review_dict["key"] + " not use"
    if not re.match(review_dict["value"], str(resource_dict[review_dict["key"]])):
        return False, "value not matched " + review_dict["value"] + " " + str(resource_dict[review_dict["key"]])
    return True, "pass"


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
    with codecs.open('./s3.tf', 'r', 'utf-8') as fp:
        obj = hcl.load(fp)["resource"]

    with codecs.open('./review_book/s3.yaml', 'r', 'utf-8') as fp2:
        review_book = yaml.load(fp2)

    for resource_name in obj.keys():
        for obj_name in obj[resource_name].keys():
            for review_dict in review_book[resource_name]:
                flg, res = review_cycle(obj[resource_name][obj_name], review_dict)
                print(res)

