import json
import os
import sys

CONFIG_FILE_NAME = '.doclirc'

class DocliConfig:
    def __init__(self):
        self.config = self.__load_config()

    def add_service(self, service, image, entrypoint=None, local=False, volumes=[]):
        config_path = self.__config_paths()[-1] if local else self.__config_paths()[0]
        config = self.__load_config(config_path)

        if not config.get('services'): config['services'] = {}
        config['services'][service] = { 'image': image }
        if entrypoint: config['services'][service]['entrypoint'] = entrypoint
        if volumes: config['services'][service]['volumes'] = volumes
        new_config = json.dumps(config, sort_keys=True, indent=2) + '\n'

        with open(config_path, 'w') as file:
            file.write(new_config)

    def exists(self, service):
        return service in self.list_services()

    def get_service(self, service):
        return self.services().get(service, {})

    def get_service_entrypoint(self, service):
        return self.get_service(service).get('entrypoint', '')

    def get_service_image(self, service):
        return self.get_service(service)['image']

    def get_service_ports(self, service):
        return self.get_service(service).get('ports', [])

    def get_service_network(self, service):
        return self.get_service(service)['network']

    def get_service_links(self, service):
        return self.get_service(service).get('links', [])

    def get_service_volumes(self, service):
        return self.get_service(service).get('volumes', [])

    def get_template(self, template_path):
        with open(template_path) as file:
            template = json.load(file)

        return template

    def get_template_entrypoint(self, template_path):
        return self.get_template(template_path).get('entrypoint', '')

    def get_template_image(self, template_path):
        return self.get_template(template_path)['image']

    def get_template_volumes(self, template_path):
        return self.get_template(template_path).get('volumes', [])

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
    def parse_arg(arg):
        if arg == "None":
            return None

        return arg

    config = DocliConfig()
    method = sys.argv[1]
    args = [parse_arg(arg) for arg in sys.argv[2:]]

    if len(sys.argv) > 5: args[3] = args[3] == "1" # Used for #add_service local parameter
    if len(sys.argv) > 6: args[4] = filter(None, args[4].split(',')) # Used for #add_service volumes parameter
    result = getattr(config, method)(*args)

    if result is None:
        pass
    elif type(result) == bool:
        if result: print(1)
    elif type(result) == list:
        print(' '.join(result))
    else:
        print(result)
