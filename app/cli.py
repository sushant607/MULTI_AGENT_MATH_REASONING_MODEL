from agents.debate import DebateSystem
from pathlib import Path
import json
import csv

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_DIR.mkdir(exist_ok=True)
TRACES_CSV = DATA_DIR / 'traces.csv'

def save_trace(trace: dict):
    header = ['problem_id','problem','trace_json']
    is_new = not TRACES_CSV.exists()
    with TRACES_CSV.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(header)
        pid = trace.get('problem_id', '')
        row = [pid, trace.get('problem',''), json.dumps(trace, ensure_ascii=False)]
        writer.writerow(row)

if __name__ == '__main__':
    ds = DebateSystem()
    print('Math Debate Agents — CLI (Version 1)')
    print('Type your math problem (or \q to quit)')
    while True:
        q = input('\nProblem> ').strip()
        if q.lower() in ('q','quit','exit','\q'):
            break
        try:
            trace = ds.run_debate(q)
        except Exception as e:
            print('Error during debate:', e)
            continue
        from pprint import pprint
        pprint(trace)
        if trace.get('verification', {}).get('pass'):
            print('\n✅ Verification passed. Saving trace to data/traces.csv')
            save_trace(trace)
        else:
            print('\n❌ Verification failed. Not saving.')
