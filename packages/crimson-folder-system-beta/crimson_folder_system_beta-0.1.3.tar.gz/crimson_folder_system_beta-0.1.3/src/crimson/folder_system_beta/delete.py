import os
from typing import List, Dict


def delete_files(file_paths: List[str]):
    results: Dict[str, List] = {"success": [], "failed": {}}

    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                results["success"].append(file_path)
            else:
                results["failed"][file_path] = "File doesn't exist"
        except Exception as e:
            results["failed"][file_path] = str(e)

    return results
