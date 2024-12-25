# Health

Types:

```python
from mechanix.types import HealthRetrieveResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/mechanix/resources/health.py">retrieve</a>() -> <a href="./src/mechanix/types/health_retrieve_response.py">object</a></code>

# Root

Types:

```python
from mechanix.types import RootRetrieveResponse
```

Methods:

- <code title="get /health">client.root.<a href="./src/mechanix/resources/root.py">retrieve</a>() -> <a href="./src/mechanix/types/root_retrieve_response.py">object</a></code>

# Users

Types:

```python
from mechanix.types import UserModel
```

Methods:

- <code title="post /v1/users/view">client.users.<a href="./src/mechanix/resources/users.py">view</a>(\*\*<a href="src/mechanix/types/user_view_params.py">params</a>) -> <a href="./src/mechanix/types/user_model.py">UserModel</a></code>

# Tools

## Search

Types:

```python
from mechanix.types.tools import SearchResponseBundle
```

Methods:

- <code title="post /v1/tools/search/web">client.tools.search.<a href="./src/mechanix/resources/tools/search.py">web</a>(\*\*<a href="src/mechanix/types/tools/search_web_params.py">params</a>) -> <a href="./src/mechanix/types/tools/search_response_bundle.py">SearchResponseBundle</a></code>

## Summarize

Types:

```python
from mechanix.types.tools import SummaryItem
```

Methods:

- <code title="post /v1/tools/summarize/youtube">client.tools.summarize.<a href="./src/mechanix/resources/tools/summarize.py">youtube</a>(\*\*<a href="src/mechanix/types/tools/summarize_youtube_params.py">params</a>) -> <a href="./src/mechanix/types/tools/summary_item.py">SummaryItem</a></code>
