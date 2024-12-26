# whats the point of this library?

Graba help you to write better tests mixing concepts like "property testing" and "faker" ideas.

This library help you to make clear the concept of a test, but also it help you to explain/document some of your domain concepts.

As an example, a traditional test might look like this:



```python
def test_user_can_delete_post():
  user = User(
    id=11,
    firstname="John",
    email="anemail@gmail.com",
    mobile="666777888"
    role="admin",
    city="NY",
    enable=True,
    department= "management"
  )
  
  post = Post(
    id=22,
    owner=user,
    content="this is the content of my post"
    showed=True
  )
  
  service_post.delete(post)
  
  assert None == service_post.find_post(id=22)
```

Is a simple example, but you might wonder: 

 - is it relevant in the test that mobile?
 - is it relatevant if the user is enabled or the post is now showed?
 - for this test can I create a user with a different role?
 - is it good this combination of values?. For example even if the test pass, in our company an admin user works in the administration department, however this test is very loose, and is passing using department="management"



Graba reduce all this "specification noise", so you focus on the properties that really matter. So this test would look like this:

```python
from graba.main import Any


def test_user_can_delete_post():
    any = Any()

    user = User(
        id=any.positiveInt(),
        firstname=any.word(),
        email=any.email(),
        mobile=any.mobile(),
        role=any.of(["admin", "user"]),
        city=any.word(),
        enable=True,
        department=any.of([None, "administration", "management"])
    )

    post = Post(
        id=any.positiveInt(),
        owner=user,
        content=any.sentence()
    showed = any.boolean()
    )

    service_post.delete(post)

    assert None == service_post.find_post(id=post.id)
```

This makes clear a few things:

-that the user must be enabled, but also that the role can be multiple, not just "admin" as we specified before.

-it doesnt matter if the post is showed or not



Now we are more clear about our tests values of interests. However still we can missconfigure the initialization of our objects. So lets give an step further

----

# How can you leavarage the most of this library?

This library "shines" when is combined with "builder" pattern, for multiple reasons.

As an example of this:

```python
from app.infrastructure.orm.OrmUser import OrmUser, EnumUserSessionmethod, EnumUserRole
from tests.Any import Any


class BuilderUser:

    def __init__(self):
        any = Any()
        self.id = any.positiveInt()
        self.email = any.email()
        self.created_at = any.dateTime()
        self.email = any.email()
        self.email_confirmed = any.bool()
        self.role = any.of(["admin", "user", "manager"])
        self.department = any.of([None, "management", "administration"])

    def build(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            created_at=self.created_at,
            email_confirmed=self.email_confirmed,
            role=self.role,
            department=self.department
        )

    def admin(self):
        # now you can see how builder explain different types of initializing things in your applications
        # in this case, we explain that an admin is using admin role, but also is working in administration department
        self.role = "admin"
        self.department = "administration"
        return self

    def user(self):
        self.role = "user"
        self.department = None
        return self

    def manager(self):
        self.role = "manager"
        self.department = "management"
        return self

    def withEmail(self, email):
        self.email = email
        return self

    def withCreatedAt(self, created_at):
        self.created_at = created_at
        return self

    def withEmailConfirmed(self):
        self.email_confirmed = True
        return self

    def withEmailNotConfirmed(self):
        self.email_confirmed = False
        return self


class BuilderPost:

    def __init__(self):
        any = Any()
        self.id = any.email()
        self.owner = BuilderUser().build()
        self.content = any.sentene()
        self.showed = any.bool()

    def with_owner(self, owner: User):
        self.owner = user
        return self
```

Then in your tests you use this builder like:

```python
from graba.main import Any

def test_user_can_delete_post():
  any = Any()
  user = BuilderUser()\
            .admin()\
            .withCreatedAt(any.dateTimeAfter(datetime(2024, 12, 16, 14, 30, 0)))\
            .build()
  
  post = BuilderPost()\
            .withOwner(user)\
            .build()
  
  service_post.delete(post)
  
  assert None == service_post.find_post(id=post.id)
```

# Additional features of Graba

You can generate controlled random list of objects:

```python
any = Any()


def createData():
    return {
        "age": any.positiveInt(),
        "name": any.word()
    }


result = any.listOf(
    min=3,
    max=7,
    factoryFunction=createData
)
print(result)
# [
#     {'age': 7323, 'name': 'vecalmzbdcvdwuqk'},
#     {'age': 9705, 'name': 'bdqqpgtpgbfbci'},
#     {'age': 9656, 'name': 'ojizqxl'}
# ]
```

You can "pick" random items from a list:

```python
result = any().subsetOf(min=1, max=4, items=["a", "b", "c", "d", "e", "f"])
print(result) # ['d', 'e', 'b']
```

You can generate random dates upon conditions:

```python
result = any().dateTimeBefore("2022-10-10 23:11:05")
print(result) # 2016-12-28 23:11:05


result = any().datetimeBetween("2023-10-10", "2027-09-09")
print(result) # 2025-08-10 22:00:19
```

# Being realistic: working with "data is dirty" mode

Let's be honest. In real life you cannot expect to recieve all the data "clean". Sometimes you receive a number or a boolean as string, others your
strings are not trimmed, others your null are not consisten so you might receive "null", None, "none", etc.

Graba consider that testing all these edge cases and observe how your application performs is of interests.
As an example of working with fuzzy mode you can do:

```python
from graba.main import Any


def test_user_can_delete_post():
    any = Any(mode_datadirty=True)  # <--- IMPORTANT LINE

    user = User(
        id=any.positiveInt(),  # This might be one of: 23, "23"
        firstname=any.word(),  # This might be one of: " MYword", "MYword", "MYword ", ...
        email=any.word(),
        mobile=any.mobile(),
        role=any.of(["admin", "user"]),
        city=any.word(),
        enable=True,
        department=any.of([None, "administration", "management"])
    )

    post = Post(
        id=any.positiveInt(),  # This might be one of: 34, "34"
        owner=user,
        content=any.sentence(),
        showed=any.boolean()  # This might be one of: "true", True, "True"
    )

    service_post.delete(post)

    service_post.find_post(id=post.id)  # exception!!!!, post.id is not an integer
```

In this case, fuzzy_mode will teach that might be interesting to check some values in the id and possibly make a proper test. This is
so because python is not typed, but with this you can put an extra layer for peace of mind :)
