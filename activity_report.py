import click
from setup_cron import setup_cron
from generate_report import generate_report
from datetime import datetime, timedelta
import webbrowser
import http.server
import socketserver


@click.command()
@click.option('--daysago', default=0, help="keep this 0 for today's report")
@click.option('--port', default=9900, help="port number")
def run(daysago, port):
    """A simple program that reports on your daily desktop app usage."""
    cronstatus = setup_cron()
    if not cronstatus:
        click.echo('Cronjob already setup')
    else:
        click.echo(click.style('Cronjob setup successfull', fg='green'))

    date = datetime.now() - timedelta(days= daysago)
    date = date.strftime("%m-%d-%Y")
    report = generate_report(date)

    if not report:
        click.echo(click.style('No data for this date', fg='red'))
        return
    
    report_file, report_filename = report[0], report[1]

    click.echo(click.style('Report generated sucessfully', fg='green'))
    click.echo(f'Stored to {report_file}')
    
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    

    print("serving at port", port)
    open_report(f'http://localhost:{port}/web/{report_filename}')
    try:                                                                                                                    
        httpd.serve_forever()
    except Exception:
        httpd.shutdown()
        
    

def open_report(r):
    webbrowser.open_new(r)
    

if __name__ == '__main__':
    run()