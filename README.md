# planning-center

Python wrapper around the planning center API. Expands upon `pypco` by adding types to responses from the Planning Center API.

## Getting Started

Ensure you have the environment variables `CLIENT_ID` and `CLIENT_SECRET` set, or add them to a `.env` file.

## Examples

```python
from planning_center import Client


c = Client()

# Get all people
people = c.services.people.list_all()

# Get a specific person
person_id = 12345
person = c.services.people.get(person_id)

# Look at blockouts for a specific person
blockouts = c.services.people(person_id).blockouts.list_all()
```
