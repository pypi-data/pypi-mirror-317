import ast
from django.core.management.utils import get_random_secret_key


def check_for_secrets(var_name :str) -> bool:
    # check if there a vaeriable that needs to be in the .env file
    secrets = ['password', 'key']
    for value in secrets:
        if var_name != 'AUTH_PASSWORD_VALIDATORS':
            if value in var_name.lower():
                return True
    return False

def secrets(line, name, env) -> None:
    # add secrets to the env file
    if name != 'SECRET_KEY':
        env[name] = line.value.value
    else:
        env[name] = get_random_secret_key()

    line.value = ast.Name(f"os.getenv('{name}')")
    
    return 

def debug(line)-> None:
    # change debug to false
    line.value.value = False
    return 

def allowed_hosts(line) -> None:
    # change allowed hosts to * (all)
    lenght :int = len(line.value.elts)
    if lenght == 0:
        line.value = ast.List([ast.Constant('*')])
    return

def template(line) -> None:
    # adding cached template loader to the template dict
    new_keys :list = []
    new_values :list = []
    for key,value in zip(line.value.elts[0].keys, line.value.elts[0].values):
        if key.value == 'APP_DIRS':
            continue
        else:
            new_keys.append(key)
            new_values.append(value)
    
    line.value.elts[0].values = new_values
    line.value.elts[0].keys = new_keys

    for value in line.value.elts[0].values:
        if type(value) == ast.Dict:
            loader_list = ast.List([ast.Constant('django.template.loaders.filesystem.Loader'), ast.Constant('django.template.loaders.app_directories.Loader')])
            loaders = ast.List([ast.Tuple([ast.Constant('django.template.loaders.cached.Loader'), loader_list])])
            
            value.values = [value.values[0], loaders]
            value.keys = [value.keys[0], ast.Constant('loaders')]
    return 
    
def database(line, env :dict) -> None:
    # checking if a database config contains a password if it is, it is moved to the .env file
    keys :list = []
    new_values :list= []

    for key, value in zip(line.value.keys,line.value.values):
        keys.append(key)
        current_key :list= []
        current_value :list= []
        for _key,_value in zip(value.keys, value.values):
            current_key.append(_key)
            if type(_value) is ast.BinOp:
                current_value.append(_value)
            else:
                if check_for_secrets(_key.value):
                    env[f'{_key.value}'] = _value.value

                    _value = ast.Name(f"os.getenv('{_key.value}')")
                    current_value.append(_value)
                else:
                    current_value.append(_value)
        new_values.append(ast.Dict(current_key, current_value))
    line.value = ast.Dict(keys, new_values)
            
    return

# change settings to meet django production reqiutements
def change_settings(parse, env: dict) -> str:
    for line in parse.body:
        if type(line) == ast.Assign:
            for object in line.targets:
                var_name :str = object.id # type: ignore

                if check_for_secrets(var_name):
                    secrets(line, var_name, env)
                if var_name == 'DEBUG':
                    debug(line)
                if var_name == 'ALLOWED_HOSTS':
                    allowed_hosts(line)
                if var_name == 'TEMPLATES':
                    template(line)
                if var_name == 'DATABASES':
                    database(line, env)

    add_some_required(parse)
    return ast.unparse(parse)

def add_some_required(file):
    # Add extra params needed for deployment to the settings file 
    # import os
    import_os = ast.Import([ast.alias('os')])
    
    # Session
    add_secure_session = ast.Assign(targets=[ast.Name(id='SESSION_COOKIE_SECURE', ctx=ast.Store())],value=ast.Constant(True), lineno=1) # causes error when theres no line number

    add_session_cache = ast.Assign(targets=[ast.Name(id='SESSION_ENGINE', ctx=ast.Store())],value=ast.Constant('django.contrib.sessions.backends.cache'), lineno=1)

    add_session_timout = ast.Assign(targets=[ast.Name(id='SESSION_COOKIE_AGE', ctx=ast.Store())],value=ast.Constant(86400), lineno=1)

    # set csrf cookie to true
    csrf_secure_cookie = ast.Assign(targets=[ast.Name(id='CSRF_COOKIE_SECURE', ctx=ast.Store())],value=ast.Constant(True), lineno=1)
    
    # Static root
    static_root = ast.Assign(targets=[ast.Name(id='STATIC_ROOT', ctx=ast.Store())],value=ast.Name("BASE_DIR / 'static'"), lineno=1)

    
    # Media Root
    media_root = ast.Assign(targets=[ast.Name(id='MEDIA_ROOT', ctx=ast.Store())],value=ast.Name("BASE_DIR / 'media'"), lineno=1)

    # Media Url
    media_url = ast.Assign(targets=[ast.Name(id='MEDIA_URL', ctx=ast.Store())],value=ast.Name('"/media/"'), lineno=1)

    # add logging
    handlers = ast.Dict([ast.Constant('file')], [ast.Dict([ast.Constant('class'), ast.Constant('filename')] , [ast.Constant('logging.FileHandler'),ast.Name("Path.joinpath(BASE_DIR, 'debug.log')")])])



    loggers = ast.Dict([ast.Constant('django')], [ast.Dict([ast.Constant('handlers'), ast.Constant('level'), ast.Constant('propagate')], [ast.List([ast.Constant('file'), ]), ast.Constant('DEBUG'), ast.Constant(True)])])


    keys_logging = [ast.Constant('version'), ast.Constant('disable_existing_loggers'), ast.Constant('handlers'), ast.Constant('loggers'), ast.Constant('loggers')]
    values_logging = [ast.Constant(1), ast.Constant(False), handlers, loggers]


    logging_setup = ast.Dict(keys_logging,values_logging) # type: ignore

    _logging_setup = ast.Assign(targets=[ast.Name(id='LOGGING', ctx=ast.Store())],value=logging_setup, lineno=1)

    # db connection max age
    conn_max_age =  ast.Assign(targets=[ast.Name(id='CONN_MAX_AGE', ctx=ast.Store())],value=ast.Constant(60), lineno=1)

    # add dotenv
    import_dotenv = ast.Import([ast.alias('dotenv\n')])
    
    initalize_loadenv = ast.Name('dotenv.load_dotenv()', ast.Store(), lineno=0)

    # add to the code
    file.body.insert(1,import_os)
    file.body.insert(1, import_dotenv)
    file.body.insert(2,initalize_loadenv)
    
    file.body.insert(-1, csrf_secure_cookie)
    
    file.body.insert(-1,_logging_setup)

    file.body.insert(-1, conn_max_age)
    
    file.body.insert(-1,add_secure_session)
    file.body.insert(-1,add_session_cache)
    file.body.insert(-1,add_session_timout)

    file.body.insert(-2, static_root)
    file.body.insert(-2, media_root)
    file.body.insert(-2, media_url)
    
    