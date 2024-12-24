from datetime import datetime
from pprint import pprint as pp
from pprint import pformat 
from pyaviso import NotificationManager, user_config
from io import StringIO
import sys
import time

# Constants
START_DATE = datetime(1999, 12, 12)  # Start date for the notification listener
LISTENER_EVENT = "data"  # Event for the listener, options are mars and dissemination
TRIGGER_TYPE = "function"  # Type of trigger for the listener

CONFIG = {
    "notification_engine": {
        "host": "aviso.lumi.apps.dte.destination-earth.eu",
        "port": 443,
        "https": True,
    },
    "configuration_engine": {
        "host": "aviso.lumi.apps.dte.destination-earth.eu",
        "port": 443,
        "https": True,
    },
    "schema_parser": "generic",
    "remote_schema": True,
    "auth_type": "none",
    "quiet": True
}  # manually defined configuration

class DTAvisoUtilities:
    def __init__(self, request):
        self.request = request
        self.manager = NotificationManager()
        self.listener = self.create_listener()
        self.notifications=list()
        self.dtu=DTUtilities()
        
    def get_notification(self):
        return self.notifications
    
    def set_notification(self,notification):
        self.notifications.append(notification)

    # Function for the listener to trigger.
    def do_something(self,notification):
        date_str=notification['request']['date']
        
        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        self.set_notification(formatted_date)
        pp(formatted_date)
        
        self.set_notification(formatted_date)
                
    # Function that creates and returns a listener configuration.
    def create_listener(self):
        trigger = {
            "type": TRIGGER_TYPE,
            "function": self.do_something,
        }  # Define the trigger for the listener
        # Return the complete listener configuration
        return {"event": LISTENER_EVENT, "request": self.request, "triggers": [trigger]}
    
    def print_notifications(self):
        
        listeners_config = {"listeners": [self.listener]} 
        config = user_config.UserConfig(**CONFIG)
        #pp(CONFIG)
        #nm = NotificationManager()  # Initialize the NotificationManager
        self.manager.listen(
            listeners=listeners_config, from_date=START_DATE, config=config
        )  # Start listening
        
        print("AAAAAAAAAAAAAAAAAAAA")
        return "BBBBBBBBBBB"

    def stop(self):
        listener_manager=self.manager.listener_manager
        listeners=listener_manager.listeners
        length=len(listeners)
        l0t=str(type(listeners[0]))
        print("listener0 type:"+l0t)
        print("listener0:"+ str(listeners[0]))
        print("len:"+str(length))
        b=self.manager.listener_manager._stop_listener(listeners[0])
        #b=self.manager.listener_manager.cancel_listeners()
        print(b)
        listeners=listener_manager.listeners
        length=len(listeners)
        print("len:"+str(length))
        print("listener0:"+ str(listeners[0]))
        b=self.manager.listener_manager._stop_listener(listeners[0])
        #b=self.manager.listener_manager.cancel_listeners()
        print(b)
        b=listeners[0].stop()
        print(b)
        
class DTUtilities:
    def __init__(self):
        self.notifications=list()
        
    def get_notification(self):
        return self.notifications
    
    def set_notification(self,notification):
        self.notifications.append(notification)