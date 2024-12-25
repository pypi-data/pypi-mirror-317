# Shared Types

```python
from altmindpy.types import UserOut
```

# Login

Types:

```python
from altmindpy.types import Token
```

Methods:

- <code title="post /api/v1/login/access-token">client.login.<a href="./src/altmindpy/resources/login.py">access_token</a>(\*\*<a href="src/altmindpy/types/login_access_token_params.py">params</a>) -> <a href="./src/altmindpy/types/token.py">Token</a></code>
- <code title="post /api/v1/login/test-token">client.login.<a href="./src/altmindpy/resources/login.py">test_token</a>() -> <a href="./src/altmindpy/types/shared/user_out.py">UserOut</a></code>

# Users

Types:

```python
from altmindpy.types import ResponseMessage, UsersOut
```

Methods:

- <code title="post /api/v1/users/">client.users.<a href="./src/altmindpy/resources/users.py">create</a>(\*\*<a href="src/altmindpy/types/user_create_params.py">params</a>) -> <a href="./src/altmindpy/types/shared/user_out.py">UserOut</a></code>
- <code title="get /api/v1/users/{user_id}">client.users.<a href="./src/altmindpy/resources/users.py">retrieve</a>(user_id) -> <a href="./src/altmindpy/types/shared/user_out.py">UserOut</a></code>
- <code title="patch /api/v1/users/{user_id}">client.users.<a href="./src/altmindpy/resources/users.py">update</a>(user_id, \*\*<a href="src/altmindpy/types/user_update_params.py">params</a>) -> <a href="./src/altmindpy/types/shared/user_out.py">UserOut</a></code>
- <code title="get /api/v1/users/">client.users.<a href="./src/altmindpy/resources/users.py">list</a>(\*\*<a href="src/altmindpy/types/user_list_params.py">params</a>) -> <a href="./src/altmindpy/types/users_out.py">UsersOut</a></code>
- <code title="delete /api/v1/users/{user_id}">client.users.<a href="./src/altmindpy/resources/users.py">delete</a>(user_id) -> <a href="./src/altmindpy/types/response_message.py">ResponseMessage</a></code>
- <code title="post /api/v1/users/open">client.users.<a href="./src/altmindpy/resources/users.py">open</a>(\*\*<a href="src/altmindpy/types/user_open_params.py">params</a>) -> <a href="./src/altmindpy/types/shared/user_out.py">UserOut</a></code>
- <code title="patch /api/v1/users/me/password">client.users.<a href="./src/altmindpy/resources/users.py">password</a>(\*\*<a href="src/altmindpy/types/user_password_params.py">params</a>) -> <a href="./src/altmindpy/types/response_message.py">ResponseMessage</a></code>

# Experimental

Types:

```python
from altmindpy.types import ExperimentalStreamResponse
```

Methods:

- <code title="get /api/v1/experimental/stream">client.experimental.<a href="./src/altmindpy/resources/experimental.py">stream</a>(\*\*<a href="src/altmindpy/types/experimental_stream_params.py">params</a>) -> <a href="./src/altmindpy/types/experimental_stream_response.py">object</a></code>

# Threads

Types:

```python
from altmindpy.types import ThreadDelete, ThreadResponse, ThreadsResponse
```

Methods:

- <code title="post /api/v1/threads/">client.threads.<a href="./src/altmindpy/resources/threads.py">create</a>(\*\*<a href="src/altmindpy/types/thread_create_params.py">params</a>) -> <a href="./src/altmindpy/types/thread_response.py">ThreadResponse</a></code>
- <code title="get /api/v1/threads/{thread_id}">client.threads.<a href="./src/altmindpy/resources/threads.py">retrieve</a>(thread_id) -> <a href="./src/altmindpy/types/thread_response.py">ThreadResponse</a></code>
- <code title="patch /api/v1/threads/{thread_id}">client.threads.<a href="./src/altmindpy/resources/threads.py">update</a>(thread_id, \*\*<a href="src/altmindpy/types/thread_update_params.py">params</a>) -> <a href="./src/altmindpy/types/thread_response.py">ThreadResponse</a></code>
- <code title="get /api/v1/threads/">client.threads.<a href="./src/altmindpy/resources/threads.py">list</a>(\*\*<a href="src/altmindpy/types/thread_list_params.py">params</a>) -> <a href="./src/altmindpy/types/threads_response.py">ThreadsResponse</a></code>
- <code title="delete /api/v1/threads/{thread_id}">client.threads.<a href="./src/altmindpy/resources/threads.py">delete</a>(thread_id) -> <a href="./src/altmindpy/types/thread_delete.py">ThreadDelete</a></code>

# Messages

Types:

```python
from altmindpy.types import MessageDelete, MessageResponse, MessagesResponse
```

Methods:

- <code title="post /api/v1/messages/">client.messages.<a href="./src/altmindpy/resources/messages/messages.py">create</a>(\*\*<a href="src/altmindpy/types/message_create_params.py">params</a>) -> <a href="./src/altmindpy/types/message_response.py">MessageResponse</a></code>
- <code title="get /api/v1/messages/{message_id}">client.messages.<a href="./src/altmindpy/resources/messages/messages.py">retrieve</a>(message_id) -> <a href="./src/altmindpy/types/message_response.py">MessageResponse</a></code>
- <code title="patch /api/v1/messages/{message_id}">client.messages.<a href="./src/altmindpy/resources/messages/messages.py">update</a>(message_id, \*\*<a href="src/altmindpy/types/message_update_params.py">params</a>) -> <a href="./src/altmindpy/types/message_response.py">MessageResponse</a></code>
- <code title="get /api/v1/messages/">client.messages.<a href="./src/altmindpy/resources/messages/messages.py">list</a>(\*\*<a href="src/altmindpy/types/message_list_params.py">params</a>) -> <a href="./src/altmindpy/types/messages_response.py">MessagesResponse</a></code>
- <code title="delete /api/v1/messages/{message_id}">client.messages.<a href="./src/altmindpy/resources/messages/messages.py">delete</a>(message_id) -> <a href="./src/altmindpy/types/message_delete.py">MessageDelete</a></code>

## Thread

Methods:

- <code title="get /api/v1/messages/thread/{thread_id}">client.messages.thread.<a href="./src/altmindpy/resources/messages/thread.py">list</a>(thread_id, \*\*<a href="src/altmindpy/types/messages/thread_list_params.py">params</a>) -> <a href="./src/altmindpy/types/messages_response.py">MessagesResponse</a></code>

# Assistants

Types:

```python
from altmindpy.types import AssistantDelete, AssistantResponse, AssistantsResponse
```

Methods:

- <code title="post /api/v1/assistants/">client.assistants.<a href="./src/altmindpy/resources/assistants.py">create</a>(\*\*<a href="src/altmindpy/types/assistant_create_params.py">params</a>) -> <a href="./src/altmindpy/types/assistant_response.py">AssistantResponse</a></code>
- <code title="get /api/v1/assistants/{assistant_id}">client.assistants.<a href="./src/altmindpy/resources/assistants.py">retrieve</a>(assistant_id) -> <a href="./src/altmindpy/types/assistant_response.py">AssistantResponse</a></code>
- <code title="patch /api/v1/assistants/{assistant_id}">client.assistants.<a href="./src/altmindpy/resources/assistants.py">update</a>(assistant_id, \*\*<a href="src/altmindpy/types/assistant_update_params.py">params</a>) -> <a href="./src/altmindpy/types/assistant_response.py">AssistantResponse</a></code>
- <code title="get /api/v1/assistants/">client.assistants.<a href="./src/altmindpy/resources/assistants.py">list</a>(\*\*<a href="src/altmindpy/types/assistant_list_params.py">params</a>) -> <a href="./src/altmindpy/types/assistants_response.py">AssistantsResponse</a></code>
- <code title="delete /api/v1/assistants/{assistant_id}">client.assistants.<a href="./src/altmindpy/resources/assistants.py">delete</a>(assistant_id) -> <a href="./src/altmindpy/types/assistant_delete.py">AssistantDelete</a></code>

# Runs

Types:

```python
from altmindpy.types import RunResponse, RunsResponse, RunCreateResponse
```

Methods:

- <code title="post /api/v1/runs/">client.runs.<a href="./src/altmindpy/resources/runs.py">create</a>(\*\*<a href="src/altmindpy/types/run_create_params.py">params</a>) -> <a href="./src/altmindpy/types/run_create_response.py">object</a></code>
- <code title="get /api/v1/runs/{run_id}">client.runs.<a href="./src/altmindpy/resources/runs.py">retrieve</a>(run_id) -> <a href="./src/altmindpy/types/run_response.py">RunResponse</a></code>
- <code title="patch /api/v1/runs/{run_id}">client.runs.<a href="./src/altmindpy/resources/runs.py">update</a>(run_id, \*\*<a href="src/altmindpy/types/run_update_params.py">params</a>) -> <a href="./src/altmindpy/types/run_response.py">RunResponse</a></code>
- <code title="get /api/v1/runs/">client.runs.<a href="./src/altmindpy/resources/runs.py">list</a>(\*\*<a href="src/altmindpy/types/run_list_params.py">params</a>) -> <a href="./src/altmindpy/types/runs_response.py">RunsResponse</a></code>
- <code title="post /api/v1/runs/{run_id}">client.runs.<a href="./src/altmindpy/resources/runs.py">delete</a>(run_id) -> <a href="./src/altmindpy/types/run_response.py">RunResponse</a></code>

# Files

Types:

```python
from altmindpy.types import FileDelete, FileResponse, FilesResponse
```

Methods:

- <code title="post /api/v1/files/">client.files.<a href="./src/altmindpy/resources/files/files.py">create</a>(\*\*<a href="src/altmindpy/types/file_create_params.py">params</a>) -> <a href="./src/altmindpy/types/file_response.py">FileResponse</a></code>
- <code title="get /api/v1/files/{file_id}">client.files.<a href="./src/altmindpy/resources/files/files.py">retrieve</a>(file_id) -> <a href="./src/altmindpy/types/file_response.py">FileResponse</a></code>
- <code title="get /api/v1/files/">client.files.<a href="./src/altmindpy/resources/files/files.py">list</a>(\*\*<a href="src/altmindpy/types/file_list_params.py">params</a>) -> <a href="./src/altmindpy/types/files_response.py">FilesResponse</a></code>
- <code title="delete /api/v1/files/{file_id}">client.files.<a href="./src/altmindpy/resources/files/files.py">delete</a>(file_id) -> <a href="./src/altmindpy/types/file_delete.py">FileDelete</a></code>

## Content

Types:

```python
from altmindpy.types.files import ContentRetrieveResponse
```

Methods:

- <code title="get /api/v1/files/content/{file_id}">client.files.content.<a href="./src/altmindpy/resources/files/content.py">retrieve</a>(file_id) -> <a href="./src/altmindpy/types/files/content_retrieve_response.py">object</a></code>
