from datetime import date, datetime

import click

import driink.config as u_config
from driink import db
from driink.migrations import ensure_migrations
from driink.notifier import notify
from driink.visualizations import display_progress

user_config = u_config.load_user_config()


@click.group()
def cli():
    """A command-line tool to track water consumption and remind you to stay
    hydrated.
    """
    pass


# 'drank' Command
@cli.command()
@click.option(
    "--amount",
    required=True,
    type=int,
    help="Amount of water in ml to log."
)
def drank(amount):
    """Log the amount of water you drank."""
    if not u_config.validate():
        print("the configuration is not valid")
        return

    db.log_drink(amount)
    msg = f"Logged {amount}ml of water."
    click.echo(msg)
    notify(msg)


# 'drank' Command
@cli.command()
def progress():
    """Show progress"""
    if not u_config.validate():
        print("the configuration is not valid")
        return

    # Start of today
    start_of_today = datetime.combine(date.today(), datetime.min.time())

    # End of today
    end_of_today = datetime.combine(date.today(), datetime.max.time())

    # Get water consumption from today
    drink_registry = db.get_water_log(start_of_today, end_of_today)
    total = 0
    for record in drink_registry:
        total += record.amount

    print(f"Today you've drank: {total} ml")
    conf = u_config.load_user_config()
    daily_goal = int(conf.get('driink', 'daily_goal'))
    percentage = float(total)*100/float(daily_goal)
    print("Progress")
    display_progress(percentage, total, daily_goal)
    notify(
        f"Today you've drank: {total} ml of {daily_goal} ml "
        f"[{percentage:.2f}%]"
    )


# 'config' Command
@cli.command()
@click.option("--key", required=False, help="Setting name to change")
@click.option("--value", required=False, help="Setting value to change")
def config(key, value):
    """Change configuration settings"""
    if key is None or value is None:
        u_config.present_config()
        return

    if u_config.set_config_param(key, value):
        message = "setting changed successfully"
    else:
        message = "error changing the settings"

    click.echo(message)
    notify(message)


def main():
    ensure_migrations()
    cli()


if __name__ == "__main__":
    cli()
