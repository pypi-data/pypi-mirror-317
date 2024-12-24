import re


def get_dict_value(key, obj):
    raw_key = key[0].strip()
    key.pop(0)
    if len(key) > 0:
        if obj.get(raw_key) is not None:
            return get_dict_value(key, obj.get(raw_key))
    return obj.get(raw_key)

def get_config(reference_value):
    config = {}
    for val in reference_value["command"]:
        config[val["type"]] = val["name"]
    return config

def get_arg_cmd_value(args):
    local_obj = {}

    for val in args:
        word_split = val.split("=")

        local_obj[word_split[0]] = "=".join(word_split[1::])

    return local_obj

def answer_yes(ans):
    list_yes = {"y":"","Y":"","yes":"","Yes":""}
    return ans in list_yes

def check_if_default_name(name):
    valid = False
    if re.search(r'^([\/\.])', name):
        valid = True

    if re.search(r'^([a-zA-z\-\+]{3,}\:\//)', name):
        valid = True

    return valid
