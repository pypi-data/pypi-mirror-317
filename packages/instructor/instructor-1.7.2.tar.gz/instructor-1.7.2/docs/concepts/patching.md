---
title: Enhancing OpenAI Client Functionality with New Keywords
description: Learn how to use new keywords for backward compatibility in the OpenAI client, improving functionality and structured output.
---

# Patching

Instructor enhances client functionality with three new keywords for backwards compatibility. This allows use of the enhanced client as usual, with structured output benefits.

- `response_model`: Defines the response type for `chat.completions.create`.
- `max_retries`: Determines retry attempts for failed `chat.completions.create` validations.
- `validation_context`: Provides extra context to the validation process.

The default mode is `instructor.Mode.TOOLS` which is the recommended mode for OpenAI clients. This mode is the most stable and is the most recommended for OpenAI clients. The other modes are for other clients and are not recommended for OpenAI clients.

## Tool Calling

This is the recommended method for OpenAI clients. It is the most stable as functions is being deprecated soon.

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI(), mode=instructor.Mode.TOOLS)
```

### Gemini Tool Calling

Gemini supports tool calling for stuctured data extraction. Gemini tool calling requires `jsonref` to be installed.

!!! warning "Limitations"
Gemini tool calling comes with some known limitations:

    - `strict` Pydantic validation can fail for integer/float and enum validations
    - Gemini tool calling is incompatible with Pydantic schema customizations such as examples due to API limitations and may result in errors
    - Gemini can sometimes call the wrong function name, resulting in malformed or invalid json
    - Gemini tool calling could fail with enum and literal field types

```python
import instructor
import google.generativeai as genai

client = instructor.from_gemini(
    genai.GenerativeModel(), mode=instructor.Mode.GEMINI_TOOLS
)
```

### Gemini Vertex AI Tool Callin

This method allows us to get structured output from Gemini via tool calling with the Vertex AI SDK.

**Note:** Gemini Tool Calling is in preview and there are some limitations, you can learn more in the [Vertex AI examples notebook](../integrations/vertex.md).

```python
import instructor
from vertexai.generative_models import GenerativeModel  # type: ignore
import vertexai

vertexai.init(project="vertexai-generative-models")


client = instructor.from_vertexai(
    client=GenerativeModel("gemini-1.5-pro-preview-0409"),
    mode=instructor.Mode.VERTEXAI_TOOLS,
)
```

## Parallel Tool Calling

Parallel tool calling is also an option but you must set `response_model` to be `Iterable[Union[...]]` types since we expect an array of results. Check out [Parallel Tool Calling](./parallel.md) for more information.

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI(), mode=instructor.Mode.PARALLEL_TOOLS)
```

## Function Calling

Note that function calling is soon to be deprecated in favor of TOOL mode for OpenAI. But will still be supported for other clients.

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI(), mode=instructor.Mode.TOOLS)
```

## JSON Mode

JSON mode uses OpenAI's JSON format for responses by setting `response_format={"type": "json_object"}` in the `chat.completions.create` method.

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI(), mode=instructor.Mode.JSON)
```

JSON mode is also required for [the Gemini Models via OpenAI's SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/call-gemini-using-openai-library#client-setup).

```sh
pip install google-auth
```

```python
import google.auth
import google.auth.transport.requests
import instructor
from openai import OpenAI

creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

# Pass the Vertex endpoint and authentication to the OpenAI SDK
PROJECT = 'PROJECT_ID'
LOCATION = 'LOCATION'

base_url = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/{LOCATION}/endpoints/openapi'
client = instructor.from_openai(
    OpenAI(base_url=base_url, api_key=creds.token), mode=instructor.Mode.JSON
)
```

### Gemini JSON Mode

This mode uses Gemini's response mimetype field to generate a response in JSON format using the schema provided.

```python
import instructor
import google.generativeai as genai

client = instructor.from_gemini(
    genai.GenerativeModel(), mode=instructor.Mode.GEMINI_JSON
)
```

## Markdown JSON Mode

This just asks for the response in JSON format, but it is not recommended, and may not be supported in the future, this is just left to support vision models and models provided by Databricks and will not give you the full benefits of instructor.

!!! warning "Experimental"

    This is not recommended, and may not be supported in the future, this is just left to support vision models and models provided by Databricks.

General syntax:

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI(), mode=instructor.Mode.MD_JSON)
```

Databricks syntax:

```python
import instructor
import os
from openai import OpenAI

DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST", "")

# Assuming Databricks environment variables are set
client = instructor.from_openai(
    OpenAI(
        api_key=DATABRICKS_TOKEN,
        base_url=f"{DATABRICKS_HOST}/serving-endpoints",
    ),
    mode=instructor.Mode.MD_JSON,
)
```
