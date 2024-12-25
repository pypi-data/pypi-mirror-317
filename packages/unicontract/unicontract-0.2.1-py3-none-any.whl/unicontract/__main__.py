import argparse
import os
import json
from typing import Dict
import importlib.util
from pathlib import Path
from unicontract.Engine import *
from unicontract.linters.SemanticChecker import *

# Adds known arguments to the argument parser
def __add_known_arguments(arg_parser: argparse.ArgumentParser):
    # Input contract file argument, required
    arg_parser.add_argument("-i",
                            "--input",
                            help="input contract file ",
                            required=True,
                            default=[])
    # Linter files argument, multiple files can be specified
    arg_parser.add_argument("-l",
                            "--linter",
                            help="used linter python file(s), if you specify multiple files, all linters will be called",
                            nargs='+',
                            default=[] )
    # Emitter files argument, multiple files can be specified
    arg_parser.add_argument("-e",
                            "--emitter",
                            help="used emitter(s), if you specify multiple emitter, then all emitters will be called. The emmiter can a built-oin emitter (json,dotnet,java) or can a emitter pyton file",
                            nargs='+',
                            default=[] )
    # Output directory argument
    arg_parser.add_argument("-o",
                            "--output-dir",
                            help="output directory",
                            type=str,
                            default="./")
    # Verbose flag for detailed output
    arg_parser.add_argument("-v",
                            "--verbose",
                            help="detailed output",
                            action="store_true")
    # Abort on error flag, execution stops if any error occurs
    arg_parser.add_argument("-aoe",
                            "--abort-on-error",
                            help="when any file has an error, or any of the linters reports an error, then no emitter will be called and execution is aborted. Default value is True",
                            default="True",
                            action="store_true")
    # Abort on warning flag, execution stops if any warning occurs
    arg_parser.add_argument("-aow",
                            "--abort-on-warning",
                            help="when any file has a warning, or any of the linters reports a warning, then no emitter will be called and execution is aborted. Default value is False",
                            default="False",
                            action="store_true")
    # Config file argument, defines the configuration in JSON format
    arg_parser.add_argument("-c",
                            "--config-file",
                            help="define the configuration in json format. If the option is not present, then the default ./configuration.json will be used")

# Reads the configuration file and returns it as a dictionary
def __read_config_file(args, unknown_args) -> Dict[str, str]:
    """Determine the configuration file to use."""
    # Use the provided config file or fallback to the default
    if (args.config_file != None):
        config_file = args.config_file
    else:
        config_file = os.path.join(Path(__file__).parent, "configuration.json")

    # Initialize an empty configuration dictionary
    configuration: Dict[str, str] = {}

    # If the input file exists, load the configuration
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            configuration = json.load(file)

    # Add any unknown arguments to the configuration
    for i in range(0, len(unknown_args), 2):
        if i + 1 < len(unknown_args):
            configuration[unknown_args[i]] = unknown_args[i + 1]

    return configuration

# Parses the input files, creates a session, and returns it
def __parse_input_files(args, configuration: Dict[str, str]) -> Session:
    """Parses the input files and creates a session."""
    engine = Engine(configuration)

    # Check if the input file exists, otherwise exit
    if os.path.exists(args.input) == False:
        exit(f"'{input}' file does not exist")

    # Create a session from the input file
    session = Session(Source.CreateFromFile(args.input))

    # Print info if verbose flag is set
    if (args.verbose):
        print(f"information: '{args.input}' file found, and added to sources")

    # Build the engine with the session
    root = engine.Build(session)

    return session

# Checks for errors in the session and exits if conditions are met
def __check_errors(session: Session, args, action: str):
    """Check for errors in the session and handle abort conditions."""
    # If there are diagnostics (errors or warnings), print them
    if (session.HasDiagnostic() == True):
        session.PrintDiagnostics()

        # Abort if any error occurs and abort-on-error is set
        if (session.HasAnyError() == True and args.abort_on_error):
            exit("abort on error is enabled, process is aborted")

        # Abort if any warning occurs and abort-on-warning is set
        if (session.HasAnyWarning() == True and args.abort_on_warinig):
            exit("abort on warning is enabled, process is aborted")
    else:
        # Print info if verbose flag is set and no errors/warnings found
        if (args.verbose):
            print(f"information: no error found in {action}")

# Calls the linters specified in the arguments
def __call_linters(session: Session, args, configuration: Dict[str, str]):
    """Call the linters for the session."""

    # Call the default semantic checker linter
    if (args.verbose):
        print(f"information: calling 'SemanticChecker")
    defaultChecker = SemanticChecker(session)
    session.main.visit(defaultChecker, None)

    # Execute additional linters specified in the arguments
    for linter_file in args.linter:
        spec = importlib.util.spec_from_file_location(Path(linter_file).stem, linter_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if (args.verbose):
            print(f"information: calling linter:'{linter_file}'")
        module.DoLint(session, configuration)

# Calls the emitters specified in the arguments
def __call_emiters(session: Session, args, configuration: Dict[str, str]):
    """Call the emitters for the session."""

    # Execute each emitter file provided in the arguments
    for emitter_name in args.emitter:
        if (args.verbose):
            print(f"information: calling emitter:'{emitter_name}'")
        
        match emitter_name:
            case "dotnet":
                spec = importlib.util.spec_from_file_location("dotnet", os.path.join(Path(__file__).parent, "emitters/DotnetEmitter.py"))
            case "json":
                spec = importlib.util.spec_from_file_location("dotnet", os.path.join(Path(__file__).parent, "emitters/JsonEmitter.py"))
            case "java":
                spec = importlib.util.spec_from_file_location("dotnet", os.path.join(Path(__file__).parent, "emitters/JavaEmitter.py"))
                pass
            case _:
                spec = importlib.util.spec_from_file_location(Path(emitter_name).stem, emitter_name)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.DoEmit(session, args.output_dir, configuration)

# Main function to run the script
def main():
    """Main function to process input files and call linters and emitters."""
    # Create argument parser and add known arguments
    arg_parser = argparse.ArgumentParser(description="This program processes d3i files and produces results according to the specified emitter.")
    __add_known_arguments(arg_parser)

    # Parse known arguments and unknown arguments
    args, unknown_args = arg_parser.parse_known_args()
    # Check if at least one input file is specified, otherwise print error
    if (len(args.input) == 0):
        print("at least one input must be specified, use -h to see help.")

    # Read configuration file and parse input files
    configuration = __read_config_file(args, unknown_args)
    session: Session = __parse_input_files(args, configuration)
    __check_errors(session, args, "parsing")

    # Run linters on the session
    __call_linters(session, args, configuration)
    __check_errors(session, args, "linting")

    # Run emitters on the session
    __call_emiters(session, args, configuration)
    __check_errors(session, args, "emitting")

# Run the main function if this is the main script
if __name__ == "__main__":
    main()
