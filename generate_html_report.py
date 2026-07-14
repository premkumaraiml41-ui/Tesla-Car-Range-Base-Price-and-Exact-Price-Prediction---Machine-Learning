import csv
import base64
from datetime import datetime
from pathlib import Path

OUTPUT_HTML = Path('report.html')
CSV_PATH = Path('all_predictions.csv')
PLOT_PATH = Path('predictions_plot.png')


def read_predictions(csv_path):
    rows = []
    if not csv_path.exists():
        return rows
    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def parse_numeric(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    # pick the first numeric token
    for token in text.replace('[', ' ').replace(']', ' ').split():
        try:
            return float(token)
        except ValueError:
            continue
    return None


def encode_image(path):
    if not path.exists():
        return ''
    data = path.read_bytes()
    return base64.b64encode(data).decode('utf-8')


def build_summary(rows):
    stats = {
        'total_scripts': len(rows),
        'numeric_outputs': 0,
        'error_outputs': 0,
        'avg_value': None,
        'min_value': None,
        'max_value': None,
    }
    values = []
    for row in rows:
        output = row.get('output', '')
        numeric = parse_numeric(output)
        if numeric is not None:
            values.append(numeric)
        else:
            stats['error_outputs'] += 1
    if values:
        stats['numeric_outputs'] = len(values)
        stats['avg_value'] = sum(values) / len(values)
        stats['min_value'] = min(values)
        stats['max_value'] = max(values)
    else:
        stats['error_outputs'] = len(rows)
    return stats


def make_card(title, value, description, accent='primary'):
    return f"""
      <div class=\"card card-{accent}\">
        <div class=\"card-title\">{title}</div>
        <div class=\"card-value\">{value}</div>
        <div class=\"card-note\">{description}</div>
      </div>
    """


def main():
    rows = read_predictions(CSV_PATH)
    plot_b64 = encode_image(PLOT_PATH)
    summary = build_summary(rows)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html = [
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        '  <title>Advanced Prediction Dashboard</title>',
        '  <style>',
        '    :root { font-family: Inter, system-ui, sans-serif; color: #1f2937; background: #eef2ff; }',
        '    body { margin: 0; padding: 0; background: #eef2ff; }',
        '    .app-shell { max-width: 1300px; margin: 0 auto; padding: 24px; }',
        '    .header { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; align-items: center; }',
        '    .header h1 { margin: 0; font-size: clamp(2rem, 2.5vw, 3rem); }',
        '    .meta { color: #4b5563; }',
        '    .grid { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin: 24px 0; }',
        '    .card { padding: 20px; border-radius: 18px; box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08); background: #ffffff; }',
        '    .card-primary { border-left: 4px solid #4f46e5; }',
        '    .card-success { border-left: 4px solid #059669; }',
        '    .card-warning { border-left: 4px solid #f59e0b; }',
        '    .card-danger { border-left: 4px solid #dc2626; }',
        '    .card-title { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.12em; color: #6b7280; margin-bottom: 10px; }',
        '    .card-value { font-size: 2rem; font-weight: 700; color: #111827; }',
        '    .card-note { margin-top: 10px; color: #6b7280; line-height: 1.5; }',
        '    .content-section { margin-bottom: 32px; }',
        '    .panel { background: #fff; border-radius: 20px; padding: 24px; box-shadow: 0 18px 35px rgba(15, 23, 42, 0.05); }',
        '    .panel h2 { margin-top: 0; font-size: 1.4rem; }',
        '    .toolbar { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; align-items: center; }',
        '    .toolbar input { flex: 1; min-width: 180px; padding: 12px 14px; border-radius: 999px; border: 1px solid #d1d5db; outline: none; }',
        '    table { width: 100%; border-collapse: collapse; min-width: 640px; }',
        '    thead th { text-align: left; padding: 14px 16px; background: #eef2ff; color: #1f2937; font-weight: 700; }',
        '    tbody tr { background: #ffffff; border-bottom: 1px solid #e5e7eb; }',
        '    tbody td { padding: 14px 16px; color: #334155; }',
        '    tbody tr:hover { background: #f8fafc; }',
        '    .badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 999px; font-size: 0.82rem; font-weight: 600; }',
        '    .badge-ok { color: #065f46; background: #dcfce7; }',
        '    .badge-error { color: #7c2d12; background: #fee2e2; }',
        '    .hero { display: flex; flex-wrap: wrap; gap: 18px; justify-content: space-between; align-items: flex-start; }',
        '    .hero p { max-width: 760px; color: #475569; line-height: 1.8; }',
        '    .image-frame { border-radius: 20px; overflow: hidden; box-shadow: 0 22px 70px rgba(15, 23, 42, 0.12); }',
        '    .image-frame img { width: 100%; display: block; }',
        '    @media (max-width: 760px) { .toolbar { flex-direction: column; } }',
        '  </style>',
        '  <script>',
        '    function filterTable() {',
        '      const search = document.getElementById("searchInput").value.toLowerCase();',
        '      const rows = document.querySelectorAll("tbody tr");',
        '      rows.forEach(row => {',
        '        const text = row.innerText.toLowerCase();',
        '        row.style.display = text.includes(search) ? "table-row" : "none";',
        '      });',
        '    }',
        '  </script>',
        '</head>',
        '<body>',
        '  <div class="app-shell">',
        '    <div class="header">',
        '      <div>',
        '        <h1>Advanced Prediction Dashboard</h1>',
        f'        <div class="meta">Generated on {timestamp}</div>',
        '      </div>',
        '      <div class="meta">Data source: <strong>all_predictions.csv</strong></div>',
        '    </div>',
        '    <div class="hero">',
        '      <div class="panel">',
        '        <h2>Dashboard Summary</h2>',
        '        <p>Latest model run results with numeric output statistics and script status indicators.</p>',
        '      </div>',
        '    </div>',
        '    <div class="grid">',
        make_card('Total scripts', summary['total_scripts'], 'Number of scripts executed', 'primary'),
        make_card('Numeric results', summary['numeric_outputs'], 'Values parsed successfully', 'success'),
        make_card('Error or non-numeric', summary['error_outputs'], 'Outputs that could not be parsed as numbers', 'warning'),
        make_card('Average numeric', f"{summary['avg_value']:.2f}" if summary['avg_value'] is not None else 'N/A', 'Average of numeric outputs', 'danger'),
        make_card('Min value', f"{summary['min_value']:.2f}" if summary['min_value'] is not None else 'N/A', 'Lowest parsed output', 'primary'),
        make_card('Max value', f"{summary['max_value']:.2f}" if summary['max_value'] is not None else 'N/A', 'Highest parsed output', 'success'),
        '    </div>',
        '    <div class="content-section panel">',
        '      <div class="toolbar">',
        '        <input id="searchInput" type="text" placeholder="Search scripts or outputs..." oninput="filterTable()" />',
        '      </div>',
        '      <h2>Script Output Table</h2>',
        '      <table>',
        '        <thead>',
        '          <tr><th>Script</th><th>Output</th><th>Status</th></tr>',
        '        </thead>',
        '        <tbody>',
    ]

    for row in rows:
        script = row.get('script', '')
        output = row.get('output', '')
        numeric = parse_numeric(output)
        status = 'OK' if numeric is not None else 'ERROR'
        badge = 'badge badge-ok' if numeric is not None else 'badge badge-error'
        html.append(f'          <tr><td>{script}</td><td>{output}</td><td><span class="{badge}">{status}</span></td></tr>')

    html.extend([
        '        </tbody>',
        '      </table>',
        '    </div>',
    ])

    if plot_b64:
        html.extend([
            '    <div class="content-section panel">',
            '      <h2>Prediction Plot</h2>',
            '      <div class="image-frame">',
            f'        <img src="data:image/png;base64,{plot_b64}" alt="Prediction Plot" />',
            '      </div>',
            '    </div>',
        ])
    else:
        html.append('    <div class="content-section panel"><p><em>Plot image not found.</em></p></div>')

    html.extend([
        '    <div class="content-section panel">',
        '      <h2>Available Files</h2>',
        f'      <p>Prediction text: <strong>{Path("prediction.txt").name}</strong>, CSV: <strong>{Path("prediction.csv").name}</strong>, ZIP bundle: <strong>{Path("outputs.zip").name}</strong></p>',
        '    </div>',
        '  </div>',
        '</body>',
        '</html>',
    ])

    OUTPUT_HTML.write_text('\n'.join(html), encoding='utf-8')
    print(f'WROTE {OUTPUT_HTML}')


if __name__ == '__main__':
    main()
