from giga_auto.request import RequestBase


class ApiBase(RequestBase):
    def __init__(self, **env):
        self.host = env['host']
        _host = self.host
        if env.get('business') and env['business'] == 'b2b':
            self.host_route = env['host_route']
            _host = self.host_route
        super().__init__(_host, env['business'] if 'business' in env else '')
        self.headers = env['headers']



