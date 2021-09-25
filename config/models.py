from .setup import db
import json

volunteer_groups = db.Table('volunteer_groups',
    db.Column('volunteer', db.Integer, db.ForeignKey('volunteers.id')),
    db.Column('group', db.Integer, db.ForeignKey('groups.id'))
    )

services_volunteer = db.Table('services_volunteer',
    db.Column('volunteer', db.Integer, db.ForeignKey('volunteers.id')),
    db.Column('service', db.Integer, db.ForeignKey('services.id'))
    )

services_vehicles = db.Table('services_vehicles',
    db.Column('vehicle', db.Integer, db.ForeignKey('vehicles.id')),
    db.Column('service', db.Integer, db.ForeignKey('services.id'))
    )

class Volunteer(db.Model):
    __tablename__ = 'volunteers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), nullable=False)
    surnames = db.Column(db.String(40), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    document = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20))
    phone1 = db.Column(db.Integer, nullable=False)
    phone2 = db.Column(db.Integer)
    active = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    groups = db.relationship('Group', secondary=volunteer_groups, backref=db.backref('volunteer'))
    services = db.relationship('Service', secondary=services_volunteer, backref=db.backref('volunteer'))

    def __init__(self, name, surnames, birthday, document, address, email, phone1, phone2, active, role,  groups):
        self.name = name
        self.surnames = surnames
        self.birthday = birthday
        self.document = document
        self.address = address
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2
        self.active = active
        self.groups = groups
        self.role = role

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
       db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def info(self):
        groups_list = [gr.name for gr in self.groups]
        db_role = Role.query.filter(Role.id==self.role).one_or_none()
        role_name = db_role.name if db_role else 'Volunteer'
        return {
          'name': self.name,
          'surnames': self.surnames,
          'groups': groups_list,
          'role': role_name,
          'active': self.active
        }

    def details(self):
        groups_list = [gr.name for gr in self.groups]
        db_role = Role.query.filter(Role.id==self.role).one_or_none()
        role_name = db_role.name if db_role else 'Volunteer'
        return {
            'name': self.name,
            'surnames': self.surnames,
            'groups': groups_list,
            'role': role_name,
            'birthday': self.birthday,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'active': self.active
        }

    def fullData(self):
        groups_list = [gr.name for gr in self.groups]
        db_role = Role.query.filter(Role.id==self.role).one_or_none()
        role_name = db_role.name if db_role else 'Volunteer'
        return {
            'name': self.name,
            'surnames': self.surnames,
            'groups': groups_list,
            'role': role_name,
            'birthday': self.birthday,
            'document': self.document,
            'address': self.address,
            'email': self.email,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'active': self.active
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(12), nullable=False)
    license = db.Column(db.String(7), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    next_itv = db.Column(db.Date, nullable=False)
    incidents = db.Column(db.String(200))
    active = db.Column(db.Boolean, nullable=False)
    services = db.relationship('Service', secondary=services_vehicles, backref=db.backref('vehicle'))

    def __init__(self, name, brand, license, year, next_itv, incidents, active):
        self.name = name
        self.brand = brand
        self.license = license
        self.year = year
        self.next_itv = next_itv
        self.incidents = incidents
        self.active = active

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def info(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'license': self.license,
            'active': self.active,
        }

    def fullData(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'license': self.license,
            'year': self.year,
            'next_itv': self.next_itv,
            'incidents': self.incidents,
            'active': self.active,
        }

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    place = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    vehicles_num = db.Column(db.Integer, nullable=False)
    vehicles = db.relationship("Vehicles", db.ForeignKey('vehicles.id'))
    volunteers_num = db.Column(db.Integer, nullable=False)
    contact_name = db.Column(db.String(30))
    contact_phone = db.Column(db.Integer)
    volunteers = db.relationship('Volunteer', secondary=services_volunteer, backref=db.backref('service_id'))
    vehicles = db.relationship('Vehicle', secondary=services_vehicles, backref=db.backref('service_id'))

    def __init__(self, name, place, date, vehicles_num, vehicles, volunteers_num, volunteers, contact_name, contact_phone):
        self.name = name
        self.place = place
        self.date = date
        self.vehicles_num = vehicles_num
        self.volunteers = volunteers
        self.vehicles = vehicles
        self.volunteers_num = volunteers_num
        self.volunteers = volunteers
        self.contact_name = contact_name
        self.contact_phone = contact_phone

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def info(self):
        return {
            'name': self.name,
            'place': self.place,
            'date': self.date,
        }

    def details(self):
        roles_list = {
          rol.id: rol.name for rol in Role.query.all()
        }
        volunteers_list = [{ 'name': f'{vol.name} {vol.surnames}', 'role': roles_list[vol.role] } for vol in self.volunteers]
        vehicles_list = [f'{veh.name} {veh.year}' for veh in self.vehicles]

        return {
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'vehicles_num': self.vehicles_num,
            'vehicles': vehicles_list,
            'volunteers_num': self.volunteers_num,
            'volunteers': volunteers_list,
        }

    def fullData(self):
        roles_list = {
          rol.id: rol.name for rol in Role.query.all()
        }
        volunteers_list = [{ 'name': f'{vol.name} {vol.surnames}', 'role': roles_list[vol.role] } for vol in self.volunteers]
        vehicles_list = [f'{veh.name} {veh.year}' for veh in self.vehicles]

        return {
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'vehicles_num': self.vehicles_num,
            'vehicles': vehicles_list,
            'volunteers_num': self.volunteers_num,
            'volunteers': volunteers_list,
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
        }

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    volunteers = db.relationship('Volunteer', secondary=volunteer_groups, backref=db.backref('group_id'))

    def __init__(self, name, volunteers):
      self.name = name
      self.volunteers = volunteers

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def info(self):
        roles_list = {
          rol.id: rol.name for rol in Role.query.all()
        }
        volunteers_list = [{ 'name': f'{vol.name} {vol.surnames}', 'role': roles_list[vol.role] } for vol in self.volunteers]
        return {
          'name': self.name,
          'volunteers': volunteers_list,
        }


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    volunteers = db.relationship('Volunteer', backref=db.backref('role_id'))

    def __init__(self, name, volunteers):
        self.name = name
        self.volunteers = volunteers

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def info(self):
        groups_list = {
          gr.id: gr.name for gr in Group.query.all()
        }
        volunteers_list = [{ 'name': f'{vol.name} {vol.surnames}', 'groups': [ groups_list[gr.id] for gr in vol.groups] } for vol in self.volunteers]
        return {
          'name': self.name,
          'volunteers': volunteers_list,
        }
