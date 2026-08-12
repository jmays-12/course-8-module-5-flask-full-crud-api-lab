from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    nextid = max(event.id for event in events) + 1
    for event in events:
        if data["title"] == event.title:
            return "Duplicate event!", 400
    newevent = Event(nextid, data["title"])
    events.append(newevent)

    return jsonify(newevent.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

        return "Error, event not found", 404


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    for event in events:
        if event.id == event_id:
            events.remove(event)
            return jsonify("Event deleted"), 204

    return "Error, event not found", 404


if __name__ == "__main__":
    app.run(debug=True)
