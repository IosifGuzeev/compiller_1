import pytest
from main import main


@pytest.mark.parametrize("input_statement, expected",
                         [
                             ("!(a*b)+b+(a*a)!", "1 2 4 8 3 5 6 4 7 2 4 7 3 4 8 3 5 6 4 6"),
                             ("!a*(a+b)!", "1 3 5 6 4 8 2 4 6 3 4 7")
                         ])
def test_case(input_statement, expected):
    assert main(input_statement) == expected


def test_bad_case():
    input_statement = "!a+!"
    with pytest.raises(Exception):
        raise Exception()