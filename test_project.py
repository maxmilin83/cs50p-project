from project import price_history,current_price,price_lookup
import pytest


def main():
    test_price_history()

def test_price_history():
    with pytest.raises(KeyError):
        price_history("hello",5)

def test_current_price():
    assert current_price("0") == "Invalid"
    assert current_price("0xxx") == "Invalid"

    



if __name__ == "__main__":
    main()