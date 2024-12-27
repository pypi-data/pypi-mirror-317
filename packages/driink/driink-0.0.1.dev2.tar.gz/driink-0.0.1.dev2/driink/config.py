import configparser
import os
import shutil

from terminaltables import SingleTable


def load_user_config():
    """
    Load user config as ConfigParser object. If it doesn't exists it creates a
    blank ini file at $HOME/.config/driink/driink.ini.
    """
    home = os.environ.get("HOME")
    driink_config_path = os.path.join(home, ".config/driink")

    # check if the config folder exists
    if not os.path.exists(driink_config_path):
        os.mkdir(driink_config_path)

    driink_config_file = os.path.join(driink_config_path, "driink.ini")

    # check if the config file exists
    if not os.path.exists(driink_config_file):
        shutil.copyfile("driink.ini", driink_config_file)

    config = configparser.ConfigParser()
    config.read(driink_config_file)
    return config


def set_config_param(name, value):
    # get our current config
    config = load_user_config()

    # check if the value we want to change exists in the ini file
    if name not in config['driink'].keys():
        return False

    # set new value
    config['driink'][name] = value

    # store new values
    home = os.environ.get("HOME")
    driink_config_file = os.path.join(home, ".config/driink/driink.ini")
    with open(driink_config_file, 'w') as config_file_fp:
        config.write(config_file_fp)

    return True


def validate():
    ok = True
    # validate required values from config
    config = load_user_config()

    # daily goal in ML is required, otherwise the tool can't work
    daily_goal = int(config['driink']['daily_goal'])
    if daily_goal <= 0:
        ok = False

    return ok


def present_config():
    # define table header
    table_data = [["Setting name", "Value"]]

    # transform settings in table data
    config = load_user_config()
    for k, v in config['driink'].items():
        table_data.append([k, v])

    table = SingleTable(title="Setting", table_data=table_data)
    print(table.table)
