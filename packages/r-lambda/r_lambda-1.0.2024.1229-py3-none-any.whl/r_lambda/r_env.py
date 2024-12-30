import json
import os

def save_configs(argv, options, workdir):
    """Save the R# runtime configuration to the workdir

    Keyword arguments:
    workdir -- required, the working directory of the R# function invocation
    argv -- required, the parameter list of the target R# function for invoke
    options -- required, the R# runtime environment configs
    """

    print(
        "*************** setup the R-sharp runtime environment variables *****************"
    )
    print("")
    print("view of your input parameters:")
    print(argv)
    print("config of the R-sharp runtime environment:")
    print(options)

    # Serializing json and setup Rscript envrionment variables
    # at current workspace
    argv_str = json.dumps(argv, indent=2)
    pwd = os.path.abspath(workdir)
    r_env = os.path.join(pwd, ".r_env")

    print("runtime files will be export to location:")
    print(r_env)

    if not os.path.exists(r_env):
        os.makedirs(r_env)

    jsonfile = open("{}/.r_env/run.json".format(pwd), "w")
    jsonfile.write(argv_str)
    jsonfile.close()

    argv_str = json.dumps(options, indent=2)

    jsonfile = open("{}/.r_env/options.json".format(pwd), "w")
    jsonfile.write(argv_str)
    jsonfile.close()

    print("")
    print("*******************  end of runtime environment setup  ***********************")
    print("")

    return argv
