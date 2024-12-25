# desing_config.py

Smart tiny config library for flask-like config

## How to install

    pip install design-config


You can find source code of library on [GitHub](https://github.com/artmihant/design_config)


## How to use

    import os
    from design_config import DesignConfig, D, ___

    class Config(DesignConfig):

        """ is D("") """
        PROP_ZERO = ___
        
        """ is 'hello' """
        PROP_ONE = 'Hello'

        """ 'World' if in init_data_dict not PROP_TWO
        As usually init_data_dict is os.environ """
        PROP_TWO = D('World')

        """ 'Hello World!' or 'hello {PROP_TWO}!' for any PROP_TWO """
        PROP_THREE = '{PROP_ONE} {PROP_TWO}!'


    config = Config()


If your global environment variables contain $PROP_TWO , it will be replaced in the config with the appropriate value. Otherwise, it will remain by default (World)

`D` means *"default"*

    config.PROP_THREE # "Hello World!"

    config['PROP_THREE'] # "Hello World!"
    config['{PROP_THREE}!!'] # "Hello World!!!"
    config['{PROP_FOUR}'] # "PROP_FOUR"

    config('{PROP_ONE} Tom') # "Hello Tom"
    config('PROP_FOUR', 'London') # "London"
    config('PROP_TWO', 'London') # "World"
    config('{PROP_ZERO}', 'London') # ""
    config('{PROP_FOUR}', 'London') # "PROP_FOUR"


Also you can use `int`, `bool`, and `float` values:

    class Config(DesignConfig):

        PROP_FIVE = D(55)

        PROP_SIX = D(True)

        PROP_SEVEN = D(7.7)

    config = Config({
        'PROP_FIVE': '5', 
        'PROP_SIX': 'FALSE',
        'PROP_SEVEN': '7e7'
    })

    config.PROP_FIVE # 5
    config.PROP_SIX # False
    config.PROP_SEVEN # 7e7


You can use DesignConfig with Flask like that:

    class MyFlaskConfig(DesignConfig):

        VERSION = '2'

        FLASK_DEBUG = D(True)
        IS_PRODUCTION = D(False)
        DEBUG = D(True)

        PROJECT_PATH = D('/base')

        REDIS_HOST = D('localhost')
        REDIS_PORT = D('6379')

        """..."""
    
    config = MyFlaskConfig()

    my_flask_app = Flask(__name__, static_folder='static', static_url_path='')
    my_flask_app.config.from_object(config)

    """..."""


