import os

import gi

import asyncio
from datetime import date, datetime, timedelta

from gi.repository import AppIndicator3, GLib, Gtk, Notify
# gi.require_version('Gtk', '3.0')
# gi.require_version('AppIndicator3', '0.1')

import driink.config as u_config
from driink import __version__, db
from driink.notifier import notify




class DriinkApplet:

    def __init__(self, loop):
        self.loop = loop
        self.indicator = AppIndicator3.Indicator.new(
            "driink-applet",
            os.path.expanduser("~/.local/share/driink/resources/water.png"),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

        Notify.init("Driink")

        asyncio.ensure_future(self.schedule_notifications())

    def show_notification(self, _=None):
        """Show a notification."""
        notification = Notify.Notification.new(
            "Driink Reminder",
            "Time to drink some water and stay hydrated!",
            "dialog-information",  # Icon name from the system theme
        )
        notification.show()

    async def schedule_notifications(self):
        """Schedule hourly notifications."""
        while True:
            await asyncio.sleep(3600)  # Wait for one hour

            # check if we had modifications during the past hour
            now = datetime.now()
            drink_registry = db.get_water_log(
                now,
                now + timedelta(hours=1)
            )
            if len(drink_registry) == 0:
                GLib.idle_add(self.show_notification)

    def build_menu(self):
        menu = Gtk.Menu()

        progress_item = Gtk.MenuItem(label="Progress")
        progress_item.connect("activate", self.open_progress)
        menu.append(progress_item)

        # Menu item to log water consumption
        log_menu = Gtk.Menu()
        log_item = Gtk.MenuItem(label="Log ...")
        log_item.set_submenu(log_menu)

        menu.append(log_item)
        quantities = [
            ("50ml", 50),
            ("100ml", 100),
            ("200ml", 200),
            ("500ml", 500),
            ("700ml", 700)
        ]
        for label, amount in quantities:
            quantity_item = Gtk.MenuItem(label=label)
            quantity_item.connect("activate", self.log_water, amount)
            log_menu.append(quantity_item)

        # settings_item = Gtk.MenuItem(label="Settings")
        # settings_item.connect("activate", self.open_settings)
        # menu.append(settings_item)

        separator1 = Gtk.SeparatorMenuItem()
        menu.append(separator1)

        about_item = Gtk.MenuItem(label="About")
        about_item.connect("activate", self.show_about)
        menu.append(about_item)

        # Menu item to quit the app
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def log_water(self, menu_item, amount):
        db.log_drink(amount)
        msg = f"Logged {amount} ml of water."
        notify(msg)

    def quit(self, _):
        Gtk.main_quit()  # Stop the GTK main loop
        self.loop.stop()  # Stop the asyncio event loop

    def display_progress_bar(self, total, daily_goal, percentage):
        """Display the progress in a GTK window with a progress bar."""
        # Create a new window
        window = Gtk.Window(title="Water Consumption Progress")
        window.set_default_size(300, 150)
        window.set_resizable(False)

        # Create a vertical box to hold widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)

        # Create a label to display the progress details
        label = Gtk.Label(label=f"Today you've drank: {total} ml\n"
                                f"Daily Goal: {daily_goal} ml\n"
                                f"Progress: {percentage:.2f}%")
        label.set_justify(Gtk.Justification.CENTER)
        vbox.pack_start(label, False, False, 0)

        # Create a progress bar
        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(percentage / 100)
        progress_bar.set_text(f"{total} ml / {daily_goal} ml")
        progress_bar.set_show_text(True)
        vbox.pack_start(progress_bar, False, False, 0)

        # Add a close button
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", lambda _: window.destroy())
        vbox.pack_start(close_button, False, False, 0)

        # Add the box to the window and show everything
        window.add(vbox)
        window.show_all()

    def open_progress(self, _):
        # Start of today
        start_of_today = datetime.combine(date.today(), datetime.min.time())

        # End of today
        end_of_today = datetime.combine(date.today(), datetime.max.time())

        # Get water consumption from today
        drink_registry = db.get_water_log(start_of_today, end_of_today)
        total = sum(record.amount for record in drink_registry)

        conf = u_config.load_user_config()
        daily_goal = int(conf.get('driink', 'daily_goal'))
        percentage = float(total)*100/float(daily_goal)

        self.display_progress_bar(total, daily_goal, percentage)

    def open_settings(self, _):
        print("Open settings clicked!")

    def show_about(self, _):
        """Show the About dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("Driink - Stay Hydrated")
        dialog.set_version(__version__)
        dialog.set_comments("A simple applet to track water consumption and "
                            "stay hydrated.")
        dialog.set_website("https://github.com/gaccardo/driink")
        dialog.set_authors(["Guido Accardo"])
        dialog.set_logo_icon_name("dialog-information")

        # Show the dialog
        dialog.run()
        dialog.destroy()

    def show_menu(self, menu):
        """Show the given menu."""
        menu.show_all()
        menu.popup(None, None, None, None, Gtk.CURRENT_TIME, 0)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(run_gtk_main())

    DriinkApplet(loop)

    loop.run_forever()


async def run_gtk_main():
    """Run the GTK main loop in an asyncio-compatible way."""
    await asyncio.to_thread(Gtk.main)


if __name__ == "__main__":
    main()
