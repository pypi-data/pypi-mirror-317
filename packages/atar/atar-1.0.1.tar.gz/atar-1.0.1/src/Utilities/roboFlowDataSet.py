from roboflow import Roboflow
import time
from src.Utilities import log
import os


def roboflow_dataset():
    start_time = time.time()

    # User inputs for API configuration
    rbflw_api_key = input("Enter your API_key: ")
    rbflw_workspace = input("Enter your workspace: ")
    rbflw_project = input("Enter your project: ")
    rbflw_version = input("Enter your version: ")
    rbflw_download = input("Enter your Download: ")

    try:
        # Create necessary directories if they don't exist
        output_dir = "OUTPUT"
        datasets_dir = os.path.join(output_dir, "datasets")

        os.makedirs(datasets_dir, exist_ok=True)

        # Change to datasets directory
        os.chdir(datasets_dir)

        # Log download start
        log.logger.info("\nDOWNLOAD START")
        print("\n")

        # Initialize Roboflow and download dataset
        rf = Roboflow(api_key=rbflw_api_key)
        project = rf.workspace(rbflw_workspace).project(rbflw_project)
        dataset = project.version(rbflw_version).download(rbflw_download)

    except Exception as e:
        # Handle exceptions and log errors
        end_time = time.time()
        log.logger.error(f"\nAn error occurred: {e}\nExecution time: %.2f seconds", end_time - start_time)
    else:
        # Log success if no errors occurred
        end_time = time.time()
        log.logger.info("\nNo errors occurred DONE SUCCESS\nExecution time: %.2f seconds", end_time - start_time)
    finally:
        # Log and reset working directory
        log.logger.warning("\nDatasetDownload EXIT\n")
        os.chdir("../../")
