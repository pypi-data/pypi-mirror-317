from screenrecord import cli


def test_create_parser():
    parser = cli.create_parser()
    assert parser.prog == "record"
    assert parser.description == "Screen Recording with python"


def test_default_args():
    parser = cli.create_parser()
    args = parser.parse_args(["test.gif"])
    assert args.filename == "test.gif"
    assert args.initdelay == 5
    assert args.delay == 0.5
    assert args.duration == 20


def test_bool_args():
    parser = cli.create_parser()
    args1 = parser.parse_args(["test.gif", "-f"])
    assert args1.fullscreen
    args2 = parser.parse_args(["test.gif"])
    assert not args2.fullscreen
