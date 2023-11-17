import yaml
import falcon
import os
import logging
from pycon_ml_serving.abstract.generic_resources import GenericFalconResources

def import_handler_from_string(handler_path: str):
    """
    Import handler from a string. Handler refers to a class and
    its method which can be either a function or a coroutine.

    Parameters
    ----------
    handler_path (str):
        handler format <module>.classname.method

    Returns
    -------
    class_ (class type)
    method (str)
    """

    parse = handler_path.split(".")
    module_path = ".".join(parse[:-2])
    classname = parse[-2]
    method = parse[-1]

    module = __import__(module_path, fromlist=["*"])
    return (
        getattr(module, classname),
        method,
    )

def generate_endpoint_groups(apis: list, config: dict):
    """
        Parameters
    ----------
    apis (List[Dict]):
        the serving config apis definition. dict contains:
            method (str): represents the REST API method,
            url (str): represents the REST API url path,
            handler (str): represent the omua handler path

    Returns
    -------
    out (Dict[str, List]):
        the restructured config. list contains tuple:
            method (str): represents the REST API method,
            function (callable): a handler function
            validators (dict): mapping from param to its validator definition

    Example
    -------
    apis:
      - method: POST
        url: /endpoint
        handler: module.ClassName.post_function
      - method: GET
        url: /endpoint
        handler: module.ClassName.get_function

    will translate to

    out:
      /endpoint:
        - (POST, <post_function>)
        - (GET, <get_function>)
    """

    handler = {}
    endpoints = {}

    for api in apis:
        if api["url"] not in endpoints:
            endpoints[api["url"]] = []

        # Handler Function
        class_, function = import_handler_from_string(api["handler"])
        classname = class_.__module__ + "." + class_.__name__

        if classname not in handler:
            handler[classname] = class_(config)

        endpoints[api["url"]].append(
            (
                api["method"].upper(),
                getattr(handler[classname], function)
            )
        )

    return endpoints


def create_falcon_app():
    """
    TO DO

    Parameters
    ----------
    config (Dict)

    Returns
    -------
    out (Dict[str, Resource])
    """
    # setting up logging level
    logging.getLogger().setLevel(logging.INFO)

    # loading application blueprint
    serving_config = {}
    serving_config_file = os.environ.get("CONFIG", "serving.yaml")
    with open(serving_config_file, 'r') as _file:
        serving_config = yaml.safe_load(_file)
    apis = serving_config.get("apis", [])
    
    # generate falcon resources based on application blueprint
    endpoints = generate_endpoint_groups(apis, config=serving_config.get("app_config", {}))
    app = falcon.App()
    for url, definitions in endpoints.items():
        http_function_map = {}
        for method, handler in definitions:
            http_function_map[method] = handler
        
        app.add_route(url, GenericFalconResources(http_function_map))

    return app