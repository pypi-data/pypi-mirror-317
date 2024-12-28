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

Types:

```python
from mechanix.types import ToolSearchWebResponse, ToolSummarizeContentResponse
```

Methods:

- <code title="post /v1/tools/search_web">client.tools.<a href="./src/mechanix/resources/tools.py">search_web</a>(\*\*<a href="src/mechanix/types/tool_search_web_params.py">params</a>) -> <a href="./src/mechanix/types/tool_search_web_response.py">ToolSearchWebResponse</a></code>
- <code title="post /v1/tools/summarize_content">client.tools.<a href="./src/mechanix/resources/tools.py">summarize_content</a>(\*\*<a href="src/mechanix/types/tool_summarize_content_params.py">params</a>) -> <a href="./src/mechanix/types/tool_summarize_content_response.py">ToolSummarizeContentResponse</a></code>
