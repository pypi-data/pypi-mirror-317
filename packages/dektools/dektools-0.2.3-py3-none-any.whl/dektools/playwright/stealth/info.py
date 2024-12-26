from playwright_stealth.core._stealth_config import StealthConfig
from playwright_stealth.properties._properties import Properties
from playwright_stealth.stealth import combine_scripts


def stealth_info(config: StealthConfig = None):
    properties = Properties()
    combined_script = combine_scripts(properties, config)
    kwargs = dict(headers=properties.as_dict()["header"])
    return combined_script, kwargs
