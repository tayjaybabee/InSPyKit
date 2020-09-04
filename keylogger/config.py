from configparser import ConfigParser
from os.path import expanduser
from os import makedirs
import subprocess
from pathlib import Path

usr = expanduser("~")
usr_src = Path(usr, '.src')


class Config(ConfigParser):

    def load(self):
        self.parser.read(self.confile_path)

        return self.parser

    def first_write(self):
        file_name = 'keys.txt'
        conf_file_name = 'keys.conf'

        makedirs(usr_src, exist_ok=True)

        key_filepath = Path(usr_src, file_name)
        conf_filepath = Path(usr_src, conf_file_name)

        with open(key_filepath, 'a') as _:
            pass

        subprocess.check_call(["attrib", "+H", key_filepath])

        with open(conf_filepath, 'a'):
            pass

        subprocess.check_call(["attrib", "+H", conf_filepath])

        defaults = {
            'FILES': {
                'key-store': key_filepath,
            },
            'SENDMAIL.PARTIES': {
                'dest': '133754X0R@fakemail.com',
                'from': 'hax0r@fakermail.com'
            },
            'SENDMAIL.SERVER': {
                'host': 'smtp.fakemail.com',
                'port': 587,
            },
            'SENDMAIL.AUTH': {
                'login': 'hax0r@fakemail.com',
                'password': '1234'
            }

        }

        self.parser.read_dict(defaults)
        self.confile_path = conf_filepath

        with open(conf_filepath, 'r+') as config_file:
            self.parser.write(config_file)

    def __init__(self):
        super().__init__()
        self.confile_path = usr_src.joinpath('keys.conf')

        self.parser = ConfigParser()

        if not Path(self.confile_path).exists() or not Path(self.confile_path).is_file():
            self.first_write()
