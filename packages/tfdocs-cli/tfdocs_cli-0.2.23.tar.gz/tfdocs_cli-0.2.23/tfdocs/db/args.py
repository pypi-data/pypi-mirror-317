from tfdocs.db.init import main


def parse_args(subparsers):
    parser = subparsers.add_parser("init", help="Initialise the documentation database")
    parser.set_defaults(func=main)
