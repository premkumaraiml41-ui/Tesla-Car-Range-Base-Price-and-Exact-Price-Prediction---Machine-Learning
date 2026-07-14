from pathlib import Path
import csv

def main():
    p = Path('prediction.txt')
    if not p.exists():
        print('prediction.txt not found')
        return
    val = p.read_text().strip()
    if not val:
        print('prediction.txt empty')
        return
    out = Path('all_predictions.csv')
    if not out.exists():
        with open(out, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['script','output'])
    with open(out, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['save_prediction.py', val])
    print('Appended', val)

if __name__ == '__main__':
    main()
