from cast_common.logger import Logger,INFO,DEBUG
from importlib import import_module
from oneclick.config import Config
from argparse import ArgumentParser
from argparse_formatter import FlexiFormatter,ParagraphFormatter

json = [
    {
        "module": "oneclick.discovery.prep",
        "class": "Prepare",
        "catagory": "SourceValidation",
        "log": INFO
    }

]


def get_argparse_defaults(parser):
    defaults = {}
    for action in parser._actions:
        if not action.required and action.dest != "help":
            defaults[action.dest] = action.default
    return defaults

parser = ArgumentParser(prog='OneClick',  formatter_class=lambda prog: FlexiFormatter(prog, width=99999, max_help_position=60))

config=Config(parser,get_argparse_defaults(parser))

for item in json:
    print(item)
    try: 
        module = import_module(item['module'])
        class_name = getattr(module, item['class'])
        catagory = item['catagory']
        log_level = item['log']

        instance = class_name(config,log_level)

    except (ImportError, AttributeError) as ex:
        print(ex)
        pass    

