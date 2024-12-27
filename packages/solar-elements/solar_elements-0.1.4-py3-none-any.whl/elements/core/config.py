import os

# This configuration object implements some very un-pythonic
# wizardry, so let's talk about it.

# I wanted to be able to access config entries as attributes,
# mostly because 'c.host' looks better than 'c.get("host")'

# In making this work for getting and setting, I had to use
# the default getters and setters from python's 'object' class.
# This means that I needed to call object.__setattr__(self', 'config', {})
# instead of saying self.config = {} like usual

class Config:
    def __init__(self):
        object.__setattr__(self, 'config', {})
        object.__setattr__(self, 'overrides', {})
        try:
            with open('...') as f:
                for line in f:
                    line = line.rstrip()
                    index = line.find('=')
                    if index == -1:
                        continue
            
                    self.config[line[:index]] = line[index+1:]
        except FileNotFoundError:
            # Default values
            object.__setattr__(self, 'config', {
                'DATA_FOLDER': 'data/',
                'FILE_EXT': '.json'
            })

    def __getattr__(self, name):
        key = name.upper()

        overrides = object.__getattribute__(self, 'overrides')
        if key in overrides:
            return overrides.get(key)

        config = object.__getattribute__(self, 'config')
        return config.get(key)

    def __setattr__(self, name, value):
        key = name.upper()
        self.config[key] = value

    def override(self, name, value):
        key = name.upper()
        overrides = object.__getattribute__(self, 'overrides')
        overrides[key] = value

    @classmethod
    def load(cls):
        config = globals().get('config')
        if config is None:
            config = Config()
            globals()['config'] = config

        return config
        
