import notify2

from driink import config


def notify(message):
    # configuration
    conf = config.load_user_config()

    # don't show notifications if we disabled them
    if not bool(conf.get('driink', 'notifications_enabled')):
        return

    # Initialize the notification system
    notify2.init("Water Tracker")

    # Create a notification object
    n = notify2.Notification("Driink - Stay Hydrated!", message)

    # Set urgency level (optional)
    n.set_urgency(notify2.URGENCY_NORMAL)

    # Set timeout in milliseconds (optional)
    n.set_timeout(int(conf.get('driink', 'notifications_timeout')))

    # Show the notification
    n.show()
