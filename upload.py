from google.cloud import firestore, storage
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('image_path')
parser.add_argument('--datetime')
parser.add_argument('--city')
parser.add_argument('--country')
args = parser.parse_args()

db = firestore.Client()
disaster_docs = db.collection('disaster-docs')
client = storage.Client()

# create firestore document

# hour:minute AM (or PM) month/day/year  hour, month, day can be 1 digit
datetime_format = f"%H:%M %p %m/%d/%Y"
timestamp = datetime.strptime(args.datetime, datetime_format)

if args.city and args.country:
    location = {'city': args.city, 'country': args.country}
else:
    location = {}

data = {
    'datetime': timestamp,
    'disaster': '',
    'labels': [],
    'landmarks': [],
    'location': location,
    'sentiment': {}
}

doc_id = args.image_path.split('.')[0]
doc = disaster_docs.document(doc_id)
if doc is None:
    disaster_docs.add(data, doc_id)
else:
    doc.set(data)

# add files to cloud storage

disaster_data = client.bucket('disaster-data')
image_blob = disaster_data.blob(args.image_path)
image_blob.upload_from_filename(args.image_path)
text_path = doc_id + '.txt'
text_blob = disaster_data.blob(text_path)
text_blob.upload_from_filename(text_path)

print('Files uploaded')
