"""
This module is used to output the hashtray results in JSON format.

Usage:
    python -m hashtray.hashtray_json_output [TARGET_TYPE] [TARGET] [--output OUTPUT_JSON_FILE_PATH]

Options:
    TARGET_TYPE: str
        The type of the target. It can be either 'email' or 'account'.
    TARGET: str
        The target to search for.
    OUTPUT_JSON_FILE_PATH: str
        The path to the JSON file to save the results.
"""
import argparse
import datetime
import json
import pathlib
from re import A

from hashtray.email_enum_for_json_output import EmailEnumForJson
from hashtray.gravatar_for_json_output import GravatarForJson


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Output the hashtray results in JSON format.",
        usage="hashtray-json [TARGET_TYPE] [TARGET] [--output OUTPUT_JSON_FILE_PATH]",
    )
    parser.add_argument(
        "target_type", 
        type=str,
        choices=["email", "account"],
        help="The type of the target. It can be either 'email' or 'account'."
    )
    parser.add_argument(
        "target",
        type=str,
        help="The target to search for."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The path to the JSON file to save the results."
    )
    args = parser.parse_args()
    target_type = args.target_type
    target = args.target
    output = args.output
    
    if target_type == "email":
        gravatar_json = GravatarForJson(email=target).get_json()
    elif target_type == "account":
        gravatar_json = EmailEnumForJson(
            target,
            domain_list="full"
        ).get_json()
    else:
        raise ValueError("Invalid target type. It should be either 'email' or 'account'.")

    if gravatar_json == {}:
        return
    
    # Output the result
    if output:
        with open(output, "w") as f:
            json.dump(gravatar_json, f, indent=4, ensure_ascii=False)
        print(f"{pathlib.Path(output).resolve()}")
    else:
        print(json.dumps(gravatar_json, indent=4, ensure_ascii=False))
        

if __name__ == "__main__":
    main()
