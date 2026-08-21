#!/usr/bin/env python3

# Expand all file-based $ref's inline to produce a single YAML file.

import sys
import os
import yaml
import json

# Is this a local file-based $ref?
# File-based refs look like paths, e.g. "../models/user.yaml".
# Non file-based refs look like URL fragments, e.g. "#/models/user"
def is_file_ref(ref, extension):
    return (ref.startswith("/") or ref.startswith("./") or ref.startswith("../")) \
        and ref.endswith(extension)

def open_with_extension(fpath, extension):
    if extension == ".yaml":
        yml_in = open(fpath, "r").read()
        return yaml.safe_load(yml_in)
    elif extension == ".json":
        json_in = open(fpath, "r").read()
        return json.loads(json_in)
    else:
        raise Exception("Unsupported file extension '%s'" % extension)

# Merge two dictionaries.  Throws on key collision.
def merge_or_die(d1, d2):
    for k, v in d2.items():
        if k in d1:
            raise Exception("Refusing to clobber key '%s' with value '%s'" % (k, v))
        d1[k] = v
    return d1

# Recursively descend through the JSON, expanding any file-based refs inline.
def inline_json(js_in, pwd, extension):
    if type(js_in) is dict:
        js_out = {}
        for k, v in js_in.items():
            if k == "$ref" and is_file_ref(v, extension):
                if v.startswith("/"):
                    ref_path = v
                else:
                    # Resolve relative paths
                    ref_path = os.path.normpath(os.path.join(pwd, v))
                v = open_with_extension(ref_path, extension)
                pwd = os.path.split(ref_path)[0]
                js_out = merge_or_die(js_out, inline_json(v, pwd, extension))
            else:
                js_out[k] = inline_json(v, pwd, extension)
        return js_out
    else:
        return js_in

def bundle_definition(js_in, pwd, extension):
    js_out = inline_json(js_in, pwd, extension)
    return js_out

def bundle_json(source_file, target_file):
    if source_file.startswith("/"):
        json_fpath = source_file
    else:
        json_fpath = os.path.join(os.getcwd(), source_file)
    js_in = open_with_extension(json_fpath, ".json")
    pwd = os.path.split(json_fpath)[0]
    js_out = bundle_definition(js_in, pwd, ".json")
    with open(target_file, "w") as f:
        f.write(json.dumps(js_out, indent=2))

def bundle_yaml(source_file, target_file):
    if source_file.startswith("/"):
        yml_fpath = source_file
    else:
        yml_fpath = os.path.join(os.getcwd(), source_file)
    yml_in = open(yml_fpath, "r").read()
    js_in = yaml.safe_load(yml_in)
    pwd = os.path.split(yml_fpath)[0]
    js_out = bundle_definition(js_in, pwd, ".yaml")
    yml_out = yaml.dump(js_out, sort_keys=False)
    with open(target_file, "w") as f:
        f.write(yml_out)

