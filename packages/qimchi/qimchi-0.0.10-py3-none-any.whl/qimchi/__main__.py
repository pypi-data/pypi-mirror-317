import argparse
import logging

# from pathlib import Path # TODOLATER:

# Local imports
from .app import app


if __name__ == "__main__":
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8050)
    parser.add_argument("-d", "--debug", action="store_true")  # False unless specified
    parser.add_argument("-l", "--debug_level", type=int, default=logging.DEBUG)
    # parser.add_argument("-r", "--reset", type=bool, default=False)
    args = parser.parse_args()

    if args.debug:
        # Set env variable for Qimchi's debug level
        import os

        os.environ["QIMCHI_DEBUG_LEVEL"] = str(args.debug_level)

    # if args.reset:
    #     # Reset the state
    #     print("Resetting the state...")
    #     Path("state.json").unlink(missing_ok=True)

    app.run(debug=args.debug, port=args.port)  # , host="0.0.0.0")
