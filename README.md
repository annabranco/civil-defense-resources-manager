# CIVIL DEFENSE RESOURCES MANAGER (beta version)

<img alt="Screenshot of how to change variables on Postman" src="https://github.com/annabranco/civil-defense-resources-manager/raw/develop/assets/prote-civ-logo.png" width="20%">

## Why did I build this project?

Since forever, I've always acted as volunteer on humanitarian organizations such as Red Cross of Civil Defense services and aggrupations. So, when it was time to build my final project for my Full Stack Web Developer nanodegree on Udacity, I thought about doing that could be really usefull for these humanitarian groups.
So, the idea of this API came as a tool for helping Civil Defense Associations - specially the smallest ones - to manage resources, such as volunteers, vehicles and publish services. The goal was to build an application where managers can publish future services and handle the allocation of resources for them. Through the application, volunteers can also easily have access to information about these services and apply for them.
I puclish this beta version of the application (so far, only a backend API) with the hope that it would be a full web application someday and be freely used for humanitarian organizations to help them doing their beautiful work.
I really hope you like it! :)

## Running the project locally

### Important

To run this project locally, it is assumed that you have some knowledge about Python, libraries such as Flask and Auth0, and working with relational databases.

If you are going to run it locally, you need to have your own Auth0 account and config an API with the following roles defined:

1. **Volunteer**

  |Permission|Description|
  |----------|-----------|
  |read:groups|Read groups|
  |read:roles|Read roles|
  |read:services-details|Read detailed data of services|
  |read:volunteers|Read volunteers data|
  |read:volunteers-own|Read full own data|
  |update:volunteers-own|Updates own volunteer data|

2. **Manager**

  |Permission|Description|
  |----------|-----------|
  |create:services|Create services|
  |create:volunteers|Create a volunteer|
  |read:groups|Read groups|
  |read:roles|Read roles|
  |read:services-details|Read detailed data of services|
  |read:services-full|Read full data of services|
  |read:vehicles|Read vehicles data|
  |read:volunteers|Read volunteers data|
  |read:volunteers-details|Read detailed data of volunteers|
  |update:services|Update services data
  |update:vehicles|Update vehicles data|
  |update:volunteers|Update volunteers data|

3. **Admin**

  |Permission|Description|
  |----------|-----------|
  |create:services|Create service|
  |create:vehicles|Create vehicle|
  |create:volunteers|Create a voluntee|
  |delete:services|Delete services data|
  |delete:vehicles|Delete vehicles data|
  |delete:volunteers|Delete volunteers data|
  |read:groups|Read group|
  |read:roles|Read role|
  |read:services-details|Read detailed data of service|
  |read:services-full|Read full data of service|
  |read:vehicles|Read vehicles data|
  |read:vehicles-full|Read full data of vehicle|
  |read:volunteers|Read volunteers data|
  |read:volunteers-details|Read detailed data of volunteer|
  |read:volunteers-full|Read full data of volunteer|
  |read:volunteers-own|Read full own data|
  |update:services|Update services data|
  |update:vehicles|Update vehicles data|
  |update:volunteers|Update volunteers data|
  |update:volunteers-own|Updates own volunteer data|

### Installing the project locally

- Clone the repo
- Have python and pip3 (preferably version 3.9) installed
- On the project volder, run `$ pip3 install -r requirements.txt`
- Create a file named `.env` and set some enviroments variables (you can use the `.env_sample` as base to set your own values. Just rename it to only `.env`).
- On your `.env` file, keep **unchanged** the value of

```env_file
FLASK_APP=app
```

All the other variables need to be changed according to your local and your Auth0 API configurations.

- Once you have all your environments variables set, you can start the application running:
`$ flask run`

## Running from the API server

You can also just access all the resources through the API URL:

https://prote-civ.herokuapp.com/

## Understanding the API

### User accesses

The API allows four different levels of access:

#### Public

- Can view informative data of any services registered

#### Volunteer

- Can view limited data of services available
- Can view groups information
- Can view roles information

#### Manager

- Can have a detailed view, create and update volunteers
- Can have a detailed view, create and update vehicles
- Can have a detailed view, create and update services
- Can view groups information
- Can view roles information

#### Admin

- Can have a full view, create, update and delete all resources
- Can view groups information
- Can view roles information

### Endpoints description

As described before, most endpoints will give different responses for users with different access levels. This will be highlighted on the response examples below.

#### API host:

https://prote-civ.herokuapp.com


| ACTION | ENDPOINT | METHOD | MIN. ACCESS LEVEL | ADDITIONAL BODY |
| --- | --- | --- | --- | --- |
| View all volunteers | /volunteers | GET | volunteer ||
| View one volunteer | /volunteers/\<id> | GET | manager ||
| Create a volunteer | /volunteers | POST |  manager | Volunteer obj.|
| Update a volunteer | /volunteers/\<id> | PATCH | manager | Volunteer obj.|
| Delete a volunteer | /volunteers/\<id> | DELETE | admin ||
| View all vehicles | /vehicles | GET |  manager ||
| View one vehicleo | /vehicles/\<id> | GET |  manager ||
| Create a vehicle | /vehicles | POST | admin | Vehicle obj.|
| Update a vehicle | /vehicles/\<id> | PATCH | manager | Vehicle obj.|
| Delete a vehicle | /vehicles/\<id> | DELETE | admin ||
| View all groups | /groups | GET | volunteer ||
| View one group | /groups/\<id> | GET | volunteer ||
| View all roles | /roles | GET |  volunteer ||
| View one role | /roles/\<id> | GET |  volunteer ||
| View all services | /services | GET |  public ||
| View one service | /services/\<id> | GET | volunteer ||
| Create a service | /services | POST |  manager | Service obj.|
| Update a service | /services/\<id> | PATCH | manager | Service obj.|
| Delete a service | /services/\<id> | DELETE |  admin ||

#### Examples of valide JSON objects on bodies:

**Volunteer**

```json
{
    "name": "Lara",
    "surnames": "Croft",
    "birthday": "1994-07-21",
    "document": "1234567Q",
    "address": "Baskerville St. 221b",
    "email": "lara@prote.ww",
    "phone1": 12345678,
    "phone2": 12345678,
    "role": 3,
    "groups": [1,2,3,4],
    "active": true
}
```

> Optional: ***phone2***

> When createing a volunteer, ***role***, ***group*** and ***active*** are also optional and will be auto-assigned to the default values if these keys are not sent.

**Vehicle**

```json
{
    "name": "Ambulance Type 2",
    "brand": "Demers",
    "license": "1234ATD",
    "year": 2016,
    "next_itv": "2022-06-01",
    "incidences": "Scratched on right door",
    "active": true
}
```

> Optional: ***incidences***

> When createing a vehicle, ***active*** is also optional and will be auto-assigned to the default value if this key is not sent.

> Clarification: *next_itv* refers to the date of the next technical inspection


**Service**

```json
{
    "name": "Visit to hospitalized elders",
    "place": "Hospital Europeo Brigid",
    "date": "2021-11-01, 09:20",
    "vehicles_num": 1,
    "contact_name": "Janus Frota",
    "contact_phone": 12345678,
    "volunteers_num": 2,
    "vehicles": [1,2],
    "volunteers": [2,3]}
}
```

> Optional: ***contact_name*** and ***contact_phone***

> Upon creation, the api does not recognize ***vehicles*** and ***volunteers*** keys. You should oinly use them when updating the service.

## Testing

### Using Postman

The easest way to test this application, while taking a good look on all its endpoints is to use the Postman collection provided on this repo:

`prote-civ.postman_collection.json`

You can import it to your Postman client and run it from Postman.

The default configuration will run the tests for public access, where most endpoints will return 401. This is being tested accordingly.

To test with other user accesses, you need to send a Bearer ***access token*** on the Authentication header. You can do it easily just by changing the Collection variables.

To know hot to get the Access Token, please check [***Getting access token*** below](#access-token). Once you have your Access Token for a specific access level, you should fill it on the Collection variables, changing the *current value* of the key `ACCESS_TOKEN`.

You should also change the *current value* of the key `ACCESS_LEVEL` so it fits the access level of the login account used.

For example, if you got an *admin* Access Token, you should set `ACCESS_LEVEL` to *admin*; for a *manager* token `ACCESS_LEVEL` is *manager* and the same for *volunteer*.

**IMPORTANT**: Failing to change accordingly the `ACCESS_LEVEL` will cause the tests to fail, as the Collection will not run the proper expectations related to the token provided. If your tests are failing, please check if you set correctly the `ACCESS_LEVEL` and the full content of `ACCESS_TOKEN` without any spaces or line breaks.

![Screenshot of how to change variables on Postman](https://github.com/annabranco/civil-defense-resources-manager/raw/develop/assets/postman1.png)

To run the tests, you just need to click on Run and confirm. There are two ways of doing it, as you can see below:
![Screenshot of how to start running the tests on Postman](https://github.com/annabranco/civil-defense-resources-manager/raw/develop/assets/postman2.png)

### Testing locally

Testing locally is a little bit harder, as you need to set your own Auth0 API to do it. But if you want to do it, for testing or evaluation, that's great! You just need to setup the environment keys.

I also recommend creating a dummy database for testing, so you don't mess up with the real database. To create a dummy database for running tests, you should set in your `.env` file the name that you want for the new testing database into the variables `DB_NAME` and also into `DB_TEST_NAME`.

For example:

```env_file
DB_NAME = 'database_test'
DB_TEST_NAME = 'database_test'
```

Uncomment the line 19 on *app.py*

`# db_drop_and_create_all()`

and run it with

`$ flask run`

It will build and hydrate a secondary database for testing.

Stop the application, and on `.env` change back DB_NAME for your original database. Keep `DB_TEST_NAME` with the name of your testing DB.

You can run the tests using

`$ pytest`

For the moment, the local tests are very simplified versions of the tests that you can run on Postman.
For running them correctly, you can change your set on your `.env` file:

```env_file
TESTING_ACCESS_TOKEN = <access token received from the /login>
TESTING_ACCESS_LEVEL = <the user level of the login: volunteer, manager or admin>
```

If you want to run your local tests against the real API, you can also do it by setting on your `.env` file

```env_file
DATABASE_URL_FOR_TESTING=https://prote-civ.herokuapp.com
```

Just remember to use the Access Token from `https://prote-civ.herokuapp.com` (see how to get the Access Token below).


<a id="access-token"></a>

### Getting the Access Token

If you are using the project locally, you need to use your browser to navigate to:

`https://localhost:5000/login`

And fill in the login information corresponding to the desired access level.

But if you are testing it on the server, you should use this URL:

`https://prote-civ.herokuapp.com/login`

If you are testing on the running server, you need to use one existent user. There are three testing users on the API:

|E-Mail|Access Level|
|------|------------|
|volunteer@prote-civ.anya|volunteer|
|manager@prote-civ.anya|manager|
|admin@prote-civ.anya|admin|

If you want to test them, please send me a DM so I can give you the credentials.

To change the user and get another Access Token, you need first logout from the current user:
`https://localhost:5000/logout`
`https://prote-civ.herokuapp.com/logout`

And then, login again with another user.

## Future development

Given the limitations of time, this project was build only as an API to be accessed by a Frontend client. In the future, I intend to build the Frontend framework inside the own application, so that users can really use it directly without having any knowledge of programming.

The main idea is to allow volunteers to update their own data and apply for services, updating these services by including/excluding them. Any volunteer update should automatically trigger a notification for the registered managers.

To be really functional, some definitions would need to change and be updated. I tried to build the definitions broader so they could be easily adapted to most Civil Defense Associations. But I am aware that for it to be really used on real cases scenarios, lots of work still would be needed. Maybe someday it will work and since now I thank you very much for being part of it!

Well, that's it! After sooo much work, I'm proud of it! I hope you like it! :)

Thank you!!!

<img src="https://github.com/annabranco/my-profile/raw/master/src/assets/images/annabranco.png" width="10%">
<a href="https://www.linkedin.com/in/annabranco/">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/240px-LinkedIn_logo_initials.png" width="20px">
</a>

[/annabranco/](https://www.linkedin.com/in/annabranco/)
