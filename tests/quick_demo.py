from agents.debate import DebateSystem

def test_basic_mul():
    ds = DebateSystem()
    prob = 'Compute 12 * 9.'
    trace = ds.run_debate(prob)
    print(trace)
    assert trace['verification']['pass'] is True

if __name__ == '__main__':
    test_basic_mul()
