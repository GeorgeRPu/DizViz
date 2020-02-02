from google.cloud import firestore
import difflib
import flask

db = firestore.Client()
disaster_docs = db.collection('disaster-docs')


def similar(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def handle_http(request):
    """Entrypoint for Cloud Function.
    """
    if request.method == 'GET':
        return gather_related(request)
    else:
        return flask.abort(405)


def gather_related(request):
    """Groups related Firestore documents. For now it groups by name.
    """
    threshold = 0.8

    groups = []
    names = set()
    for doc_snapshot in disaster_docs.stream():
        biggest_sim, closest_name = maximize(doc_snapshot.id, names)
        if biggest_sim > threshold and closest_name is not None:
            idx = find_group_idx(groups, closest_name)
            groups[idx].append(doc_snapshot.id)
        else:
            groups.append([doc_snapshot.id])
        names.add(doc_snapshot.id)

    # convert sets to lists as set cannot be converted into JSON
    groups = [list(group) for group in groups]
    return flask.jsonify({'grouping': groups})


def maximize(x, Y):
    max = float('-inf')
    argmin = None
    for y in Y:
        sim = similar(x, y)
        if sim > max:
            max = sim
            argmin = y
    return max, argmin


def find_group_idx(groups, name):
    for i, group in enumerate(groups):
        if name in group:
            return i
    return -1
