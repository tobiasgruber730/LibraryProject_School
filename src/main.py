import sys
import os
import traceback

# 1. Setup path so we can import modules from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Import the Application Class from our new file 'app.py'
from app import LibraryApp

if __name__ == "__main__":
    """
    Entry point of the program.
    Initializes the main application loop and handles global exceptions
    to prevent the console window from closing immediately in case of error.
    """
    try:
        # Create instance of the app and run it
        app = LibraryApp()
        app.run()

    except Exception:
        # Global Error Handling for EXE stability
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("FATAL ERROR - PROGRAM CRASHED")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        traceback.print_exc()
        print("\n")
        input("Press ENTER to exit...")