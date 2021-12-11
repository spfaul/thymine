from src.lang import ThymineInterpreter


def main():
    intpr: ThymineInterpreter = ThymineInterpreter()
    intpr.feed_file("tests/test.tym", "tests/test.html", "tests/test.template.html")


if __name__ == '__main__':
    main()