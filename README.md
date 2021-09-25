# CIVIL DEFENSE RESOURCES MANAGER (beta version)

*(include logo)*

## Why did I build this project?

Since forever, I've always acted as volunteer on humanitarian organizations such as Red Cross of Civil Defense services and aggrupations. So, when it was time to build my final project for my Full Stack Web Developer nanodegree on Udacity, I thought about doing that could be really usefull for these humanitarian groups.
So, the idea of this API came as a tool for helping Civil Defense Associations - specially the smallest ones - to manage resources, such as volunteers, vehicles and publish services. The goal was to build an application where managers can publish future services and handle the allocation of resources for them. Through the application, volunteers can also easily have access to information about these services and apply for them.
I puclish this beta version of the application (so far, only a backend API) with the hope that it would be a full web application someday and be freely used for humanitarian organizations to help them doing their beautiful work.
I really hope you like it! :)

## Important

To run this project locally, it is assumed that you have some knowledge about Python, libraries such as Flask and Auth0, and working with relational databases.

If you are going to run it locally, you need to have your own Auth0 account with the following roles defined:

```txt
Define roles
```

*(include image)*

## Installing the project locally

- Clone the repo
- Have python and pip3 (preferably version 3.9) installed
- On the project repo, run `$ pip3 install -r requirements.txt`
- Create a file named `.env` and set some enviroments variables (you can use the `.env_sample` as base to set your own values. Just rename it to only `.env`).
- On your `.env` file, keep **unchanged** the values of

```env_file
FLASK_APP=app
FLASK_ENV=development
```

All the other variables need to be changed according to your local configurations.

- Once you have all your environments variables set, you can start the application running:
`$ flask run`

## Understanding the API

### User accesses

The API allows four different levels of access:

#### Public

- Can view informative data of any services registered

#### Volunteer

- Can view limited data of services available
- Can apply for any active service where there is vacancy
- Can view resources.
- Can view and update their own data
- Can view groups information

#### Manager

- Can create, update and archive volunteers
- Can create, update and archive vehicles
- Can create, update and delete services
- Can view groups information

#### Admin

- Can view, create, update, archive and delete all resources
- Can view, create, update and delete groups

### Endpoints description

As described before, most endpoints will give different responses for users with different access levels. This will be highlighted on the response examples below.

| ACTION | ENDPOINT | METHOD | BODY |
| --- | --- | --- | --- |
| View all volunteers | /volunteers | GET ||
| View one volunteer | /volunteers/\<id> | GET ||
| Create a volunteer | /volunteers | POST | Volunteer obj.|
| Update a volunteer | /volunteers/\<id> | PATCH ||
| Delete a volunteer | /volunteers/\<id> | DELETE ||
| View all vehicles | /vehicles | GET ||
| View one vehicleo | /vehicles/\<id> | GET ||
| Create a vehicle | /vehicles | POST | Vehicle obj.|
| Update a vehicle | /vehicles/\<id> | PATCH ||
| Delete a vehicle | /vehicles/\<id> | DELETE ||
| View all groups | /groups | GET ||
| View one group | /groups/\<id> | GET ||
| Create a group | /groups | POST | Group obj.|
| Update a group | /groups/\<id> | PATCH ||
| Delete a group | /groups/\<id> | DELETE ||
| View all roles | /roles | GET ||
| View one role | /roles/\<id> | GET ||
| Create a role | /roles | POST | Role obj.|
| Update a role | /roles/\<id> | PATCH ||
| Delete a role | /roles/\<id> | DELETE ||
| View all services | /services | GET ||
| View one service | /services/\<id> | GET ||
| Create a service | /services | POST | Service obj.|
| Update a service | /services/\<id> | PATCH ||
| Delete a service | /services/\<id> | DELETE ||

*(specify objects)*
*(speficy responses)*

## Testing

### Using Postman

The easest way to test this application, while taking a good look on all its endpoints is to use the Postman collection provided on this repo:

`postman_file`

You can import it to your Postman application.
Open enviroments, create two different environments, one for local testing and the other for the server and set these variables on them:

```text
local: localhost:8080
server: https://prote-civ.herokuapp.com
```

*(include image)*

On the collection, run it. It will automatically call all endpoints and run tests on the results. More than 200 tests are passed, moving throughouhly through all the possible cases of use.

### Testing locally

To create a dummy database for running tests, you should set in your `.env` file tje name that you want for the new testing database into the variables DB_NAME and also into DB_TEST_NAME.
For example

```env_file
DB_NAME = 'database_test'
DB_TEST_NAME = 'database_test'
```

Uncomment the line 19 on *app.py*
`# db_drop_and_create_all()`
and run it with
`$ flask run`
It will build and hydrate a secondary database for testing.

Stop the application, and on `.env` change back DB_NAME for your original database. Keep DB_TEST_NAME with the name of your testing DB.

You can run the tests using
`$ pytest`

The tests are the same that you can run on Postman, but here they work only with the local database.
If you want to run your local tests against the real API, you can set on your .env file

```env_file
DATABASE_URL_FOR_TESTING=https://prote-civ.herokuapp.com
```

## Future development

Given the limitations of time, this project was build only as an API to be accessed by a Frontend client. In the future, I intend to build the Frontend framework inside the own application, so that users can really use it directly without having any knowledge of programming.
To be really functional, some definitions would need to change and be updated. I tried to build the definitions broader so they could be easily adapted to most Civil Defense Associations. But I am aware that for it to be really used on real cases scenarios, lots of work still would be needed. Maybe someday it will work and since now I thank you very much for being part of it!

Thank you!!!
