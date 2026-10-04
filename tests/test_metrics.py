from resutura.metrics import wilson_interval

def test_interval_bounds():
    lo,hi=wilson_interval(8,10)
    assert 0<=lo<.8<hi<=1
