# DizViz

## Challenges

Real truck
- Most technically impressive, bonus if serverless (Airpods)

Carnival
- Innovation across the Guest Journey (Raspberry Pi)

Fracture
- Photography/Digital Image Challenge (backback, $150 gift card, Airpods)
- Best use of ARKit (same)

Infinite Energy
- Best Hack (electronics kit + tote + coffee cup + case + accessories)

Infotech
- Most innovative use of a public dataset (speakers)

JPMorgan
- Best Hack for Disaster Relief and Recovery (wireless headphones)

MHL
- Best use of Google Cloud (Google Home Mini)
- Best use of UIPath (backpack)
- 1, 2, 3, Organizer choice ($$$)

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

Use `upload.py` to add any image file `name.img_ext` and associated text `name.txt` (`name` *must* be the same for both files) to cloud storage.
It also creates an entry in firestore which are populated by cloud functions.
