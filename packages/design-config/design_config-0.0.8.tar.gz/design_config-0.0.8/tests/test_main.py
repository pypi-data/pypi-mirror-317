
import os
from design_config import DesignConfig, D, ___
from os.path import join

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

    PROP_FIVE = D(55)

    PROP_SIX = D(True)

    PROP_SEVEN = D(7.7)



def test_base():
    """ Config() == Config(os.environ) """
    config = Config({'PROP_ONE': 'Hi', 
    'PROP_TWO': 'Alex', 'PROP_FIVE': '5', 'PROP_SIX': 'FALSE','PROP_SEVEN': '7e7', })

    assert config.PROP_THREE == "Hello Alex!"

    assert hasattr(config, 'PROP_FOUR') == False

    assert config['PROP_THREE'] == "Hello Alex!"
    assert config['{PROP_THREE}!!'] == "Hello Alex!!!"
    assert config['{PROP_FOUR}'] == "PROP_FOUR"

    assert config['{PROP_ONE} Tom'] == "Hello Tom"
    assert config('PROP_FOUR', 'London') == "London"
    assert config('PROP_TWO', 'London') == "Alex"
    assert config('PROP_SEVEN', '') == 7e7
    assert config('PROP_SEVEN', 0) == 7e7

    assert config.PROP_FIVE == 5
    assert config.PROP_SIX is False
    assert config.PROP_SEVEN == 7e7

    # print(config)

if __name__ == '__main__':
    test_base()