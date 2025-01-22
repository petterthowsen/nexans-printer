import yaml
import os

class ConfigManager:
    def __init__(self, config_path='config.yml'):
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Default config
            self.config = {
                'printer': {
                    'num_copies': 2,
                    'drying_time': 19
                }
            }
            self.save_config()
    
    def save_config(self):
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get_num_copies(self):
        return self.config['printer']['num_copies']
    
    def get_drying_time(self):
        return self.config['printer']['drying_time']
    
    def set_num_copies(self, value):
        if value < 1:
            raise ValueError("Number of copies must be at least 1")
        self.config['printer']['num_copies'] = value
        self.save_config()
    
    def set_drying_time(self, value):
        if value < 1:
            raise ValueError("Drying time must be at least 1 hour")
        self.config['printer']['drying_time'] = value
        self.save_config()
