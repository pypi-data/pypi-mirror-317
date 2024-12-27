# Fixpoint

Open source infra for stateful AI workflows with memory and human-in-the-loop.

Build AI agents and workflows that remember your data and users, and can work
together with humans or other AI agents to get their work done, reliably. Think
of us like an open-source alternative to OpenAI's Assistant API.

<h3>

[Homepage](https://www.fixpoint.co/) | [Documentation](https://docs.fixpoint.co/) | [Discord](https://discord.gg/tdRmQQXAhY) | [Examples](https://github.com/gofixpoint/fixpoint/tree/main/examples)

</h3>

## Table of contents

- [Why Fixpoint?](#why-fixpoint)
- [Fixpoint's features](#fixpoints-features)
- [Getting started](#getting-started)
  - [A drop-in replacement for OpenAI](#a-drop-in-replacement-for-openai)
  - [Making it a multi-step workflow](#making-it-a-multi-step-workflow)
- [Examples](#examples)
- [Running locally and contributing](#running-locally-and-contributing)


## Why Fixpoint?

By default, AIs don’t remember any context about their work, they cannot
interact with the outside world to fact-check or ask for guidance, and they
make mistakes. Workflows can fail, and you need the AI to be able to recover
gracefully, picking up where they left off or asking for a human-in-the-loop to
correct or review the work.

Fixpoint solves these problems for you so that you can focus on the goals of
your AI and your application.


## Fixpoint's features

- **Workflows** let you coordinate one or more LLMs together in multi-step
  interactions. Each step is checkpointed, so they are reliable in the face of LLM
  provider or other system failure.
- **Memory and Data**: Agents have memory about past users, sessions,
  interactions, and relevant documents.
- **Human-in-the-loop**: Incorporate human-in-the-loop into any step of your LLM
  workflow. You can audit your LLM's outputs, make corrections, or do any other
  human steps before resuming the rest of your workflow.
- **Durability**: Inference providers time out and fail, so Fixpoint supports
  caching, model fallbacks, and agent multi-plexing so you run workflows
  uninterrupted, without double-spending on LLM tokens.
- **Connect to the outside world**: Connect your AI to web search + scraping,
  so they have up-to-date info. Allow your AIs to send and receive emails and
  Slack messages so they can automatically process your comms channels.
- **Structured Data**: Control the structure of your LLM output so that the rest
  of your program can easily work with it.


## Examples

Some example workflows:

- A [Request/Reply Workflow example](https://docs.fixpoint.co/workflows-and-durability/request-reply-workflows#in-depth-use-case-a-chatbot-form-wizard)
  that chats with a user to gather a set of answers and fill out an internal
  form
- A [Structured Workflow example](https://docs.fixpoint.co/workflows-and-durability/structured-workflows#in-depth-use-case-comparing-multiple-llm-models)
  that concurrently compares different LLM models on a prompt, and checkpoints
  all inference requests so you if your experiment fails you don't respend
  on LLM inference when you restart it
- in the [`examples/` directory of our repo](https://github.com/gofixpoint/fixpoint/tree/main/examples) or see some
  example [Jupyter notebooks](https://github.com/gofixpoint/examples-notebooks/tree/main/notebooks)


## Getting started

Fixpoint is a Python package. First, install it:

```bash
pip install fixpoint
```

### A drop-in replacement for OpenAI

Let's say you already have an OpenAI app, but you want to give your AI memory
and output structured data via [Instructor](https://github.com/jxnl/instructor).
You can just swap out your OpenAI client and have a compatible interface.

Let's create a drop-in replacement for your OpenAI agent. It is API-compatible.

```python
# instead of:
# from openai import OpenAI
# client = OpenAI(api_key='...')

from fixpoint.agents.oai import OpenAI
from fixpoint.agents.openai import OpenAIClients

client = OpenAI(
    agent_id="my-agent",
    openai_clients=OpenAIClients.from_api_key(os.environ["OPENAI_API_KEY"]),
)
```

Your agent must have an ID, which is used for when you build multi-agent
workflows. For now, set it to whatever you want.

Now let's add memory and caching to your agent:

- memory: remember all past messages and responses this agent had
- cache: a cache that can be shared between agents to save money and speed up
  inference

```python {1,5-9,14-15}
import fixpoint
from fixpoint.agents.oai import OpenAI
from fixpoint.agents.openai import OpenAIClients

cache = fixpoint.cache.ChatCompletionDiskTLRUCache(
    ttl_s=60 * 60,
    size_limit_bytes=1024 * 1024 * 50,
    cache_dir="/tmp/agent-cache",
)

client = OpenAI(
    agent_id="my-agent",
    openai_clients=OpenAIClients.from_api_key(os.environ["OPENAI_API_KEY"]),
    memory=fixpoint.memory.Memory(),
    cache=cache,
)
```

Let's say we want to ask the LLM a question and get back a Python object that
the rest of our computer program can work with, without writing custom string
parsing code. We'll use Pydantic for that:

```python
class City(BaseModel):
    name: str = Field(description="The name of the city")
    country: str = Field(description="The country the city is in")
    population: int = Field(description="The population of the city")

class CityList(BaseModel):
    cities: list[City]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What are the most populous cities in Europe?"},
    ],
    # specify your structured output format here
    response_model=CityList,
)

for city in completion.fixp.structured_output.cities:
    print(f"{city.name}, {city.country} - population of {city.population}")
```

### Making it a multi-step workflow

Imagine you're building a travel planning LLM. It needs to do a series of
research and planning steps, and at the end return a travel itinerary. You need
to keep track of all of the past steps the LLM took so that you can refer back
to that info later in your workflow. You also want to make sure if any part of
the travel planning process fails, you can resume from there without restarting
the workflow and spending extra on LLM inference costs.

Fixpoint lets you do this using [Structured Workflows](https://docs.fixpoint.co/workflows-and-durability/structured-workflows).
A structured workflow lets you run multiple tasks comprised of multiple agents.
The workflow keeps track of all LLM inferences, and you can load relevant docs
and other state into the workflow for your agents to access. Each task and step
in the workflow is checkpointed, so if the workflow fails you can easily pick
back up from where it left off.

Let's briefly extend our travel agent example:

```python
from fixpoint_extras.workflows import structured

@structured.workflow(id="travel-agent")
class TravelAgent:
    @structured.workflow_entrypoint()
    async def run(self, ctx, continent):
        cities = structured.call_step(ctx, research_cities, continent)
        # take the 2 cities and plan an itinerary for each
        for city in cities.cities[:2]:
            structured.call_step(ctx, plan_itinerary, city.name, city.country)


@structured.step(id="research-cities")
async def research_cities(ctx, continent):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"What are the most populous cities in {continent}?"},
        ],
        response_model=CityList,
    )
    return completion.fixp.structured_output


@structured.step(id="plan-itinerary")
async def plan_itinerary(ctx, city, country):
    completion = ctx.agents['my-agent'].create_completion(
      model_name="gpt-4o",
      messages=[
        {"role": "user", "content": f"Plan a tourist itinerary for 3 days in {city}, {country}."},
      ],
    )
    ctx.workflow_run.docs.store(
      f"itinerary-{city}-{country}.txt",
      completion.choices[0].message.content,
    )
```

To learn more about structured workflows, read the
[Structured Workflows](https://docs.fixpoint.co/workflows-and-durability/structured-workflows)
section of the docs.


## Running locally and contributing

See the [CONTRIBUTING.md](/CONTRIBUTING.md) for how to run Fixpoint locally and contribute.
