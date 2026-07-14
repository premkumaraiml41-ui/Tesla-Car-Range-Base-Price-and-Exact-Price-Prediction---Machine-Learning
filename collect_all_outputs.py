import subprocess
import sys
import csv
from pathlib import Path

SCRIPTS = [
    'tesla-car-base-price-prediction-machine-learning.py',
    'tesla-car-base-price-range-fully-loaded-coefficient-machine-learning.py',
    'tesla-car-fully-loaded-prediction-machine-learning.py',
    'tesla-car-range-prediction-machine-learning.py',
    'save_prediction.py'
]

def run_script(script):
    proc = subprocess.run([sys.executable, script], capture_output=True, text=True)
    out = proc.stdout.strip()
    err = proc.stderr.strip()
    if proc.returncode != 0:
        return f'ERROR (code {proc.returncode}): {err}'
    return out

def main():
    workspace = Path('.')
    rows = []
    for script in SCRIPTS:
        path = workspace / script
        if not path.exists():
            rows.append((script, 'MISSING'))
            continue
        result = run_script(str(path))
        # save individual output
        outfile = workspace / f"{Path(script).stem}_output.txt"
        outfile.write_text(result + '\n')
        rows.append((script, result.replace('\n', ' | ')))

    # write combined CSV
    with open('all_predictions.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['script', 'output'])
        for r in rows:
            writer.writerow(r)

    print('WROTE all_predictions.csv')

if __name__ == '__main__':
    main()
