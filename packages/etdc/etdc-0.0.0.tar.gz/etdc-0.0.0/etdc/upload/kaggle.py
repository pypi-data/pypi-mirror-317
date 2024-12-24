# NOT WORKING
# import base64
# import logging
# import os
# import sys
# from datetime import datetime


# USERNAME = "cGlvdHJwb3Bpcwo="
# DATASET_ID = "piotrpopis/mcpp-eyes"


# def decode(encoded_str: str) -> str:
#     try:
#         decoded_bytes = base64.b64decode(encoded_str)
#         return decoded_bytes.decode("utf-8")
#     except Exception as e:
#         raise ValueError(f"Error decoding Base64 string: {e}")


# def get_msg(base_message: str = "Dataset updated") -> str:
#     user = os.getenv("USER", "Unknown User")
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     return f"{base_message} by {user} on {current_date}"


# def kaggle_push(file: str, key: str = "d528df05c76b8a54cbcf923b3fdd1e6e"):
#     logging.debug("Authenticating with Kaggle")
#     os.environ["KAGGLE_USERNAME"] = decode(USERNAME)
#     os.environ["KAGGLE_KEY"] = ""
#     import requests
#     requests.packages.urllib3.disable_warnings()
#     import kaggle
#     from kaggle.api.kaggle_api_extended import KaggleApi
#     api = KaggleApi()
#     api.authenticate()
#     api.model_list_cli()
#     api._load_config(
#         {
#             "username": os.environ["KAGGLE_USERNAME"],
#             "key": os.environ["KAGGLE_KEY"],
#             "proxy": {"http": "", "https": ""},
#         }
#     )
#     try:
#         # Test Kaggle API
#         api.dataset_status(DATASET_ID)
#         sys.exit(0)
#         logging.debug("Uploading file to Kaggle")

#         api.dataset_create_version(
#             folder=os.path.dirname(file),
#             version_notes=get_msg(),
#             dataset_id=DATASET_ID,
#             dir_mode="zip",
#         )
#         logging.info(f"File '{file}' uploaded successfully to dataset '{DATASET_ID}'.")
#     except Exception as e:
#         logging.error(f"Error uploading file to dataset: {e}")
#         raise
