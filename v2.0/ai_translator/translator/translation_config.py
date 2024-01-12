import yaml

class TranslationConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationConfig, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance
    
    def initialize(self, args):
        # 先读yaml配置，再用命令行参数覆盖
        with open(args.config_file, "r") as f:
            config = yaml.safe_load(f)

        # Use the argparse Namespace to update the configuration
        # 只有config里面本身有的参数才会覆盖，防止输入无效的参数
        overridden_values = {
            key: value for key, value in vars(args).items() if key in config and value is not None
        }
        config.update(overridden_values)    
        
        # Store the original config dictionary
        self._instance._config = config

    # __getattr__ 是 Python 中一个特殊的方法，它在类中定义，用于在访问对象的属性时提供一种动态响应机制。
    # 当你尝试访问一个对象的属性时，如果该属性不存在，Python 将调用该对象的 __getattr__ 方法。
    # 这个方法的作用为:简化self.instance.config[name]为self.name
    def __getattr__(self, name):
        # Try to get attribute from _config
        if self._instance._config and name in self._instance._config:
            return self._instance._config[name]
        raise AttributeError(f"'TranslationConfig' object has no attribute '{name}'")