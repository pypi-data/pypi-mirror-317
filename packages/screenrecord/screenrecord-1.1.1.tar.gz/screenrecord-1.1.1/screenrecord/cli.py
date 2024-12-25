from screenrecord.srecord import create_parser, mainrun


def cli():
    "Record screen with python"
    parser = create_parser()
    args = parser.parse_args()
    mainrun(args)
