import json
import os
import sys

CONFIG_FILE_NAME = '.doclirc'

class DocliConfig:
    def __init__(self):
        self.config = self.__load_config()

    def add_service(self, service, image, entrypoint=None, local=False):
        config_path = self.__config_paths()[-1] if local else self.__config_paths()[0]
        config = self.__load_config(config_path)

        if not config.get('services'): config['services'] = {}
        config['services'][service] = { 'image': image }
        if entrypoint: config['services'][service]['entrypoint'] = entrypoint
        new_config = json.dumps(config, sort_keys=True, indent=2) + '\n'

        with open(config_path, 'w') as file:
            file.write(new_config)

        return True

    def exists(self, service):
        return service in self.list_services()

    def get_service(self, service):
        return self.services().get(service, {})

    def get_service_entrypoint(self, service):
        return self.get_service(service).get('entrypoint', '')

    def get_service_image(self, service):
        return self.get_service(service)['image']

    def list_services(self):
        services = self.services().keys()
        services.sort()
        return services

    def remove_service(self, service):
        config_path = self.__config_paths()[0]
        config = self.__load_config(config_path)

        if not config.get('services', {}).get(service):
            return False

        del config['services'][service]
        new_config = json.dumps(config, sort_keys=True, indent=2) + '\n'

        with open(config_path, 'w') as file:
            file.write(new_config)

        return True

    def services(self):
        return self.config.get('services', {})

    def __load_config(self, path=None):
        paths = [path] if path else self.__config_paths()
        config = {}

        for path in paths:
            try:
                config.update(
                    json.load(open(path))
                )
            except (IOError, ValueError):
                pass

        return config

    def __config_paths(self):
        paths = [os.getcwd()] + self.__parent_directories(os.getcwd())
        paths.reverse()
        return [os.path.realpath(path + '/' + CONFIG_FILE_NAME) for path in paths]

    def __parent_directories(self, path):
        if (os.environ['HOME'] == path): return []
        parent = os.path.dirname(path)
        return [parent] + self.__parent_directories(parent)

if __name__ == '__main__':
    config = DocliConfig()
    method = sys.argv[1]
    result = getattr(config, method)(*sys.argv[2:])

    if result is None:
        pass
    elif type(result) == bool:
        if result:
            print(1)
    elif type(result) == list:
        print(' '.join(result))
    else:
        print(result)
