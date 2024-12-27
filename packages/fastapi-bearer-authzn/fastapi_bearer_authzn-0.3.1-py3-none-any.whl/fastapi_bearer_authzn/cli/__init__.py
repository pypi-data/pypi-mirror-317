from fastapi_bearer_authzn import bootstrap_config

import argparse
import json

def lib_cli():
    parser = argparse.ArgumentParser(
        description="Bootstrap FastAPI Bearer Authorization configuration",
        prog="uv run fastapi_bearer_authzn bootstrap_config",
        epilog="""
        This script generates a bootstrap configuration for FastAPI Bearer Authorization.
        It creates a specified number of identities with associated tokens and permissions.
        The output can be in JSON format or as a minified JSON environment variable.

        Examples:
          uv run fastapi_bearer_authzn bootstrap_config -n 5 -o json
          uv run fastapi_bearer_authzn bootstrap_config --num-identities 2 --output env
        """
    )
    parser.add_argument("bootstrap_config")
    parser.add_argument("-n", "--num-identities", type=int, default=3, help="Number of identities to generate (default: 3)")
    parser.add_argument("-o", "--output", choices=['json', 'env'], default='json', 
                        help="Output format (default: json). 'env' outputs minified single-line JSON")
    args = parser.parse_args()

    config, tokens = bootstrap_config(args.num_identities)

    if args.output == 'json':
        print(json.dumps({"config": config, "tokens": tokens}, indent=2))
    else:
        config_str = json.dumps(config, separators=(',', ':'))  # Minified JSON
        print(f"FASTAPI_BEARER_AUTHZN_CONFIG='{config_str}'")
        print("\nGenerated tokens:")
        for user_id, token_info in tokens.items():
            print(f"{user_id}: {token_info['token']}")