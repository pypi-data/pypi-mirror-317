from verysimplesamplemodule.substract import substract

def test_subtracts_multiple_numbers():
    assert substract(10, 2, 3) == 5

def test_subtracts_single_number():
    assert substract(5) == 5

def test_subtracts_no_numbers():
    assert substract() == ()

def test_subtracts_negative_numbers():
    assert substract(-10, -5, -5) == 0

def test_subtracts_mixed_numbers():
    assert substract(10, -5, 5) == 10
