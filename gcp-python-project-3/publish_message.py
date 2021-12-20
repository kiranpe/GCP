#!/usr/bin/env python3

import os
import json
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/kiran/devops/GCP/credentials.json"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

timeout = 3.0

with open("terraform.tfstate") as file:
  data = json.load(file)
  project_id = (data['resources'][1]['instances'][0]['attributes']['project'])
  print(project_id)
  topic_id = (data['resources'][1]['instances'][0]['attributes']['id'])
  print(topic_id)
  subscription_id = (data['resources'][0]['instances'][0]['attributes']['id'])
  print(subscription_id)
  subscription_name = (data['resources'][0]['instances'][0]['attributes']['name'])

future = publisher.publish(topic_id, b'Hello World!!', spam='testing')
print("Publisher messageId=" + future.result())

subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    #print(f"Received {message}\n")
    print(message.data.decode())
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
