import __main__
import json
import os

class Singleton_base(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class Config(Singleton_base):
    def __init__(self):
        default_config_dir = os.path.join(os.path.dirname( \
            os.path.dirname(__main__.__file__)), 'config')
        config_dir = os.getenv('BOURSE_CONFIG_DIR', default_config_dir)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self._config_file_path = os.path.join(config_dir, 'config.json')
        self._config = None
        print(f'Config file = {self._config_file_path}')

        # Temporary Directory
        defaulttmppath = os.path.join(os.path.dirname( \
            os.path.dirname(__main__.__file__)), 'tmp')

        self._tmppath = os.getenv('TMPDIR', defaulttmppath)
        if not os.path.exists(self._tmppath):
            os.makedirs(self._tmppath)

        print(f'Temp Dir is: {self._tmppath}')

        self.loadConfig()

    def get_temp_path(self):
        return self._tmppath

    def writeConfig(self):
        if self._config:
            # ecriture de la configuration
            try:
                with open(self._config_file_path, 'w') as fobj:
                    fobj.write(json.dumps(self._config))
                print(f'Ok fichier de conf ecrit dans {self._config_file_path}')
            except:
                print(f'Erreur ecriture fichier de conf dans {self._config_file_path}')
                raise
        else:
            print(f'Pas d ecriture de fichier de conf dans {self._config_file_path}')

    def loadConfig(self):
        try:
            with open(self._config_file_path, 'r') as ofile:
                buf = ofile.read()
                self._config = json.loads(buf)
            print(f'Fichier conf charge de {self._config_file_path}')
        except FileNotFoundError:
            print(f'Pas de Fichier conf charge de {self._config_file_path}')
        if not self._config:
            self._config = {}
        if 'auto_del_isin_csv' not in self._config:
            self._config['auto_del_isin_csv'] = True
