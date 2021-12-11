from src.lang import ThymineInterpreter


def main():
    intpr: ThymineInterpreter = ThymineInterpreter()
    intpr.feed_file("tests/test.tym", "tests/test.html")


if __name__ == '__main__':
    main()