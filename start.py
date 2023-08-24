from baseapp import BaseApp
import logging

if __name__ == "__main__":
    app = BaseApp()
    app.setLogLevel(logging.DEBUG)
    app.config["routines_directories"] = ["tests/routines/fixtures"]
    app.config["services_directories"] = ["tests/services/fixtures"]
    app.start()