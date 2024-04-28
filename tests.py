import interpreter


def test_price():
    print(interpreter.instructions["if"].get_price())
    print(interpreter.instructions["price"].get_price())
    print(interpreter.instructions["if"].buy(10))
    print(interpreter.instructions["if"].get_price())
    print(interpreter.instructions["if"].buy(10))
    print(interpreter.instructions["if"].get_price())
    print(interpreter.instructions["if"].buy(10))
    print(interpreter.instructions["if"].get_price())
    print(interpreter.instructions["if"].sell(10))


if __name__ == "__main__":
    test_price()