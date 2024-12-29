# config.py
from prefref import Config, Config_Option, Config_Options

class MyOptions(Config_Options):
    rss_json: Config_Option = Config_Option('rss_json', arg_short_key='f')

config = Config(MyOptions(), 'RSS Feed Generator', 'Generate an rss feed from a json file.')
args: MyOptions = config.options



# __main__:
# from src.config import config, args
# print(args.rss_json)
