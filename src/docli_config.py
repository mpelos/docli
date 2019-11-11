import json
import os
import sys

class DocliConfig:
    def __init__(self):
        self.config = self.__load_config()

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

    def services(self):
        return self.config.get('services', {})

    def __load_config(self):
        config = {}

        for path in self.__config_paths():
            try:
                config_path = os.path.realpath(path + '/.doclirc')
                config.update(
                    json.load(open(config_path))
                )
            except (IOError, ValueError):
                pass

        return config

    def __config_paths(self):
        paths = [os.getcwd()] + self.__parent_directories(os.getcwd())
        paths.reverse()
        return paths

    def __parent_directories(self, path):
        if (os.environ['HOME'] == path): return []
        parent = os.path.dirname(path)
        return [parent] + self.__parent_directories(parent)

if __name__ == '__main__':
    config = DocliConfig()
    method = sys.argv[1]
    result = getattr(config, method)(*sys.argv[2:])

    if type(result) == None:
        pass
    elif type(result) == bool:
        if result:
            print(0)
        else:
            print(1)
    elif type(result) == list:
        print(' '.join(result))
    else:
        print(result)
