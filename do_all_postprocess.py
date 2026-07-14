import csv
import re
from pathlib import Path
import zipfile

def parse_value(s):
    # Try to extract a numeric value from the output cell
    if s is None:
        return None
    s = s.strip()
    # handle formats like [123.45] or 123.45
    m = re.search(r"-?\d+\.?\d*(?:e[\-+]?\d+)?", s)
    if m:
        try:
            return float(m.group(0))
        except:
            return None
    return None

def make_plot(csv_path, out_png):
    import matplotlib.pyplot as plt
    names = []
    vals = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.append(row['script'])
            vals.append(parse_value(row['output']))

    # Replace None with 0 for plotting
    vals_plot = [v if v is not None else 0 for v in vals]
    plt.figure(figsize=(10,4))
    plt.bar(range(len(vals_plot)), vals_plot)
    plt.xticks(range(len(names)), [Path(n).stem for n in names], rotation=45, ha='right')
    plt.ylabel('Prediction (numeric)')
    plt.tight_layout()
    plt.savefig(out_png)
    print('WROTE', out_png)

def make_zip(files, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            p = Path(f)
            if p.exists():
                z.write(p, arcname=p.name)
    print('WROTE', zip_path)

def main():
    workspace = Path('.')
    csv_path = workspace / 'all_predictions.csv'
    png = workspace / 'predictions_plot.png'
    zip_path = workspace / 'outputs.zip'

    if csv_path.exists():
        make_plot(csv_path, png)
    else:
        print('all_predictions.csv not found')

    # collect files to zip
    files = ['all_predictions.csv', 'prediction.txt', 'prediction.csv', 'predictions_plot.png']
    # add per-script outputs
    for p in workspace.glob('*_output.txt'):
        files.append(p.name)

    make_zip(files, zip_path)

if __name__ == '__main__':
    main()
