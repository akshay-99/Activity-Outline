import click
from setup_cron import setup_cron
from generate_report import generate_report
from datetime import datetime, timedelta
import webbrowser

@click.command()
@click.option('--daysago', default=0, help="keep this 0 for today's report")
def run(daysago):
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
    

    click.echo(click.style('Report generated sucessfully', fg='green'))
    click.echo(f'Stored to {report}')
    
    open_report(report)
    
def open_report(r):
    webbrowser.open_new(r)
    

if __name__ == '__main__':
    run()