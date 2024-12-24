from tfdocs.logging import setup_logs
from tfdocs.cli import parse_args, select_provider
import logging


def main():
    parser, args = parse_args()

    setup_logs(print_log_level=args["verbose"], enable_log_streaming=args["serve_logs"])
    log = logging.getLogger(__name__)
    log.debug(args)

    if "func" in args:
        command = args["command"]
        provider = args["provider"]
        log.info(f"Running command {command}")
        try:
            if command is None and provider is not None:
                provider = select_provider(args["provider"])
                args["func"](provider)
            else:
                args["func"]()
        except Exception as e:
            log.fatal(f"Caught an unhandled error, exiting...: {e}")
            exit(1)


if __name__ == "__main__":
    main()
