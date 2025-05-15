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
    policies = []
    for filename in os.listdir(policy_folder):
        if filename.endswith(".json"):
            with open(os.path.join(policy_folder, filename), "r") as f:
                try:
                    policy = json.load(f)
                    if isinstance(policy, list):
                        policies.extend(policy)
                    else:
                        policies.append(policy)
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON file: {filename}")
    return policies