"""
Application entry point.
"""


from config import initialize_directories

from logger import setup_logger

from gui import SecureFileVaultGUI



def main():

    initialize_directories()


    logger = setup_logger()


    logger.info(
        "Application started"
    )


    application = SecureFileVaultGUI()


    application.run()



if __name__ == "__main__":

    main()
