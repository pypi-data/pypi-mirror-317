import os
from sfn_llm_client.llm_api_client.anthropic_client import AnthropicClient
from sfn_llm_client.llm_api_client.base_llm_api_client import LLMAPIClientConfig
from sfn_blueprint.utils.logging import setup_logger
from sfn_llm_client.llm_api_client.openai_client import OpenAIClient
from snowflake.snowpark import Session
from sfn_llm_client.llm_api_client.cortex_client import CortexClient

def sfn_openai_client(model):
    logger, _ = setup_logger('sfn_openai_client')
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    try:
        openai_client = OpenAIClient(LLMAPIClientConfig(
            api_key=OPENAI_API_KEY,
            default_model=model,
            headers={}
        ))
        return openai_client
    except Exception as e:
        logger.error(f"Error in OpenAI llm_client creation: {e}")
        raise e

def sfn_anthropic_client(model):
    logger, _ = setup_logger('sfn_anthropic_client')
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

    try:
        anthropic_client = AnthropicClient(LLMAPIClientConfig(
            api_key=ANTHROPIC_API_KEY,
            default_model=model,
            headers={}
        ))
        return anthropic_client
    except Exception as e:
        logger.error(f"Error in anthropic llm_client creation: {e}")
        raise e

def sfn_cortex_client(model):
    cortex_client = CortexClient()
    return cortex_client

def get_snowflake_session():
    # Load environment variables
    db_password = os.getenv("SNOWFLAKE_PASSWORD")
    creds = dict()
    creds["account"] = os.getenv("SNOWFLAKE_ACCOUNT")
    creds["warehouse"] = os.getenv("SNOWFLAKE_WAREHOUSE")
    creds["database"] = os.getenv("SNOWFLAKE_DATABASE")
    creds["schema"] = os.getenv("SNOWFLAKE_SCHEMA")
    
    # Check if any required Snowflake credentials are missing
    required_creds = ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_WAREHOUSE", "SNOWFLAKE_DATABASE", "SNOWFLAKE_SCHEMA"]
    missing_creds = [cred for cred in required_creds if not os.getenv(cred)]

    if missing_creds:
        raise ValueError(f"Missing Snowflake credentials: {', '.join(missing_creds)}. Please set them in the environment variables or in .env file.")
    
    if db_password:
        creds["password"] = db_password
        creds["user"] = os.getenv("SNOWFLAKE_USER")
        if not creds["user"]:
            raise ValueError("SNOWFLAKE_USER is missing. Please add the Snowflake user credentials.")
    else:
        creds["host"] = os.getenv("SNOWFLAKE_HOST")
        creds["authenticator"] = "oauth"
        try:
            with open("/snowflake/session/token", "r") as token_file:
                creds["token"] = token_file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("Snowflake OAuth token file not found at /snowflake/session/token. Please ensure the token is available.")
    
    try:
        session = Session.builder.configs(creds).create()
        return session
    except Exception as e:
        raise ConnectionError(f"Failed to create Snowflake session: {e}")
