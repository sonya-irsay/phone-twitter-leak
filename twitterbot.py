
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time

#Twitter credentials
CONSUMER_KEY = 'YzlS7uAWdXmhEDUhc4zDoWQL6'
CONSUMER_SECRET = 'fTPQvdgbfQ0blPdGLlZJVxvwJEwh9UG6VdpoNRX1KEEomA9zbZ'
ACCESS_KEY = '991674087721324547-hm452a50s96kJdFcSTndtqgWBKX5fw3'
ACCESS_SECRET = '2rNTYmqoPHCeVMaDgtYdsJUC9ICFUsqiUJd3BShSJ4Pex'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# ADAFRUIT ------------------------------------------------------------
# Import library and create instance of REST client.

# Import standard python modules.
import sys

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient


# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = '8999ffefe40647799ecb8b762983e797'
ADAFRUIT_IO_USERNAME = 'alfatiharufa'  # See https://accounts.adafruit.com
                                                    # to find your username.

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'phone.translations'


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload, retain):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.

    import json
    # message example: [{"message":"the collaboration","lang":"phone.en-us"}]
    j = json.loads('{1}'.format(feed_id, payload))
    print "leaking new data:", j[0]["message"]

    # print('Feed {0} received new value: {1}'.format(feed_id, payload))
    api.update_status(j[0]["message"])
    # print('{1}'.format(feed_id, payload))

    # twitter --------------------------------------------------
    # #File the bot will tweet from
    # filename=open('text.txt','r')
    # f=filename.readlines()
    # filename.close()
    #
    # #Tweet a line every minute
    # for line in f:
    #      api.update_status(line)
    #      print line
    #      time.sleep(60) #Sleep for 1 minute
    #------------------------------------------------------------

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_blocking()

# --------------------------------------------------------------------------
