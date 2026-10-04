from resutura.schemas import Predicate
from resutura.state import evaluate_predicate

def test_predicates():
    obs={"a":{"b":3},"x":["z"]}
    assert evaluate_predicate(obs,Predicate("a.b","eq",3))[0]
    assert evaluate_predicate(obs,Predicate("a.b","gte",2))[0]
    assert evaluate_predicate(obs,Predicate("x","contains","z"))[0]
