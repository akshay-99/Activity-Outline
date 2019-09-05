import os
from jinja2 import Environment, FileSystemLoader
import shutil
from datetime import datetime
import json

def generate_report(date):
    script_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists( os.path.join(script_path, 'csv_data', f'watch-{date}.csv') ):
        return False

    shutil.copy2(os.path.join( script_path, 'csv_data', f'watch-{date}.csv'), os.path.join( script_path , 'web') )

    report_date = datetime.strptime(date, '%m-%d-%Y').strftime("%A %-d %B %Y")
    generation_date = datetime.now().strftime('%d %B %Y %H:%M')
    csv_file = f'watch-{date}.csv'

    json_data = json.dumps(
        {
            'report_date': report_date,
            'generation_date': generation_date,
            'csv_file': csv_file
        }
    )

    rendered = _render_template(json_data)
    report_filename = os.path.join(script_path, 'web',f'report-{date}.html')
    with open(os.path.join(report_filename), 'w') as f:
        f.write(rendered)

    return report_filename, f'report-{date}.html'

def _render_template(json_data):
    
    file_loader = FileSystemLoader('web')
    env = Environment(
        loader=file_loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    
    template = env.get_template('index.html')
    
    return template.render(json_data=json_data)
