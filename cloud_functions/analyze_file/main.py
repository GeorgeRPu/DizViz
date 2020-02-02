"""Analyzes file using Google's ML APIs and records results in firestore

Starting point: https://cloud.google.com/functions/docs/tutorials/ocr#processing_images
"""
from google.cloud import firestore, language, storage, vision

db = firestore.Client()
disaster_docs = db.collection('disaster-docs')
language_client = language.LanguageServiceClient()
storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()


def validate_message(message, param):
    var = message.get(param)
    if not var:
        raise ValueError(f'{param} is not provided. Make sure you have'
                         f'property {param} in the request')
    return var


def process_file(file, context):
    """Cloud Function triggered by Cloud Storage when a file is changed.
    Args:
        file (dict): Metadata of the changed file, provided by the triggering
                     Cloud Storage event.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None. The output is written to stdout and Stackdriver Logging.
    """
    bucket = validate_message(file, 'bucket')
    name = validate_message(file, 'name')

    if name.split('.')[-1] in {'jfif', 'jpeg', 'png'}:
        get_labels_landmarks(bucket, name)
        print(f'Image file {name} processed.')
    elif name.split('.')[-1] == 'txt':
        blob = storage_client.get_bucket(bucket).get_blob(name)
        contents = blob.download_as_string().lower()
        get_sentiment(contents, name)
        find_location(contents, name)
        print(f'Text file {name} processed.')
    else:
        print(f'{name} is not a image or text file.')


def get_labels_landmarks(bucket, filename):
    """Uses Google Vision API to get top 5 labels for image. Writes to
    firestore.
    """
    uri = f'gs://{bucket}/{filename}'
    response = vision_client.annotate_image({
        'image': {'source': {'image_uri': uri}},
        'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION},
                     {'type': vision.enums.Feature.Type.LANDMARK_DETECTION}],
    })

    error_msg = response.error.message
    if error_msg:
        raise Exception(f'{error_msg}\nFor more info on error messages, check: '
                        f'https://cloud.google.com/apis/design/errors')

    labels = response.label_annotations
    labels = (label.description for label in labels)
    print('Labels:', *labels)

    landmarks = response.landmark_annotations
    landmarks = (landmark.description for landmark in landmarks)
    print('Landmarks:', *labels)

    doc_id = filename.split('.')[0]
    doc = disaster_docs.document(doc_id)
    doc.set({'labels': list(labels), 'landmarks': list(landmarks)}, merge=True)
    print(f'After set: {doc.get().to_dict()}')


def get_sentiment(bucket, filename):
    """Uses Google Natural Language API to get text sentiment. Writes to
    firestore.
    """
    document = language.types.Document(
        gcs_content_uri=f'gs://{bucket}/{filename}',
        language='en',
        type=language.enums.PLAIN_TEXT,
    )

    response = language_client.analyze_sentiment(document, encoding_type='UTF32')
    sentiment = response.document_sentiment
    print(f'Sentiment score: {sentiment.score}')
    print(f'Sentiment magnitude: {sentiment.magnitude}')

    for sentence in response.sentences:
        print(f'Sentence text: {sentence.text.content}'.format(sentence.text.content))
        print(f'Sentence sentiment score: {sentence.sentiment.score}')
        print(f'Sentence sentiment magnitude: {sentence.sentiment.magnitude}')


locations = {
    ('new York', 'united states'),
    ('san fransisco', 'united states'),
    ('hong kong', "people's republic of china"),
    ('tokyo', 'japan'),
    ('london', 'united kingdom'),
    ('canberra', 'australia')
}


def find_location(contents, filename):
    """Matches text against known list of cities and writes match to firestore.
    """
    for city, country in locations:
        if city in contents:
            print(f'Found {city}, {country} in {filename}')
            doc_id = filename.split('.')[0]
            doc = disaster_docs.get(doc_id)
            doc.update({'location:', {'city': city, 'country': country}})
            break

    print(f'No city in {locations} found.')
