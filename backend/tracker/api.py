import json
from datetime import datetime

from flask import request

from tracker import app, db
from tracker.models import (
    User,
    Place,
    Tag,
    Item,
    ItemTag,
    Event,
    EventTagged,
    EventNameChanged,
    EventPriceChanged,
    EventMoved,
)


@app.route("/users", methods=["GET"])
def get_users():
    return json.dumps([user.to_dict() for user in User.query.all()])


@app.route("/users", methods=["PUT", "POST"])
def put_user():
    data = json.loads(request.data)
    user = User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    return json.dumps(user.to_dict())


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter(User.id == int(user_id)).one()
    return json.dumps(user.to_dict())


@app.route("/users/<user_id>/places", methods=["GET"])
def get_places(user_id):
    query = Place.query.filter(Place.user_id == int(user_id))
    return json.dumps([place.to_dict() for place in query.all()])


@app.route("/users/<user_id>/places", methods=["POST"])
def post_place(user_id):
    data = json.loads(request.data)
    place = Place(name=data["name"], user_id=int(user_id))
    db.session.add(place)
    db.session.commit()
    return json.dumps(place.to_dict())


@app.route("/users/<user_id>/places/<place_id>", methods=["GET"])
def get_place(user_id, place_id):
    place = Place.query.filter(Place.id == int(place_id)).one()
    return json.dumps(place.to_dict())


@app.route("/users/<user_id>/places/<place_id>", methods=["PUT"])
def put_place(user_id, place_id):
    data = json.loads(request.data)
    place = Place.query.filter(Place.id == int(place_id)).one()
    place.name = data["name"]
    db.session.add(place)
    db.session.commit()
    return json.dumps(place.to_dict())


@app.route("/users/<user_id>/places/<place_id>", methods=["DELETE"])
def delete_place(user_id, place_id):
    place = Place.query.filter(Place.id == int(place_id)).one()
    db.session.delete(place)
    db.session.commit()
    return ""


@app.route("/users/<user_id>/tags", methods=["GET"])
def get_tags(user_id):
    query = Tag.query.filter(Tag.user_id == int(user_id))
    return json.dumps([tag.to_dict() for tag in query.all()])


@app.route("/users/<user_id>/tags", methods=["POST", "PUT"])
def post_tag(user_id):
    data = json.loads(request.data)
    tag = Tag(name=data["name"], user_id=int(user_id), color=data["color"])
    db.session.add(tag)
    db.session.commit()
    return json.dumps(tag.to_dict())


@app.route("/users/<user_id>/tags/<tag_id>", methods=["GET"])
def get_tag(user_id, tag_id):
    tag = Tag.query.filter(Tag.id == int(tag_id)).one()
    return json.dumps(tag.to_dict())


@app.route("/users/<user_id>/items", methods=["GET"])
def get_items(user_id):
    query = Item.query.filter(Item.user_id == int(user_id))
    return json.dumps([item.to_dict() for item in query.all()])


@app.route("/users/<user_id>/items", methods=["POST", "PUT"])
def post_item(user_id):
    data = json.loads(request.data)
    item = Item(name=data["name"],
                user_id=int(user_id),
                place_id=data.get("place_id", None),
                price=int(data.get("price", 0)))
    db.session.add(item)
    db.session.commit()
    return json.dumps(item.to_dict())


@app.route("/users/<user_id>/items/<item_id>", methods=["PUT"])
def put_item(user_id, item_id):
    data = json.loads(request.data)
    item = Item.query.filter(Item.id == int(item_id)).one()
    event = Event(timestamp=datetime.now(), item_id=item.id)
    db.session.add(event)
    db.session.commit()
    if data.get("name", item.name) != item.name:
        name_changed = EventNameChanged(
            old_name=item.name,
            new_name=data["name"],
            event_id=event.id)
        db.session.add(name_changed)
        item.name = data["name"]
    if int(data.get("price", item.price)) != item.price:
        price_changed = EventPriceChanged(
            old_price=item.price,
            new_price=int(data["price"]),
            event_id=event.id)
        db.session.add(price_changed)
        item.price = data["price"]
    if "place_id" in data and int(data["place_id"]) != item.place_id:
        old_place_id = item.place_id
        new_place_id = int(data["place_id"])
        print old_place_id, new_place_id
        place_changed = EventMoved(
            old_place_id=old_place_id,
            new_place_id=new_place_id,
            event_id=event.id)
        item.place_id = new_place_id
        db.session.add(place_changed)
    db.session.add(item)
    db.session.commit()
    return json.dumps(item.to_dict())


@app.route("/users/<user_id>/tags/<tag_id>", methods=["PUT"])
def put_tag(user_id, tag_id):
    data = json.loads(request.data)
    tag = Tag.query.filter(Tag.id == int(tag_id)).one()
    tag.name = data.get("name", tag.name)
    tag.color = data.get("color", tag.color)
    db.session.add(tag)
    db.session.commit()
    return json.dumps(tag.to_dict())


@app.route("/users/<user_id>/items/<item_id>", methods=["GET"])
def get_item(user_id, item_id):
    item = Item.query.filter(Item.id == int(item_id)).one()
    return json.dumps(item.to_dict())


@app.route("/users/<user_id>/items/<item_id>", methods=["DELETE"])
def delete_item(user_id, item_id):
    item = Item.query.filter(Item.id == int(item_id)).one()
    db.session.delete(item)
    db.session.commit()
    return ""


@app.route("/users/<user_id>/tags/<tag_id>", methods=["DELETE"])
def delete_tag(user_id, tag_id):
    tag = Tag.query.filter(Tag.id == int(tag_id)).one()
    db.session.delete(tag)
    db.session.commit()
    return ""


@app.route("/users/<user_id>/items/<item_id>/tags/<tag_id>",
           methods=["POST", "PUT"])
def tag_item(user_id, item_id, tag_id):
    item = Item.query.filter(Item.id == int(item_id)).one()
    tag = Tag.query.filter(Tag.id == int(tag_id)).one()
    item.tags.append(tag)
    db.session.add(item)
    event = Event(timestamp=datetime.now(), item_id=item.id)
    db.session.add(event)
    db.session.commit()
    tagged_event = EventTagged(tag_id=tag.id, event_id=event.id)
    db.session.add(tagged_event)
    db.session.commit()
    return json.dumps(item.to_dict())


@app.route("/users/<user_id>/items/<item_id>/tags/<tag_id>",
           methods=["DELETE"])
def untag_item(user_id, item_id, tag_id):
    query = ItemTag.query
    query = query.filter(ItemTag.item_id == int(item_id))
    query = query.filter(ItemTag.tag_id == int(tag_id))
    relation = query.one()
    db.session.delete(relation)
    db.session.commit()
    return ""


@app.route("/users/<user_id>/items/<item_id>/events", methods=["GET"])
def get_events(user_id, item_id):
    price_changes = EventPriceChanged.query.join('event').filter(
        Event.item_id == int(item_id)).all()
    name_changes = EventNameChanged.query.join('event').filter(
        Event.item_id == int(item_id)).all()
    moved = EventMoved.query.join('event').filter(
        Event.item_id == int(item_id)).all()
    tagged = EventTagged.query.join('event').filter(
        Event.item_id == int(item_id)).all()
    sorted_results = sorted(price_changes + name_changes + moved + tagged,
                            key=lambda x: x.event.timestamp)
    return json.dumps([event.to_dict() for event in sorted_results])
