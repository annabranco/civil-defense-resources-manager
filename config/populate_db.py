from .models import Group, Role, Service, Vehicle, Volunteer
from .setup import db

role_vol = Role(name='Volunteer', volunteers=[])
role_tle = Role(name='Team Leader', volunteers=[])
role_man = Role(name='Manager', volunteers=[])
role_com = Role(name='Commander', volunteers=[])
group_ems = Group(name='EMS', volunteers=[])
group_log = Group(name='Logistics', volunteers=[])
group_com = Group(name='Communications', volunteers=[])
group_soc = Group(name='Social', volunteers=[])
group_adm = Group(name='Administration', volunteers=[])
group_edu = Group(name='Education', volunteers=[])
group_gen = Group(name='Generic', volunteers=[])

def create_default_roles():
    db.session.add(role_vol)
    db.session.add(role_tle)
    db.session.add(role_man)
    db.session.add(role_com)
    db.session.commit()

def create_default_groups():
    db.session.add(group_ems)
    db.session.add(group_log)
    db.session.add(group_com)
    db.session.add(group_soc)
    db.session.add(group_adm)
    db.session.add(group_edu)
    db.session.add(group_gen)
    db.session.commit()

def create_dummy_resources():
    vir = Vehicle(
        name = 'Range Rover',
        brand = 'Leyland',
        license = '1234LRR',
        year = 2015,
        next_itv = '2022-12-31T00:30:00.000Z',
        incidents = '',
        active = True
    )
    ambulance  =  Vehicle(
        name = 'Ambulance Type 1',
        brand = 'Demers',
        license = '1234ATU',
        year = 2020,
        next_itv = '2024-06-01T00:30:00.000Z',
        incidents = 'Scuff marks on right passenger door',
        active = True
    )
    chief = Volunteer(
        name = 'Anna',
        surnames = 'Branco',
        birthday = '2000-06-01',
        document = '12345678-W',
        address = 'Calle de la Suerte, 26',
        email = 'anna@prote.ww',
        phone1 = 12345678,
        phone2 =  87654321,
        active = True,
        role = 4,
        groups = [group_ems, group_com, group_soc, group_adm]
    )
    squad_leader = Volunteer(
        name = 'Debra',
        surnames = 'Reyes Sternkova',
        birthday = '1994-08-13',
        document = '12345678-W',
        address = 'Calle de la Vida, 12',
        email = 'debra@prote.ww',
        phone1 = 12345678,
        phone2 =  None,
        active = True,
        role = 3,
        groups = [group_log, group_adm]
    )
    manager = Volunteer(
        name = 'David',
        surnames = 'Livingstone Algibez',
        birthday = '1970-01-01',
        document = '12345678-W',
        address = 'Calle de la Cruz, 1',
        email = 'algibez@prote.ww',
        phone1 = 12345678,
        phone2 =  None,
        active = True,
        role = 2,
        groups = [group_gen]
    )
    team_member = Volunteer(
        name = 'Cris',
        surnames = 'Lopez Lopez',
        birthday = '1983-12-09',
        document = '12345678-W',
        address = 'Calle de la Anunciación, 31',
        email = 'cris@prote.ww',
        phone1 = 12345678,
        phone2 =  None,
        active = True,
        role = 1,
        groups = [group_soc, group_edu]
    )
    service1 = Service(
        name = 'Preventive service on football match',
        place = 'Av. de Europa, 15 - Estadio del RFC',
        date = '2021-12-02, 11:00',
        vehicles = [ambulance],
        vehicles_num = 1,
        contact_name = 'Marcos de la Torre',
        contact_phone = 12345678,
        volunteers_num = 2,
        volunteers = [chief, team_member]
    )
    service2 = Service(
        name = 'Preventive service on trail running',
        place = 'Club Polideportivo de la Sirena',
        date = '2022-04-02, 17:30',
        vehicles = [vir],
        vehicles_num = 1,
        contact_name = 'Alesandra Hoobstabank',
        contact_phone = 12345678,
        volunteers_num = 3,
        volunteers = [squad_leader, team_member, manager]
    )
    service3 = Service(
        name = 'Fiestas del pueblo',
        place = 'Av. del Ayuntamiento, S/N',
        date = '2021-12-31, 19:00',
        vehicles = [ambulance, vir],
        vehicles_num = 2,
        contact_name = 'Yaiza Blanca',
        contact_phone = 12345678,
        volunteers_num = 6,
        volunteers = [squad_leader]
    )

    db.session.add(vir)
    db.session.add(ambulance)
    db.session.add(chief)
    db.session.add(squad_leader)
    db.session.add(manager)
    db.session.add(team_member)
    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)
    db.session.commit()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # if (Role.query.all())
    if len(Role.query.all()) == 0:
        create_default_roles()
    if len(Group.query.all()) == 0:
        create_default_groups()
    if len(Volunteer.query.all()) == 0:
        # Uncomment it for creating dummy data for testing
        create_dummy_resources()
