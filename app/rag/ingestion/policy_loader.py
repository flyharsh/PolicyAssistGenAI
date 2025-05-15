# app/rag/ingestion/policy_loader.py

import os
import json


def load_policy_documents(policy_folder: str) -> list[dict]:
    """
    Loads JSON files from the policy folder.

    Args:
        policy_folder (str): Path to directory containing policy JSON files.

    Returns:
        list[dict]: List of loaded policy dictionaries.
    """
    policies = []  # List to store all loaded policies
    for filename in os.listdir(policy_folder):
        # Only process files ending with .json
        if filename.endswith(".json"):
            with open(os.path.join(policy_folder, filename), "r") as f:
                try:
                    policy = json.load(f)  # Load JSON content
                    if isinstance(policy, list):
                        # If the JSON is a list of policies, extend the main list
                        policies.extend(policy)
                    else:
                        # If the JSON is a single policy, append to the list
                        policies.append(policy)
                except json.JSONDecodeError:
                    # Handle invalid JSON files gracefully
                    print(f"⚠️ Skipping invalid JSON file: {filename}")
    return policies  # Return the list of loaded policies
