# Postman Tests

## How to Use

### Postman Client

To import the collection into your Postman client, you can click on the "Import" button in the top left of the application and then drag and drop the JSON file(s_ into the popup menu.

At the moment you can right click and select "Run Folder" for these following folders and it will run all of the routes in the folder selected so you can easily test any changes to the routes.

### Command Line

To run from the command line, you can use Newman which is installed in the Docker container.  For example:

```
docker exec -it milestones_api newman run /app/tests/postman/Milestones_Users.postman_collection.json
```

...produces output like:
```
..............
→ Bulk Update Services
  PUT http://127.0.0.1/v1/users/12e5c13d798c97ee378eb1415b28dfd5d0719a9807178dedbc9659f9/services [200 OK, 1.04kB, 49ms]
  ✓  Successful PUT request

┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│                requests │               10 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│            test-scripts │               20 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│      prerequest-scripts │               14 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│              assertions │               17 │                0 │
├─────────────────────────┴──────────────────┴──────────────────┤
│ total run duration: 418ms                                     │
├───────────────────────────────────────────────────────────────┤
│ total data received: 3.79kB (approx)                          │
├───────────────────────────────────────────────────────────────┤
│ average response time: 22ms [min: 3ms, max: 50ms, s.d.: 19ms] │
└───────────────────────────────────────────────────────────────┘
```

# Each Postman Collection below should leave the database clean when it is done running.


## Milestones_all_routes.postman_collection.json

This collection currently has all of the routes in it. It is essentially a backup of the separate collections and also has the routes in it that are not fully testable yet. It will become outdated as the other collections are updated and is just currently being kept as a backup. Eventually it will be removed and we will just have the separate collections.

## Milestones_admins.postman_collection.json

Running this collection will create a client, client_user, program, and then a program_admin, it will the GET the admin, update the permissions, and then delete them along with everything else.

You should see 27 tests pass

## Milestones_awards.postman_collection.json

Running this collection will create an award, get all awards and one specifically. Then it will update the award added and delete it.

You should see 10 tests pass


## Milestones_budgets.postman_collection.json

Running this collection will create a client and then it will create a static budget, parent budget, and sub budget, it will then run full CRUD checks on all of the budgets and also delete the client in the end.

You should see 38 tests pass

## Milestones_clients.postman_collection.json

Running this collection will create a client and two client_users, it will get them all and individually, update them both, and then delete everything and check that it has been deleted.

You should see 39 tests pass

## Milestones_client_awards.postman_collection.json

Running this collection will create a client and a client_award, it will perform a get all and get one for the client_award. Then it will update the client_award and then delete the client_award and the client.

You should see 14 tests pass

## Milestones_events.postman_collection.json

Running this collection will create a client, client_user, program, program_event and a sub event. It will GET the events and update them and then delete them along with everything else created.

You should see 27 tests pass

## Milestones_message_templates.postman_collection.json

Running his collection will create a message_template, then get them all and get the one created specifically. It will then update the message_template and then delete it.

You should see 5 tests pass

## Milestones_messages.postman_collection.json

Running this collection will create a client, a client_user and a program associated for the client, it will then create a message, get all messages and the one created specifically. Then it will update the message and delete it along with the program, client_user, client, and user.

You should see 32 tests pass

## Milestones_programs.postman_collection.json

Running this collection will create a client, a client_user and a program associated for the client, it will get the program, update it, and then delete the program, the client_user, and the client.

You should see 28 tests pass

## Milestones_users.postman_collection.json

This collection is a series of sequential tests regarding users.  In essence:

- Get all users, should 404
- Creates a test user, should succeed
- Gets users again, should get the new user in list of users
- Gets the test user, should get the test user back
- Updates the user, should succeed
- Creates a 2nd service for the test user, should succeed
- Gets the 2nd service for the test user, should get the service back
- Updates the user service, should succeed
- Does a bulk update of services
- Deletes all users and services

You should see 24 tests pass