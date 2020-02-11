# DizViz

First responders have an incredibly dangerous job. One reasons is the difficulty of acquiring real-time knowledge of disasters and emergencies as they happen. At the same time, 81% of the US population owns a smartphone, enabling them to photograph or even live stream events and them post to social media in seconds. Our solution is to automatically scrape images from the web and process them using AI. After extracting useful features from the data, we cluster recent images based on location, content, etc. Once enough images are found, they are converted into a 3D model using photogrammetry. This model can be viewed using a VR headset.

Made at SwampHacks VI: https://devpost.com/software/dizviz. Won JPMorgan Chase - Best Hack for Disaster Relief!

## Todo

- [ ] Web scraper
- [x] Processing pipeline
- [ ] Automatic clustering
- [ ] Photogrammetry in the cloud?

## Firestore Schema

```
document id: string
cloud-store-uri
- image: string
- text: string
datetime: timestamp
disaster: array of string
landmarks: array of strings
location
- city: string
- country: string
sentiment
- score: number (negative emotion to positive emotion)
- magnitude: number (amount of emotion)
labels: array of strings
disaster: string
```

## Adding Files to Storage

Use `upload.py` to add any image file `<name>.img_ext` and associated text `name.txt` (`<name>` *must* be the same for both files) to cloud storage.
It also creates an entry in firestore which are populated by cloud functions.
