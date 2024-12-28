from dotenv import dotenv_values
from collections import defaultdict
from pydantic import BaseModel

"""
    Load environment variables with a specific prefix, validate them using the given Pydantic schema,
    and return an instance of the schema.

    example .env: 
    # h3ask123sjasl
    h3ask123sjasl_API_KEY=your_api_key_1
    h3ask123sjasl_SOMETHING_ELSE=value_1  
    
    :param env_file: Path to the .env file.
    :param prefix: Prefix for environment variables (e.g., "PRACTICE_1_").
    :param schema: A Pydantic model class to validate the loaded data.
    :return: An instance of the Pydantic model with the loaded data.
    """

def load_prefixed_env(env_file : str, id_as_prefix : str, schema : BaseModel): 
    # loading the env_file 
    env_data = dotenv_values(env_file)
    # updating the prefix 
    prefix = f"{id_as_prefix}_"
    # extracting the values from the key 
    data_filtered_by_id = { 
        key[len(prefix):]: value 
        for key, value in env_data 
        if key.startswith(prefix) }
    # try validating the schema a creating an object based on the Pydantic Model 
    return schema(**data_filtered_by_id )  # "**" unpacks the dictionary into single key, value pairs
    


