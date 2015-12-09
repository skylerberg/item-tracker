from tracker import db


ItemTag = db.Table('item_tag', db.Model.metadata,
                   db.Column('item_id', db.Integer, db.ForeignKey('items.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref="items")
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    place = db.relationship("Place", backref="items")
    tags = db.relationship("Tag", secondary=ItemTag, backref="items")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "place_name": self.place.name if self.place else "",
            "price": self.price,
            "tags": [tag.to_dict() for tag in self.tags],
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref="places")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "item_count": len(self.items),
            "value": sum(item.price for item in self.items),
        }


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    color = db.Column(db.String(16))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref="tags")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "user_id": self.user_id,
            "item_count": len(self.items),
            "value": sum(item.price for item in self.items),
        }


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    item_id = db.Column(db.Integer,
                        db.ForeignKey('items.id'))
    item = db.relationship("Item",
                           backref="events",
                           cascade="all, delete-orphan",
                           single_parent=True)

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.timestamp.strftime("%I:%M%p %b. %d, %Y"),
            "itemId": self.item_id,
        }


class EventTagged(db.Model):
    __tablename__ = "tagged_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id'))
    event = db.relationship("Event", backref="tagged_events")
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'))
    tag = db.relationship("Tag", backref="tagged_events")

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.event.timestamp.strftime("%I:%M%p %b. %d, %Y"),
            "type": "tagged",
            "itemId": self.event.item_id,
            "tagId": self.tag_id,
            "tag": self.tag.to_dict(),
        }


class EventNameChanged(db.Model):
    __tablename__ = "name_changed_events"

    id = db.Column(db.Integer, primary_key=True)
    old_name = db.Column(db.String(128))
    new_name = db.Column(db.String(128))
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id'))
    event = db.relationship("Event", backref="name_changed_events")

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.event.timestamp.strftime("%I:%M%p %b. %d, %Y"),
            "type": "nameChanged",
            "itemId": self.event.item_id,
            "oldName": self.old_name,
            "newName": self.new_name,
        }


class EventPriceChanged(db.Model):
    __tablename__ = "price_changed_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id'))
    event = db.relationship("Event", backref="price_changed_events")
    old_price = db.Column(db.Integer)
    new_price = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.event.timestamp.strftime("%I:%M%p %b. %d, %Y"),
            "itemId": self.event.item_id,
            "type": "priceChanged",
            "oldPrice": self.old_price,
            "newPrice": self.new_price,
        }


class EventMoved(db.Model):
    __tablename__ = "moved_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id'))
    event = db.relationship("Event", backref="moved_events")
    new_place_id = db.Column(db.Integer,
                             db.ForeignKey('places.id'))
    new_place = db.relationship("Place",
                                backref="moved_to",
                                foreign_keys=[new_place_id])
    old_place_id = db.Column(db.Integer,
                             db.ForeignKey('places.id'))
    old_place = db.relationship("Place",
                                backref="moved_from",
                                foreign_keys=[old_place_id])

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.event.timestamp.strftime("%I:%M%p %b. %d, %Y"),
            "type": "moved",
            "itemId": self.event.item_id,
            "newPlaceId": self.new_place_id,
            "newPlace": self.new_place.to_dict() if self.new_place else None,
            "oldPlaceId": self.old_place_id,
            "oldPlace": self.old_place.to_dict() if self.old_place else None,
        }
