#!/usr/bin/python3

from r_lambda import shell
from r_lambda import r_env

def call_lambda(func, 
                argv = None, 
                options = None,
                workdir = "./",
                docker = None, 
                run_debug = False):
    """A helper function for run a R# function from the commandline
    
    #### Keyword arguments:
    
    + func -- required, the target R# function name to run, should be in format 
        like: pkg_name::function_name
    + argv -- optional, the function parameters of the target R# function, default none 
        means target function not required of parameters.
    + options -- optional, the R# runtime environment options, this parameter value will
        take effects of the ``getOption`` function in the R# environment.
    + workdir -- optional, the workdir for invoke the target R# function, default work dir
        for the function invocation is at current directory
    + docker -- optional, the docker image argument for this function invoke, default 
        value none means run on locally, not running in a docker container. The value 
        of this parameter should be generated via the ``docker_image`` helper function. 
    + run_debug -- optional, a boolean value for flag the function call running in 
        debug mode or not? set this parameter value to ``True`` means echo more verbose
        information about the function call and skip of the commandline invoke.
    """

    # default has no arguments
    if argv is None: argv = {}
    if options is None: options = {}

    r_env.save_configs(argv, options, workdir)
    r_lambda = None 

    if docker is None:
        r_lambda = shell.local_shell(argv, options, workdir)
    else:
        r_lambda = shell.docker_run(argv, options, docker, workdir)

    return r_lambda.call_lambda(func, run_debug = run_debug)