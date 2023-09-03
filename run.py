import os
import sys

from google.cloud import storage
from twilio.rest import Client

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-key.json'

# Twilio config variables
account_sid = "INSERT TWILIO ACCOUNT SID HERE"
auth_token = "INSERT TWILIO AUTH TOKEN HERE"
twilio_phone_number = "INSERT TWILIO PHONE NUMBER HERE"
to_phone_number = "INSERT RECIPIENT PHONE NUMBER HERE"
client = Client(account_sid, auth_token)

def SendTextMessage(text: str):
    _ = client.messages.create(
        to=to_phone_number,
        from_=twilio_phone_number,
        body=text)

def RetrieveMessage(index: int):
    file = open('motivationaltexts.txt', 'r')
    lines = file.readlines()
    file.close()

    return lines[index]

def RetrieveIndex():
    # Initialize the GCS client
    storage_client = storage.Client(project="INSERT PROJECT ID HERE")

    # Define your GCS bucket and file name
    bucket_name = 'INSERT GCP BUCKET NAME HERE'
    file_name = 'index.txt'

    # Read the current value from the GCS file
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        current_value = int(blob.download_as_text())
    except:
        # Handle the case where the file doesn't exist yet
        current_value = 0

    # Increment the value
    new_value = current_value + 1

    # Write the updated value back to the GCS file
    blob.upload_from_string(str(new_value))

    return current_value


def main(request):
    index = RetrieveIndex()

    text = RetrieveMessage(index)
    SendTextMessage(text)