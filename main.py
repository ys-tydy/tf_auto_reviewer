# coding: UTF-8
import hcl
import yaml
import re
import codecs


def key_value_check(resource_dict, review_dict):
    if review_dict["key"] not in resource_dict:
        return False, review_dict["key"] + " not use"
    if not re.match(review_dict["value"], str(resource_dict[review_dict["key"]])):
        return False, "value not matched " + review_dict["value"] + " " + str(resource_dict[review_dict["key"]])
    return True, "pass"



if __name__ == '__main__':
    with codecs.open('./s3.tf', 'r', 'utf-8') as fp:
        obj = hcl.load(fp)["resource"]

    with codecs.open('./review_book/s3.yaml', 'r', 'utf-8') as fp2:
        review_book = yaml.load(fp2)

    for resource_name in obj.keys():
        for obj_name in obj[resource_name].keys():
            for review_dict in review_book[resource_name]:
                if "value" not in review_dict:
                    review_dict["value"] = ".*"
                flg, res = key_value_check(obj[resource_name][obj_name], review_dict)
                print(flg)
                print(res)
                if not flg:
                    continue
                if review_dict["mode"] == "nested":
                    for review_dict2 in review_dict["nest"]:
                        if "value" not in review_dict:
                            review_dict["value"] = ".*"
                        flg, res = key_value_check(obj[resource_name][obj_name][review_dict["key"]], review_dict2)
                        print(flg)
                        print(res)
                elif review_dict["mode"] == "if":
                    flg, res = key_value_check(obj[resource_name][obj_name], review_dict2)
                    if not flg:
                        continue
                    for review_dict2 in review_dict["nest"]:
                        if "value" not in review_dict:
                            review_dict["value"] = ".*"
                        flg, res = key_value_check(obj[resource_name][obj_name], review_dict2)
                        print(flg)
                        print(res)

