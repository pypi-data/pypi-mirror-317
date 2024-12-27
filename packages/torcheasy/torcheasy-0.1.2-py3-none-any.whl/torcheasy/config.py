import json
import os


def build_flag(model_name, **kwargs):
    keys = kwargs.keys()
    for key in keys:
        model_name += "_" + key + str(kwargs[key])
    return model_name


class BaseConfig(object):
    """
    This class serves as the foundational class for constructing a *TrainableModule (BaseConfig)*.

    There are 2 formats for utilizing this class:

    1. **Extending the BaseConfig class**:

       You can create a custom configuration class by extending `BaseConfig` as follows:

       >>> class YourConfig(BaseConfig):
       >>>     def __init__(self):
       >>>         super(YourConfig, self).__init__()
       >>>         self.batch_size = 16
       >>>         self.epoch = 100
       >>>         ...
       >>> config = YourConfig()
       >>> model = Model(config)  # Model is a subclass of TrainableModule.

       This method allows you to benefit from IDE code hints, but it requires more lines of code to define a new class.

    2. **Managing hyperparameter dynamics**:

       You can also manage hyperparameters dynamically with:

       >>> config = BaseConfig()
       >>> config.add_param("batch_size", 16)
       >>> config.add_param("epoch", 100)
       >>> model = Model(config)  # Model is a subclass of TrainableModule.

       This method is simpler and faster, but note that hyperparameters may not be managed by the IDE, and as a result,
       you may not receive code hints.
    """
    def __init__(self):
        self.model_flag = build_flag("model")
        self.device = "cuda"

    def add_param(self,
                  param: str,
                  default_value):
        if param.startswith("_") or param.startswith("__"):
            raise ValueError("The param name '{}' which starting with '_' or '__' is not usable for Config objects."
                             "It should be added by '__setattr__(param, default_value)' method.")
        self.__setattr__(param, default_value)

    def del_param(self,
                  param: str):
        self.__delattr__(param)

    def get_params(self):
        return self.__dict__

    def save(self, path):
        """
        This method saves the hyperparameters of the model to the specified path.

        :param path: the absolute path to the saved hyperparameters.
        """
        config_json = json.dumps(self.get_params(), indent=4)
        with open(os.path.join(path, "config.json"), "w") as file:
            file.write(config_json)

    def load(self, path):
        """
        This method loads a **json-format** config file of the model from the specified path.

        :param path: absolute path to the saved json file.
        """
        with open(path, "r") as file:
            config_json = json.load(file)
        for p in config_json.keys():
            self.add_param(p, config_json[p])
        return self

