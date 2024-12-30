import logging
import time

from src.Utilities import features
from src.Utilities import log

def display_menu():
    """
    Display the CLI menu to the user.
    """
    logger = logging.getLogger(__name__)
    start_time = time.time()
    
    log.logger.info("Welcome To ATAR ! :)")

    print("\n\n\t-----------------------")
    print("\tWelcome to My CLI Menu")
    print("\t-----------------------\n")
    print("\t\t1. Download RoboFlow training dataset")
    print("\t\t2. Train")
    print("\t\t3. Resume existing training")
    print("\t\t4. Validate")
    print("\t\t5. Live Test")
    print("\t\t6. Test on an existing file")
    print("\t\t7. Quit")
    print("\n\t----------------------------------------------------------")
    print("\tTo exit the CLI menu, choose option '7' or press 'Ctrl+C'.")
    print("\t------------------------------------------------------------\n")

    end_time = time.time()
    log.logger.info("Execution time: %.2f seconds", end_time - start_time)
    print("\n\n")


def get_choice():
    """
    Get the user's menu choice.
    """
    return input("\n\t  ======> Enter your choice : ")


def process_choice(choice):
    """
    Process the user's menu choice and execute corresponding actions.
    """
    if choice == '1':
        print("Downloading Dataset ...............................")
        features.get_dataset()
        return True
    elif choice == '2':
        print("\n\t DEFAULT MODELS :")
        features.train()
        return True
    elif choice == '4':
        print("\n\t Trained Model to Validate : ")
        features.valid()
        return True
    elif choice == '5':
        print("Streaming Live Test..............")
        features.stream()
        return True
    elif choice == '6':
        print("Testing on Existing File..............")
        features.video_detect()
        return True
    elif choice == '3':
        print("Resuming Training..............")
        features.resume_train()
        return True
    elif choice == '7':
        log.logger.info("\nThank you for using ATAR! Goodbye! :)")
        return False
    else:
        log.logger.warning("\nInvalid choice. Please select a valid option!")
        return True


def main():
    """
    Main entry point for the ATAR CLI.
    """
    running = True
    while running:
        display_menu()
        choice = get_choice()
        running = process_choice(choice)


if __name__ == "__main__":
    main()
