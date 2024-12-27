import subprocess
import json
import logging

from EVMVerifier.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util

build_script_logger = logging.getLogger("build_script")


def run_script_and_parse_json(context: CertoraContext) -> None:
    if not context.build_script:
        return
    try:
        build_script_logger.info(f"Building from script {context.build_script}")
        run_cmd = [context.build_script, '--json']
        if context.cargo_features is not None:
            run_cmd.append('--cargo_features')
            for feature in context.cargo_features.split(' '):
                run_cmd.append(feature)
        result = subprocess.run(run_cmd, capture_output=True, text=True)

        # Check if the script executed successfully
        if result.returncode != 0:
            raise Util.CertoraUserInputError(f"Error running the script {context.build_script}\n{result.stderr}")

        json_obj = json.loads(result.stdout)

        if not json_obj:
            raise Util.CertoraUserInputError(f"No JSON output from build script {context.build_script}")

        if missing_keys := [key for key in ["success", "project_directory", "sources", "executables"] if key not in json_obj]:
            raise Util.CertoraUserInputError(f"Missing required keys in build script response: {', '.join(missing_keys)}")

        if not json_obj.get("success"):
            raise Util.CertoraUserInputError(
                f"Compilation failed using build script: {context.build_script}\n"
                f"Success value in JSON response is False."
            )

        context.rust_project_directory = json_obj.get("project_directory")
        context.rust_sources = json_obj.get("sources")
        context.rust_executables = json_obj.get("executables")

        if context.test == str(Util.TestValue.AFTER_BUILD_RUST):
            raise Util.TestResultsReady(None)

    except Util.TestResultsReady as e:
        raise e
    except FileNotFoundError as e:
        raise Util.CertoraUserInputError(f"File not found: {e}")
    except json.JSONDecodeError as e:
        raise Util.CertoraUserInputError(f"Error decoding JSON: {e}")
    except Exception as e:
        raise Util.CertoraUserInputError(f"An unexpected error occurred: {e}")
