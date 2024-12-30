# MangoMango


## Basics

### Usage

#### Connecting to MongoDB

To connect to a MongoDB instance, create a `MangoMango` client:

```python
from mangomango import MangoMango

client = MangoMango(host="localhost", port=27017)
```

#### Creating a Database

To create or get a database, use the `get_database` method:

```python
db = client.get_database("mydatabase")
```

#### Defining a Table

To define a table, use the `table` decorator on a Pydantic model. The type will not change, it will just register a table with this Model.
To get the table, use get_table:

```python
@db.table(collection="users", primary_key="id")
class User(BaseModel):
    id: int
    username: str
    email: str

UserTable = db.get_table("users")
```

#### Inserting Data

To insert data into a table:

```python
user = User(id=0, username="john_doe", email="john@example.com")
UserTable.insert(user)
```

#### Querying Data

To query data from a table:

```python
user = UserTable.find({"username": "john_doe"})
print(user.username, user.email)
```

#### Updating Data

To update data in a table, use the update() method. The first argument is the primary key of the object, it can also be the object itself.

```python
UserTable.update(john.id, {"$set": {"email": "john_new@example.com"}})
```

You can also edit the object and re-push it with the same primary key. use push() method that insert if there is no object with the same primary key, else it remove and then insert

```python
john.email = "john_new@example.com"
UserTable.push(john)
```

#### Deleting Data

To delete one data from a table, use remove() method.
Can take either primary key or object as first argument:

```python
UserTable.remove(john.id)
```

#### Bulk Insert

To insert multiple objects:

```python
users = [
    User(id=1, username="alice", email="alice@example.com"),
    User(id=2, username="bob", email="bob@example.com")
]
UserTable.insert_many_iter(users)
```

#### Bulk Update

To update multiple objects:

```python
UserTable.update_many({"username": {"$in": ["alice", "bob"]}}, {"$set": {"active": True}})
```

#### Bulk Delete

To delete multiple objects:

```python
UserTable.remove_many({"username": {"$in": ["alice", "bob"]}})
```

the doc is not finished