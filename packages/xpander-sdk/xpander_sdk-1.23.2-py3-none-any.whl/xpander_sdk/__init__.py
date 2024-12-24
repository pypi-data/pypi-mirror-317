r'''
# Xpander SDK

**Xpander Open Source SDK** empowers developers to build intelligent and reliable AI Agents capable of managing complex, multi-step tasks across diverse systems and platforms. The SDK simplifies challenges like function calling, schema definition, graph enforcement, and prompt group management.

With support for leading LLM providers such as OpenAI, Amazon Bedrock, and NVIDIA NIM, the **Xpander SDK** seamlessly integrates into your existing systems.

![ai-agents-with-xpander](static/images/screenshots/2024-11-19-21-45-27.png)

## 📦 Installation

Choose your preferred package manager:

### npm

```bash
npm install xpander-sdk
```

### pip

```bash
pip install xpander-sdk
```

## 🚀 Getting Started

### Prerequisites

1. Visit [app.xpander.ai](https://app.xpander.ai)
2. Retrieve your Agent Key from the Agent Settings page
3. Install the SDK and make sure you have Node.js installed (required as the SDK runs as a Node.js app under the hood)

### Quick Start Examples

<details><summary>TypeScript</summary>

```python
import { XpanderClient } from 'xpander-sdk';
import * as dotenv from 'dotenv';

dotenv.config();

const xpanderAPIKey = process.env.XPANDER_API_KEY || '';
const xpanderAgentID = process.env.XPANDER_AGENT_ID || '';

const xpanderClient = new XpanderClient({ apiKey: xpanderAPIKey });
const agent = await xpanderClient.agents.get(xpanderAgentID);

// Get available tools for the agent
const tools = await agent.getTools();

// This is a placeholder for AI to analyze the tools and decide which to invoke
// You would typically send these tools to your AI provider (e.g., OpenAI, Anthropic)
// The AI will return a structured response indicating which tools to call
const llmResponse = await yourAIProvider.chat.completions.create({
  messages: [userMessage],
  tools: tools // The tools are formatted for the AI to understand
  // ... other AI configuration
});

// Parse LLM response automatically into tool calls
const toolsToRun = XpanderClient.extractToolCalls(llmResponse);

// Execute multiple tool calls at once
const results = await agent.runTools(toolsToRun);
```

</details><details>
<summary>JavaScript</summary>

```javascript
const { XpanderClient } = require('xpander-sdk');
require('dotenv').config();

const xpanderAPIKey = process.env.XPANDER_API_KEY || '';
const xpanderAgentID = process.env.XPANDER_AGENT_ID || '';

const xpanderClient = new XpanderClient({ apiKey: xpanderAPIKey });
const agent = await xpanderClient.agents.get(xpanderAgentID);

// Get available tools for the agent
const tools = await agent.getTools();

// This is a placeholder for AI to analyze the tools and decide which to invoke
// You would typically send these tools to your AI provider (e.g., OpenAI, Anthropic)
// The AI will return a structured response indicating which tools to call
const llmResponse = await yourAIProvider.chat.completions.create({
  messages: [userMessage],
  tools: tools // The tools are formatted for the AI to understand
  // ... other AI configuration
});

// Parse LLM response automatically into tool calls
const toolsToRun = XpanderClient.extractToolCalls(llmResponse);

// Execute multiple tool calls at once
const results = await agent.runTools(toolsToRun);
```

</details><details>
<summary>Python</summary>

```python
from xpander_sdk import XpanderClient
from dotenv import load_dotenv
import os

load_dotenv()

xpanderAPIKey = os.environ.get("XPANDER_API_KEY", "")
xpanderAgentID = os.environ.get("XPANDER_AGENT_ID", "")

xpander_client = XpanderClient(api_key=xpanderAPIKey)
agent = xpander_client.agents.get(agent_id=xpanderAgentID)

# Get available tools for the agent
tools = agent.get_tools()

# This is a placeholder for AI to analyze the tools and decide which to invoke
# You would typically send these tools to your AI provider (e.g., OpenAI, Anthropic)
# The AI will return a structured response indicating which tools to call
llm_response = your_ai_provider.chat.completions.create(
    messages=[user_message],
    tools=tools  # The tools are formatted for the AI to understand
    # ... other AI configuration
)

# Parse LLM response automatically into tool calls
tools_to_run = XpanderClient.extract_tool_calls(llm_response=llm_response.model_dump())

# Execute multiple tool calls at once
results = agent.run_tools(tools_to_run)
```

</details><details>
<summary>C#</summary>

```csharp
using Xpander.Sdk;
using DotEnv.Net;

new DotEnvLoader().Load();

var xpanderAPIKey = Environment.GetEnvironmentVariable("XPANDER_API_KEY") ?? "";
var xpanderAgentID = Environment.GetEnvironmentVariable("XPANDER_AGENT_ID") ?? "";

var xpanderClient = new XpanderClient(xpanderAPIKey);
var agent = await xpanderClient.Agents.GetAsync(xpanderAgentID);

// Get available tools for the agent
var tools = await agent.GetToolsAsync();

// This is a placeholder for AI to analyze the tools and decide which to invoke
// You would typically send these tools to your AI provider (e.g., OpenAI, Anthropic)
// The AI will return a structured response indicating which tools to call
var llmResponse = await yourAIProvider.chat.completions.create({
  messages: [userMessage],
  tools: tools // The tools are formatted for the AI to understand
  // ... other AI configuration
});

// Parse LLM response automatically into tool calls
var toolsToRun = XpanderClient.ExtractToolCalls(llmResponse);

// Execute multiple tool calls at once
var results = await agent.RunToolsAsync(toolsToRun);
```

</details>

## 📚 Documentation

For comprehensive documentation, tutorials, and API references, visit:

* [Official Documentation](https://docs.xpander.ai/userguides/overview/introduction)
* [API Reference](https://docs.xpander.ai/api-reference/SDK/getting-started)

## ⚙️ Technical Note

The library is compiled using Projen and runs as a Node.js application under the hood. Ensure you have Node.js installed for optimal performance.

## 🤝 Contributing

We welcome contributions to improve the SDK. Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit improvements and bug fixes.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *


@jsii.enum(jsii_type="xpander-sdk.AgentStatus")
class AgentStatus(enum.Enum):
    '''Enum representing the possible statuses of an agent.'''

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Agents(metaclass=jsii.JSIIMeta, jsii_type="xpander-sdk.Agents"):
    '''Manages a collection of Agent instances in xpanderAI, providing methods to list, retrieve, and initialize specific agents including custom agents.'''

    def __init__(self, configuration: "Configuration") -> None:
        '''
        :param configuration: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c927c42c835c774c6f5f1f6f97fed3b3214baccc5c46df58f7f5cf97262992)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        jsii.create(self.__class__, self, [configuration])

    @jsii.member(jsii_name="get")
    def get(
        self,
        agent_id: builtins.str,
        source_node_type: typing.Optional["SourceNodeType"] = None,
    ) -> "Agent":
        '''Retrieves an agent by ID and initializes it with the given source node type.

        :param agent_id: - The ID of the agent to retrieve.
        :param source_node_type: - The source node type for the agent, default is SDK.

        :return: The requested Agent instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb382a0499d6ff9252ba35bb8f4c90a05697129cfe9cad98a7f8a1a14da8e1d4)
            check_type(argname="argument agent_id", value=agent_id, expected_type=type_hints["agent_id"])
            check_type(argname="argument source_node_type", value=source_node_type, expected_type=type_hints["source_node_type"])
        return typing.cast("Agent", jsii.invoke(self, "get", [agent_id, source_node_type]))

    @jsii.member(jsii_name="getCustomAgent")
    def get_custom_agent(
        self,
        source_node_type: typing.Optional["SourceNodeType"] = None,
    ) -> "Agent":
        '''Retrieves the custom agent instance, initializing it with the given source node type.

        :param source_node_type: - The source node type for the custom agent, default is SDK.

        :return: The custom Agent instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2dae6950d6e1716f079e39f5f02b0b55d94d51d936cd9d0017bfc2c7e8a7109)
            check_type(argname="argument source_node_type", value=source_node_type, expected_type=type_hints["source_node_type"])
        return typing.cast("Agent", jsii.invoke(self, "getCustomAgent", [source_node_type]))

    @jsii.member(jsii_name="list")
    def list(
        self,
        refetch: typing.Optional[builtins.bool] = None,
    ) -> typing.List["Agent"]:
        '''Retrieves the list of agents.

        If ``refetch`` is true, it re-fetches the list
        from the API even if agents are already loaded.

        :param refetch: - If true, forces a re-fetch of the agent list from the API.

        :return: Array of Agent instances.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea39ecf496725a5bdaabe40097604046c959e93c71defecacfbe7b2ca0b8d98)
            check_type(argname="argument refetch", value=refetch, expected_type=type_hints["refetch"])
        return typing.cast(typing.List["Agent"], jsii.invoke(self, "list", [refetch]))

    @builtins.property
    @jsii.member(jsii_name="agentsList")
    def agents_list(self) -> typing.List["Agent"]:
        '''Collection of Agent instances managed by this class.'''
        return typing.cast(typing.List["Agent"], jsii.get(self, "agentsList"))

    @agents_list.setter
    def agents_list(self, value: typing.List["Agent"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f37932ab42616ef0215f3190c6c4bfa79237ec478d6c77803ea5cc9260af1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentsList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "Configuration":
        return typing.cast("Configuration", jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: "Configuration") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4b41eaf57993f4b49ed6bc9995e9ed9fa2685fb355f0d948717f7ea7e34c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]


class AmazonBedrockSupportedModels(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="xpander-sdk.AmazonBedrockSupportedModels",
):
    '''Contains constants representing various models supported by Amazon Bedrock.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_5_SONNET_20240620")
    def ANTHROPIC_CLAUDE_3_5_SONNET_20240620(cls) -> builtins.str:
        '''Anthropocene Claude 3.5 Sonnet model (version 2024-06-20).'''
        return typing.cast(builtins.str, jsii.sget(cls, "ANTHROPIC_CLAUDE_3_5_SONNET_20240620"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_HAIKU_20240307")
    def ANTHROPIC_CLAUDE_3_HAIKU_20240307(cls) -> builtins.str:
        '''Anthropocene Claude 3 Haiku model (version 2024-03-07).'''
        return typing.cast(builtins.str, jsii.sget(cls, "ANTHROPIC_CLAUDE_3_HAIKU_20240307"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_COMMAND_R")
    def COHERE_COMMAND_R(cls) -> builtins.str:
        '''Cohere Command R model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "COHERE_COMMAND_R"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_COMMAND_R_PLUS")
    def COHERE_COMMAND_R_PLUS(cls) -> builtins.str:
        '''Cohere Command R Plus model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "COHERE_COMMAND_R_PLUS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA3_1_405B_INSTRUCT")
    def META_LLAMA3_1_405_B_INSTRUCT(cls) -> builtins.str:
        '''Meta Llama 3 1.405B Instruct model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "META_LLAMA3_1_405B_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA3_1_70B_INSTRUCT")
    def META_LLAMA3_1_70_B_INSTRUCT(cls) -> builtins.str:
        '''Meta Llama 3 1.70B Instruct model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "META_LLAMA3_1_70B_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA3_1_8B_INSTRUCT")
    def META_LLAMA3_1_8_B_INSTRUCT(cls) -> builtins.str:
        '''Meta Llama 3 1.8B Instruct model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "META_LLAMA3_1_8B_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MISTRAL_MISTRAL_LARGE_2402")
    def MISTRAL_MISTRAL_LARGE_2402(cls) -> builtins.str:
        '''Mistral Large 2402 model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "MISTRAL_MISTRAL_LARGE_2402"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MISTRAL_MISTRAL_LARGE_2407")
    def MISTRAL_MISTRAL_LARGE_2407(cls) -> builtins.str:
        '''Mistral Large 2407 model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "MISTRAL_MISTRAL_LARGE_2407"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MISTRAL_MISTRAL_SMALL_2402")
    def MISTRAL_MISTRAL_SMALL_2402(cls) -> builtins.str:
        '''Mistral Small 2402 model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "MISTRAL_MISTRAL_SMALL_2402"))


class _AmazonBedrockSupportedModelsProxy(AmazonBedrockSupportedModels):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AmazonBedrockSupportedModels).__jsii_proxy_class__ = lambda : _AmazonBedrockSupportedModelsProxy


class Base(metaclass=jsii.JSIIMeta, jsii_type="xpander-sdk.Base"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, data: typing.Any) -> "Base":
        '''
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dab3da5f8c0475ccab1873969e148ad9dcbdb0ddf88c9ecc6b02b751238b6e5)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("Base", jsii.sinvoke(cls, "fromObject", [data]))

    @jsii.member(jsii_name="from")
    def from_(self, data: typing.Mapping[typing.Any, typing.Any]) -> "Base":
        '''
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4d603584cc9880629c407e84565dc862d0614d798748f7556e51d6023943cb)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("Base", jsii.invoke(self, "from", [data]))

    @jsii.member(jsii_name="toDict")
    def to_dict(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "toDict", []))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toJson", []))


class Configuration(
    Base,
    metaclass=jsii.JSIIMeta,
    jsii_type="xpander-sdk.Configuration",
):
    '''Manages the configuration settings for the xpanderAI client, including API key, base URL, metrics reporting, and custom parameters.'''

    def __init__(self, __0: "IConfiguration") -> None:
        '''
        :param __0: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafae5b4445df1b4c673783f144d770b151e831e63bc8be999b4708f966d5caa)
            check_type(argname="argument __0", value=__0, expected_type=type_hints["__0"])
        jsii.create(self.__class__, self, [__0])

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''API key for authenticating requests to xpanderAI.'''
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135b56998170832cdd7296e91cdddd9c57d7b17d36e505bee4468b800785e5a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        '''Base URL for the xpanderAI API requests.'''
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6025924c03e9981cc1b85f95320de6d369f9970a79f6ee17298111769cddfa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customParams")
    def custom_params(self) -> "IXpanderClientCustomParams":
        '''Custom parameters for additional configuration options.'''
        return typing.cast("IXpanderClientCustomParams", jsii.get(self, "customParams"))

    @custom_params.setter
    def custom_params(self, value: "IXpanderClientCustomParams") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57aadab9068339b18a9a9bd0a0c861024d57eee8e2450a27a4cf5da13f417253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withMetricsReport")
    def with_metrics_report(self) -> builtins.bool:
        '''Flag to enable or disable metrics reporting.'''
        return typing.cast(builtins.bool, jsii.get(self, "withMetricsReport"))

    @with_metrics_report.setter
    def with_metrics_report(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66c1cb417d578246e8364e66bde633c4843b6604b43b28c0a1768e3d971c32a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withMetricsReport", value) # pyright: ignore[reportArgumentType]


class FriendliAISupportedModels(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="xpander-sdk.FriendliAISupportedModels",
):
    '''Contains constants representing various models supported by OpenAI.

    :remarks:

    This abstract class defines static constants for the supported models
    by xpanderAI's OpenAI real-time integrations.
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_1_70B_INSTRUCT")
    def META_LLAMA_3_1_70_B_INSTRUCT(cls) -> builtins.str:
        '''Meta LLaMA 3.1 70B Instruct model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "META_LLAMA_3_1_70B_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_3_1_8B_INSTRUCT")
    def META_LLAMA_3_1_8_B_INSTRUCT(cls) -> builtins.str:
        '''Meta LLaMA 3.1 8B Instruct model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "META_LLAMA_3_1_8B_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MISTRAL_8X_7B_INSTRUCT")
    def MISTRAL_8_X_7_B_INSTRUCT(cls) -> builtins.str:
        '''Mistral 8x7B Instruct model (version 0.1).'''
        return typing.cast(builtins.str, jsii.sget(cls, "MISTRAL_8X_7B_INSTRUCT"))


class _FriendliAISupportedModelsProxy(FriendliAISupportedModels):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FriendliAISupportedModels).__jsii_proxy_class__ = lambda : _FriendliAISupportedModelsProxy


@jsii.interface(jsii_type="xpander-sdk.IAgentTool")
class IAgentTool(typing_extensions.Protocol):
    '''Interface representing a tool available to an agent.'''

    @builtins.property
    @jsii.member(jsii_name="functionDescription")
    def function_description(self) -> builtins.str:
        '''Function-level description for the tool.'''
        ...

    @function_description.setter
    def function_description(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for the tool.'''
        ...

    @id.setter
    def id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        '''HTTP method used to call the tool.'''
        ...

    @method.setter
    def method(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Name of the tool.'''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Parameters required for executing the tool.'''
        ...

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Endpoint path for the tool.'''
        ...

    @path.setter
    def path(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="pathParams")
    def path_params(self) -> typing.Any:
        '''Parameters for path in the tool’s endpoint.'''
        ...

    @path_params.setter
    def path_params(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(self) -> typing.Any:
        '''Parameters for query in the tool’s endpoint.'''
        ...

    @query_params.setter
    def query_params(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rawDescription")
    def raw_description(self) -> builtins.str:
        '''Raw description of the tool.'''
        ...

    @raw_description.setter
    def raw_description(self, value: builtins.str) -> None:
        ...


class _IAgentToolProxy:
    '''Interface representing a tool available to an agent.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IAgentTool"

    @builtins.property
    @jsii.member(jsii_name="functionDescription")
    def function_description(self) -> builtins.str:
        '''Function-level description for the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "functionDescription"))

    @function_description.setter
    def function_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013ed94cf5075f5bf0c5bc74a0e8036501c284d35e4392ea6f15080eddc2a7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b25237ddc5e6038acd2ee375459e97263388f5a79c9b19df1509b8ad33817e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        '''HTTP method used to call the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba86af1a111c4132196288035231114364f7fd5846ba31b895e28cf0263f6b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Name of the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd4d28b7b8f38ee90640906c0dfa66779e13f1537479bfac62236199af53599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Parameters required for executing the tool.'''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb31aa04b21eb4806b8482aa225a11b478a08f9a3d8fe6ed1ff02f818c62244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Endpoint path for the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7629b10507753cd17f8a141e1f5acf42aa3ad6279b11466521e8e879158f1c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathParams")
    def path_params(self) -> typing.Any:
        '''Parameters for path in the tool’s endpoint.'''
        return typing.cast(typing.Any, jsii.get(self, "pathParams"))

    @path_params.setter
    def path_params(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1639f3cf0ce4876316784b66d4eb55d50082b87dcaa56347a0ebcb4c5be615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(self) -> typing.Any:
        '''Parameters for query in the tool’s endpoint.'''
        return typing.cast(typing.Any, jsii.get(self, "queryParams"))

    @query_params.setter
    def query_params(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76420473c4800542a5c924d1375223fda76771d1a194354c646c87a134351b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawDescription")
    def raw_description(self) -> builtins.str:
        '''Raw description of the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "rawDescription"))

    @raw_description.setter
    def raw_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d18303f76ca1cea7f0333afa6e171a5ff4c99c53601d4772e5d916b00ae6de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawDescription", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAgentTool).__jsii_proxy_class__ = lambda : _IAgentToolProxy


@jsii.interface(jsii_type="xpander-sdk.IBedrockTool")
class IBedrockTool(typing_extensions.Protocol):
    '''Interface representing a Bedrock tool.'''

    @builtins.property
    @jsii.member(jsii_name="toolSpec")
    def tool_spec(self) -> "IBedrockToolSpec":
        '''Specification details for the Bedrock tool.'''
        ...

    @tool_spec.setter
    def tool_spec(self, value: "IBedrockToolSpec") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="execute")
    def execute(self) -> typing.Any:
        '''Function to execute the tool, if defined.'''
        ...

    @execute.setter
    def execute(self, value: typing.Any) -> None:
        ...


class _IBedrockToolProxy:
    '''Interface representing a Bedrock tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IBedrockTool"

    @builtins.property
    @jsii.member(jsii_name="toolSpec")
    def tool_spec(self) -> "IBedrockToolSpec":
        '''Specification details for the Bedrock tool.'''
        return typing.cast("IBedrockToolSpec", jsii.get(self, "toolSpec"))

    @tool_spec.setter
    def tool_spec(self, value: "IBedrockToolSpec") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686bee2f9cc4cb8e5e46bd20309c912c48752fa01feec49d211288fe414d9879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="execute")
    def execute(self) -> typing.Any:
        '''Function to execute the tool, if defined.'''
        return typing.cast(typing.Any, jsii.get(self, "execute"))

    @execute.setter
    def execute(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50442d45bad8e7fa927b6be3feac263e79712091c62056e831a391b5a17c13bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "execute", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBedrockTool).__jsii_proxy_class__ = lambda : _IBedrockToolProxy


@jsii.interface(jsii_type="xpander-sdk.IBedrockToolOutput")
class IBedrockToolOutput(typing_extensions.Protocol):
    '''Output interface for a Bedrock tool.'''

    @builtins.property
    @jsii.member(jsii_name="toolSpec")
    def tool_spec(self) -> "IBedrockToolSpec":
        '''Specification of the Bedrock tool.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="execute")
    def execute(self) -> typing.Any:
        '''Function to execute the Bedrock tool.'''
        ...


class _IBedrockToolOutputProxy:
    '''Output interface for a Bedrock tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IBedrockToolOutput"

    @builtins.property
    @jsii.member(jsii_name="toolSpec")
    def tool_spec(self) -> "IBedrockToolSpec":
        '''Specification of the Bedrock tool.'''
        return typing.cast("IBedrockToolSpec", jsii.get(self, "toolSpec"))

    @builtins.property
    @jsii.member(jsii_name="execute")
    def execute(self) -> typing.Any:
        '''Function to execute the Bedrock tool.'''
        return typing.cast(typing.Any, jsii.get(self, "execute"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBedrockToolOutput).__jsii_proxy_class__ = lambda : _IBedrockToolOutputProxy


@jsii.interface(jsii_type="xpander-sdk.IBedrockToolSpec")
class IBedrockToolSpec(typing_extensions.Protocol):
    '''Interface representing the specification for a Bedrock tool.'''

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of what the Bedrock tool does.'''
        ...

    @description.setter
    def description(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputSchema")
    def input_schema(self) -> "IBedrockToolSpecInputSchema":
        '''Input schema detailing required parameters for the tool.'''
        ...

    @input_schema.setter
    def input_schema(self, value: "IBedrockToolSpecInputSchema") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Bedrock tool.'''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...


class _IBedrockToolSpecProxy:
    '''Interface representing the specification for a Bedrock tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IBedrockToolSpec"

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of what the Bedrock tool does.'''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab15f7ad29e9cbdf37869d4d12b1eca4937a0130eb1409bb74f1149d0dfc26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputSchema")
    def input_schema(self) -> "IBedrockToolSpecInputSchema":
        '''Input schema detailing required parameters for the tool.'''
        return typing.cast("IBedrockToolSpecInputSchema", jsii.get(self, "inputSchema"))

    @input_schema.setter
    def input_schema(self, value: "IBedrockToolSpecInputSchema") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39dfbf6fa195f65cf55b428cbf9c7e700af738bcd9c47ebdda318cfedf78e70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Bedrock tool.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0534d2b1daae9caffc87b99f4b6cc09e1a9eac3888374c04e9c619375c2f1b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBedrockToolSpec).__jsii_proxy_class__ = lambda : _IBedrockToolSpecProxy


@jsii.interface(jsii_type="xpander-sdk.IBedrockToolSpecInputSchema")
class IBedrockToolSpecInputSchema(typing_extensions.Protocol):
    '''Interface representing the input schema for a Bedrock tool.'''

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> typing.Mapping[builtins.str, "IToolParameter"]:
        '''JSON schema defining the parameters for the tool.'''
        ...

    @json.setter
    def json(self, value: typing.Mapping[builtins.str, "IToolParameter"]) -> None:
        ...


class _IBedrockToolSpecInputSchemaProxy:
    '''Interface representing the input schema for a Bedrock tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IBedrockToolSpecInputSchema"

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> typing.Mapping[builtins.str, "IToolParameter"]:
        '''JSON schema defining the parameters for the tool.'''
        return typing.cast(typing.Mapping[builtins.str, "IToolParameter"], jsii.get(self, "json"))

    @json.setter
    def json(self, value: typing.Mapping[builtins.str, "IToolParameter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1454322c6f1b39bdf36a5d88226526fce2d55d1e13ada58cf00d44f12fd64366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "json", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBedrockToolSpecInputSchema).__jsii_proxy_class__ = lambda : _IBedrockToolSpecInputSchemaProxy


@jsii.interface(jsii_type="xpander-sdk.IConfiguration")
class IConfiguration(typing_extensions.Protocol):
    '''Interface representing configuration settings for the xpanderAI client.'''

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''API key for authenticating with xpanderAI.'''
        ...

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="customParams")
    def custom_params(self) -> "IXpanderClientCustomParams":
        '''Custom parameters for client-specific settings.'''
        ...

    @custom_params.setter
    def custom_params(self, value: "IXpanderClientCustomParams") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> typing.Optional[builtins.str]:
        '''Optional base URL for the xpanderAI API.'''
        ...

    @base_url.setter
    def base_url(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="withMetricsReport")
    def with_metrics_report(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable metrics reporting.'''
        ...

    @with_metrics_report.setter
    def with_metrics_report(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IConfigurationProxy:
    '''Interface representing configuration settings for the xpanderAI client.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IConfiguration"

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''API key for authenticating with xpanderAI.'''
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e8b15e3c3381cc6704c1ee29aa4c16d1b4a86e2ac011b6e441b3e0b431f930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customParams")
    def custom_params(self) -> "IXpanderClientCustomParams":
        '''Custom parameters for client-specific settings.'''
        return typing.cast("IXpanderClientCustomParams", jsii.get(self, "customParams"))

    @custom_params.setter
    def custom_params(self, value: "IXpanderClientCustomParams") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83454a3c655acd05227e58cd1768d64624b4c0ca0c928ab30fe2d5404c1c20a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> typing.Optional[builtins.str]:
        '''Optional base URL for the xpanderAI API.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a526e81165d7b0acee70572029a007577d042379f52fcd7844f14a292ff14e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withMetricsReport")
    def with_metrics_report(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable metrics reporting.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "withMetricsReport"))

    @with_metrics_report.setter
    def with_metrics_report(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1540b2d417df65eae973c655ee643690a0dcd51cb4e6c7e9d779c317f9cec97a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withMetricsReport", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConfiguration).__jsii_proxy_class__ = lambda : _IConfigurationProxy


@jsii.interface(jsii_type="xpander-sdk.IGraphItem")
class IGraphItem(typing_extensions.Protocol):
    '''Interface representing an item in an agent's graph, containing the structure of connected nodes, prompt details, and associated group information.'''

    @builtins.property
    @jsii.member(jsii_name="enrichedPrompts")
    def enriched_prompts(self) -> typing.List[builtins.str]:
        '''Array of enriched prompts, providing additional context or formatting.'''
        ...

    @enriched_prompts.setter
    def enriched_prompts(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="graph")
    def graph(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''Representation of the graph structure with nodes and their connections.'''
        ...

    @graph.setter
    def graph(
        self,
        value: typing.Mapping[builtins.str, typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="promptGroupId")
    def prompt_group_id(self) -> builtins.str:
        '''Unique identifier for the prompt group associated with this graph item.'''
        ...

    @prompt_group_id.setter
    def prompt_group_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="prompts")
    def prompts(self) -> typing.List[builtins.str]:
        '''Array of prompt texts associated with the graph item.'''
        ...

    @prompts.setter
    def prompts(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="startingNode")
    def starting_node(self) -> builtins.str:
        '''Identifier for the starting node in the graph.'''
        ...

    @starting_node.setter
    def starting_node(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="operationNodesInstructions")
    def operation_nodes_instructions(
        self,
    ) -> typing.Optional[typing.List["IOperationNodeInstructions"]]:
        ...

    @operation_nodes_instructions.setter
    def operation_nodes_instructions(
        self,
        value: typing.Optional[typing.List["IOperationNodeInstructions"]],
    ) -> None:
        ...


class _IGraphItemProxy:
    '''Interface representing an item in an agent's graph, containing the structure of connected nodes, prompt details, and associated group information.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IGraphItem"

    @builtins.property
    @jsii.member(jsii_name="enrichedPrompts")
    def enriched_prompts(self) -> typing.List[builtins.str]:
        '''Array of enriched prompts, providing additional context or formatting.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enrichedPrompts"))

    @enriched_prompts.setter
    def enriched_prompts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63dac3f67c0f52d800dcd097be9ddb6eb98f70c71ea8289dbaad0e94a58d47f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrichedPrompts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="graph")
    def graph(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''Representation of the graph structure with nodes and their connections.'''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "graph"))

    @graph.setter
    def graph(
        self,
        value: typing.Mapping[builtins.str, typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53cbdb3cb6871f560d5a0a78bd2ceff7528297ba8da6e71aa3da216d1c0284f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graph", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptGroupId")
    def prompt_group_id(self) -> builtins.str:
        '''Unique identifier for the prompt group associated with this graph item.'''
        return typing.cast(builtins.str, jsii.get(self, "promptGroupId"))

    @prompt_group_id.setter
    def prompt_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa5a9bfea7b1902145aadecc5674d2699888d69e501b26b8c8c3ad694675881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prompts")
    def prompts(self) -> typing.List[builtins.str]:
        '''Array of prompt texts associated with the graph item.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prompts"))

    @prompts.setter
    def prompts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a9c3fc5cff09316502fc55db2175287af1ef6831a515963059bd6de019711a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prompts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingNode")
    def starting_node(self) -> builtins.str:
        '''Identifier for the starting node in the graph.'''
        return typing.cast(builtins.str, jsii.get(self, "startingNode"))

    @starting_node.setter
    def starting_node(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c77329d9ea483c6111ccb444f6e30c3a08d7baf27c81a55cc015bb38ed9369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationNodesInstructions")
    def operation_nodes_instructions(
        self,
    ) -> typing.Optional[typing.List["IOperationNodeInstructions"]]:
        return typing.cast(typing.Optional[typing.List["IOperationNodeInstructions"]], jsii.get(self, "operationNodesInstructions"))

    @operation_nodes_instructions.setter
    def operation_nodes_instructions(
        self,
        value: typing.Optional[typing.List["IOperationNodeInstructions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6269099b38fe2e344fbcf8d67e4d22c04f53523963a6b49a82311bfff413a54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationNodesInstructions", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphItem).__jsii_proxy_class__ = lambda : _IGraphItemProxy


@jsii.interface(jsii_type="xpander-sdk.ILocalTool")
class ILocalTool(typing_extensions.Protocol):
    '''Interface for a local tool.'''

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> "ILocalToolFunction":
        '''Function specification for the local tool.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Specifies the tool type as a 'function'.'''
        ...


class _ILocalToolProxy:
    '''Interface for a local tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.ILocalTool"

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> "ILocalToolFunction":
        '''Function specification for the local tool.'''
        return typing.cast("ILocalToolFunction", jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Specifies the tool type as a 'function'.'''
        return typing.cast(builtins.str, jsii.get(self, "type"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILocalTool).__jsii_proxy_class__ = lambda : _ILocalToolProxy


@jsii.interface(jsii_type="xpander-sdk.ILocalToolFunction")
class ILocalToolFunction(typing_extensions.Protocol):
    '''Interface for a function within a local tool.'''

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of the local tool's purpose.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the local tool function.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Parameters used by the local tool function.'''
        ...


class _ILocalToolFunctionProxy:
    '''Interface for a function within a local tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.ILocalToolFunction"

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of the local tool's purpose.'''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the local tool function.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Parameters used by the local tool function.'''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILocalToolFunction).__jsii_proxy_class__ = lambda : _ILocalToolFunctionProxy


@jsii.interface(jsii_type="xpander-sdk.INodeDescription")
class INodeDescription(typing_extensions.Protocol):
    '''Represents a prompt group + node name node's description override.'''

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="promptGroupId")
    def prompt_group_id(self) -> builtins.str:
        ...


class _INodeDescriptionProxy:
    '''Represents a prompt group + node name node's description override.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.INodeDescription"

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeName"))

    @builtins.property
    @jsii.member(jsii_name="promptGroupId")
    def prompt_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "promptGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeDescription).__jsii_proxy_class__ = lambda : _INodeDescriptionProxy


@jsii.interface(jsii_type="xpander-sdk.INodeSchema")
class INodeSchema(typing_extensions.Protocol):
    '''Represents the schema of a single node with defined input and output structures.'''

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> typing.Any:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> typing.Any:
        ...


class _INodeSchemaProxy:
    '''Represents the schema of a single node with defined input and output structures.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.INodeSchema"

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeName"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "output"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeSchema).__jsii_proxy_class__ = lambda : _INodeSchemaProxy


@jsii.interface(jsii_type="xpander-sdk.IOpenAIToolFunctionOutput")
class IOpenAIToolFunctionOutput(typing_extensions.Protocol):
    '''Output interface for an OpenAI tool function.'''

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of the tool function's purpose.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the tool function.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="execute")
    def execute(self) -> typing.Any:
        '''Secondary execution function for Bedrock compatibility.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="func")
    def func(self) -> typing.Any:
        '''Primary function to execute the tool.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional["IToolParameter"]:
        '''Parameters required for the tool function.'''
        ...


class _IOpenAIToolFunctionOutputProxy:
    '''Output interface for an OpenAI tool function.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IOpenAIToolFunctionOutput"

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''Description of the tool function's purpose.'''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the tool function.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="execute")
    def execute(self) -> typing.Any:
        '''Secondary execution function for Bedrock compatibility.'''
        return typing.cast(typing.Any, jsii.get(self, "execute"))

    @builtins.property
    @jsii.member(jsii_name="func")
    def func(self) -> typing.Any:
        '''Primary function to execute the tool.'''
        return typing.cast(typing.Any, jsii.get(self, "func"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional["IToolParameter"]:
        '''Parameters required for the tool function.'''
        return typing.cast(typing.Optional["IToolParameter"], jsii.get(self, "parameters"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOpenAIToolFunctionOutput).__jsii_proxy_class__ = lambda : _IOpenAIToolFunctionOutputProxy


@jsii.interface(jsii_type="xpander-sdk.IOpenAIToolOutput")
class IOpenAIToolOutput(typing_extensions.Protocol):
    '''Output interface for an OpenAI tool.'''

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> IOpenAIToolFunctionOutput:
        '''Function specification for the OpenAI tool.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Type of the tool, typically 'function'.'''
        ...


class _IOpenAIToolOutputProxy:
    '''Output interface for an OpenAI tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IOpenAIToolOutput"

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> IOpenAIToolFunctionOutput:
        '''Function specification for the OpenAI tool.'''
        return typing.cast(IOpenAIToolFunctionOutput, jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Type of the tool, typically 'function'.'''
        return typing.cast(builtins.str, jsii.get(self, "type"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOpenAIToolOutput).__jsii_proxy_class__ = lambda : _IOpenAIToolOutputProxy


@jsii.interface(jsii_type="xpander-sdk.IOperationNodeInstructions")
class IOperationNodeInstructions(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="instructions")
    def instructions(self) -> builtins.str:
        ...

    @instructions.setter
    def instructions(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeIndexInGraph")
    def node_index_in_graph(self) -> jsii.Number:
        ...

    @node_index_in_graph.setter
    def node_index_in_graph(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        ...

    @node_name.setter
    def node_name(self, value: builtins.str) -> None:
        ...


class _IOperationNodeInstructionsProxy:
    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IOperationNodeInstructions"

    @builtins.property
    @jsii.member(jsii_name="instructions")
    def instructions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instructions"))

    @instructions.setter
    def instructions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5029eec55150a99d387bd33a241844941678a723123f576ab5ca1dbe8560ac7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instructions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIndexInGraph")
    def node_index_in_graph(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeIndexInGraph"))

    @node_index_in_graph.setter
    def node_index_in_graph(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a691e85b135dcb7a3455055b40b75c9fd087eccfa1e4530a0d3b72f8779ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIndexInGraph", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeName"))

    @node_name.setter
    def node_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734c9db79aa3475cc0b924e42ac63aa8d52b10288609ab049f61de3218eb4e27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeName", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOperationNodeInstructions).__jsii_proxy_class__ = lambda : _IOperationNodeInstructionsProxy


@jsii.interface(jsii_type="xpander-sdk.IPGSchema")
class IPGSchema(typing_extensions.Protocol):
    '''Represents a schema group for a prompt group session (PGSchema), containing multiple node schemas.'''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="schemas")
    def schemas(self) -> typing.List[INodeSchema]:
        ...


class _IPGSchemaProxy:
    '''Represents a schema group for a prompt group session (PGSchema), containing multiple node schemas.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IPGSchema"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="schemas")
    def schemas(self) -> typing.List[INodeSchema]:
        return typing.cast(typing.List[INodeSchema], jsii.get(self, "schemas"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPGSchema).__jsii_proxy_class__ = lambda : _IPGSchemaProxy


@jsii.interface(jsii_type="xpander-sdk.ISourceNode")
class ISourceNode(typing_extensions.Protocol):
    '''Interface representing a source node in the agent's graph.'''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for the source node.'''
        ...

    @id.setter
    def id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Any:
        '''Metadata associated with the source node.'''
        ...

    @metadata.setter
    def metadata(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="pgSwitchAllowed")
    def pg_switch_allowed(self) -> builtins.bool:
        '''Flag indicating if switching prompt groups is allowed for this node.'''
        ...

    @pg_switch_allowed.setter
    def pg_switch_allowed(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.List[builtins.str]:
        '''List of target nodes connected to this source node.'''
        ...

    @targets.setter
    def targets(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceNodeType":
        '''Type of the source node (e.g., SDK, TASK).'''
        ...

    @type.setter
    def type(self, value: "SourceNodeType") -> None:
        ...


class _ISourceNodeProxy:
    '''Interface representing a source node in the agent's graph.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.ISourceNode"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for the source node.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6782cb166f668691a7b4be7b743380ed50722ee1549291808eee66d6a811fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Any:
        '''Metadata associated with the source node.'''
        return typing.cast(typing.Any, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf5d7d569b37ac0c974cabb49c4e85f99273856f9fc2bdac40d66bc3412561d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pgSwitchAllowed")
    def pg_switch_allowed(self) -> builtins.bool:
        '''Flag indicating if switching prompt groups is allowed for this node.'''
        return typing.cast(builtins.bool, jsii.get(self, "pgSwitchAllowed"))

    @pg_switch_allowed.setter
    def pg_switch_allowed(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ff19b4a8024e50148ba3c27b2519b80a78e68bd64da8c9b6837e86b5f0c4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgSwitchAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.List[builtins.str]:
        '''List of target nodes connected to this source node.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targets"))

    @targets.setter
    def targets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f4b1df8a6a0b38fd90f64ad03fcab2e6e4c28016977ac1461fc18c8a932c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceNodeType":
        '''Type of the source node (e.g., SDK, TASK).'''
        return typing.cast("SourceNodeType", jsii.get(self, "type"))

    @type.setter
    def type(self, value: "SourceNodeType") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0db8ab6f32bead8676f5d65edb0c8465aea43ef940f7b1d7b2ba9d2d577c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceNode).__jsii_proxy_class__ = lambda : _ISourceNodeProxy


@jsii.interface(jsii_type="xpander-sdk.ITool")
class ITool(typing_extensions.Protocol):
    '''Interface representing a general tool.'''

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''A description of the tool's functionality.'''
        ...

    @description.setter
    def description(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the tool.'''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="func")
    def func(self) -> typing.Any:
        '''Function to execute the tool's logic.'''
        ...

    @func.setter
    def func(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "IToolParameter"]]:
        '''Parameters required by the tool.'''
        ...

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, "IToolParameter"]],
    ) -> None:
        ...


class _IToolProxy:
    '''Interface representing a general tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.ITool"

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''A description of the tool's functionality.'''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f56ea2b548b4cdfe22f0f80bf2c3f88697c04aedd2bf7fe61755b4eb9cee55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5396ff1ffb06161e7b92840a35a663b1f418ffdcc7dde0e2593addf6ca31936a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="func")
    def func(self) -> typing.Any:
        '''Function to execute the tool's logic.'''
        return typing.cast(typing.Any, jsii.get(self, "func"))

    @func.setter
    def func(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682720a04a90eb0d29239c0baf8e36b53b239f76f1079edf9cd418a69ddb97ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "func", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "IToolParameter"]]:
        '''Parameters required by the tool.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "IToolParameter"]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, "IToolParameter"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf23d7676e5d1c7e307b10d99651d3e323b4741175a001eec3d04daa9f6a063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITool).__jsii_proxy_class__ = lambda : _IToolProxy


@jsii.interface(jsii_type="xpander-sdk.IToolCallPayload")
class IToolCallPayload(typing_extensions.Protocol):
    '''Interface representing the payload for a tool call.'''

    @builtins.property
    @jsii.member(jsii_name="bodyParams")
    def body_params(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Parameters for the request body.'''
        ...

    @body_params.setter
    def body_params(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Headers for the tool call request.'''
        ...

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="pathParams")
    def path_params(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Parameters for the URL path.'''
        ...

    @path_params.setter
    def path_params(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Parameters for the URL query string.'''
        ...

    @query_params.setter
    def query_params(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        ...


class _IToolCallPayloadProxy:
    '''Interface representing the payload for a tool call.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IToolCallPayload"

    @builtins.property
    @jsii.member(jsii_name="bodyParams")
    def body_params(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Parameters for the request body.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "bodyParams"))

    @body_params.setter
    def body_params(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9832f75123fcf9d9b942f4c173edc15dd68204b28ad5d4260488d6c5c649f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Headers for the tool call request.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a367c116b987fb49136a9814177e4d056c61593dd022f63355bb894da7fc9988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathParams")
    def path_params(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Parameters for the URL path.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "pathParams"))

    @path_params.setter
    def path_params(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e21845a97036e31f029489182b71f645274dafcc99c56e102732ed75019f377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Parameters for the URL query string.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "queryParams"))

    @query_params.setter
    def query_params(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893f015e220df05bf7b08ec5d24e2064db840604744494f599f33b596f114ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryParams", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IToolCallPayload).__jsii_proxy_class__ = lambda : _IToolCallPayloadProxy


@jsii.interface(jsii_type="xpander-sdk.IToolExecutionResult")
class IToolExecutionResult(typing_extensions.Protocol):
    '''Represents the result of a tool execution, including status, data, and success indicator.'''

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Any:
        ...

    @data.setter
    def data(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> builtins.bool:
        ...

    @is_success.setter
    def is_success(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        ...

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        ...


class _IToolExecutionResultProxy:
    '''Represents the result of a tool execution, including status, data, and success indicator.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IToolExecutionResult"

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45442afc737189c680b610029e36c0388f812ca6addfc20d90f2255236a7a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isSuccess"))

    @is_success.setter
    def is_success(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f354465848d57d08212584493a7b8ebb70e6a4185a12514d09d39089267cc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSuccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd332b88cb4f7bb75ce8e88200df9b702232ca7807d466896031bba1bac55a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IToolExecutionResult).__jsii_proxy_class__ = lambda : _IToolExecutionResultProxy


@jsii.interface(jsii_type="xpander-sdk.IToolInstructions")
class IToolInstructions(typing_extensions.Protocol):
    '''Interface representing instructions for a tool.'''

    @builtins.property
    @jsii.member(jsii_name="functionDescription")
    def function_description(self) -> builtins.str:
        '''Description of the tool's function.'''
        ...

    @function_description.setter
    def function_description(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Identifier for the tool.'''
        ...

    @id.setter
    def id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Parameters required by the tool.'''
        ...

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        ...


class _IToolInstructionsProxy:
    '''Interface representing instructions for a tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IToolInstructions"

    @builtins.property
    @jsii.member(jsii_name="functionDescription")
    def function_description(self) -> builtins.str:
        '''Description of the tool's function.'''
        return typing.cast(builtins.str, jsii.get(self, "functionDescription"))

    @function_description.setter
    def function_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdc5a25cd119bc40de0970a3da5a996792b481e3623e5692f2220f66858eaff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Identifier for the tool.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116d46c0c30294630e565344bb001679a311f6d4bdf7fde9def35de5f5e69bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Parameters required by the tool.'''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09181db93f9b9267ab92d06c025f7bac4699c1fdac9ca798c651a63559aa913f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IToolInstructions).__jsii_proxy_class__ = lambda : _IToolInstructionsProxy


@jsii.interface(jsii_type="xpander-sdk.IToolParameter")
class IToolParameter(typing_extensions.Protocol):
    '''Interface representing a parameter for a tool.'''

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, "IToolParameter"]:
        '''Properties of the parameter, if it is an object type.'''
        ...

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, "IToolParameter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the parameter (e.g., string, object).'''
        ...

    @type.setter
    def type(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of required properties within this parameter, if any.'''
        ...

    @required.setter
    def required(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IToolParameterProxy:
    '''Interface representing a parameter for a tool.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IToolParameter"

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, IToolParameter]:
        '''Properties of the parameter, if it is an object type.'''
        return typing.cast(typing.Mapping[builtins.str, IToolParameter], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, IToolParameter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187dae4a63a6fee1ee6e1cb395b2f91742bd245c20c13ab04570590726c5ef61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the parameter (e.g., string, object).'''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16039ce6185f742cd5865e412fc0342905a7a6d458331abeea0c8aea52fd0eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of required properties within this parameter, if any.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "required"))

    @required.setter
    def required(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b13164b7161ac045d14f7c4212e2fc304cf9b4c0234c2221c11807a860fee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IToolParameter).__jsii_proxy_class__ = lambda : _IToolParameterProxy


@jsii.interface(jsii_type="xpander-sdk.IXpanderClientCustomParams")
class IXpanderClientCustomParams(typing_extensions.Protocol):
    '''Interface representing optional custom parameters for configuring the xpanderAI client.'''

    @builtins.property
    @jsii.member(jsii_name="connectors")
    def connectors(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Optional array of connectors associated with the client.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> typing.Optional[builtins.str]:
        '''Optional organization ID associated with the client.'''
        ...


class _IXpanderClientCustomParamsProxy:
    '''Interface representing optional custom parameters for configuring the xpanderAI client.'''

    __jsii_type__: typing.ClassVar[str] = "xpander-sdk.IXpanderClientCustomParams"

    @builtins.property
    @jsii.member(jsii_name="connectors")
    def connectors(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Optional array of connectors associated with the client.'''
        return typing.cast(typing.Optional[typing.List[typing.Any]], jsii.get(self, "connectors"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> typing.Optional[builtins.str]:
        '''Optional organization ID associated with the client.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IXpanderClientCustomParams).__jsii_proxy_class__ = lambda : _IXpanderClientCustomParamsProxy


@jsii.enum(jsii_type="xpander-sdk.LLMProvider")
class LLMProvider(enum.Enum):
    '''Enum representing different Large Language Model (LLM) providers.

    This enum lists various LLM service providers integrated with xpanderAI, enabling
    selection of the desired LLM provider for specific tasks.
    '''

    LANG_CHAIN = "LANG_CHAIN"
    '''Represents the 'langchain' provider.'''
    OPEN_AI = "OPEN_AI"
    '''Represents the 'openai' provider.'''
    REAL_TIME_OPEN_AI = "REAL_TIME_OPEN_AI"
    '''Represents the 'openai' provider.'''
    NVIDIA_NIM = "NVIDIA_NIM"
    '''Represents the 'nvidiaNim' provider.'''
    AMAZON_BEDROCK = "AMAZON_BEDROCK"
    '''Represents the 'amazonBedrock' provider.'''
    OLLAMA = "OLLAMA"
    '''Represents the 'ollama' provider.'''
    FRIENDLI_AI = "FRIENDLI_AI"
    '''Represents the 'FriendliAI' provider.'''


class NvidiaNIMSupportedModels(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="xpander-sdk.NvidiaNIMSupportedModels",
):
    '''Contains constants representing various models supported by Nvidia NIM.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="LLAMA_3_1_70B_INSTRUCT")
    def LLAMA_3_1_70_B_INSTRUCT(cls) -> builtins.str:
        '''Meta Llama 3.1 70B Instruct model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "LLAMA_3_1_70B_INSTRUCT"))


class _NvidiaNIMSupportedModelsProxy(NvidiaNIMSupportedModels):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NvidiaNIMSupportedModels).__jsii_proxy_class__ = lambda : _NvidiaNIMSupportedModelsProxy


class OpenAISupportedModels(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="xpander-sdk.OpenAISupportedModels",
):
    '''Contains constants representing various models supported by OpenAI.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="GPT_4")
    def GPT_4(cls) -> builtins.str:
        '''OpenAI GPT-4 model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "GPT_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GPT_4_O")
    def GPT_4_O(cls) -> builtins.str:
        '''OpenAI GPT-4o model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "GPT_4_O"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GPT_4_O_MINI")
    def GPT_4_O_MINI(cls) -> builtins.str:
        '''OpenAI GPT-4o Mini model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "GPT_4_O_MINI"))


class _OpenAISupportedModelsProxy(OpenAISupportedModels):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, OpenAISupportedModels).__jsii_proxy_class__ = lambda : _OpenAISupportedModelsProxy


class PromptGroupSession(
    metaclass=jsii.JSIIMeta,
    jsii_type="xpander-sdk.PromptGroupSession",
):
    '''Represents a session within a prompt group in xpanderAI, managing the graph item and tracking the last processed node.'''

    def __init__(
        self,
        pg: IGraphItem,
        last_node: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pg: The graph item associated with the prompt group session.
        :param last_node: Identifier for the last node accessed in the session.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5b89168bd30319b7dbf2cd29845dadc5a899be20dfb299d48ff8e8c473f752)
            check_type(argname="argument pg", value=pg, expected_type=type_hints["pg"])
            check_type(argname="argument last_node", value=last_node, expected_type=type_hints["last_node"])
        jsii.create(self.__class__, self, [pg, last_node])

    @builtins.property
    @jsii.member(jsii_name="lastNode")
    def last_node(self) -> builtins.str:
        '''Identifier for the last node accessed in the session.'''
        return typing.cast(builtins.str, jsii.get(self, "lastNode"))

    @last_node.setter
    def last_node(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d006c5bddd9b020c15566de3c68941f0760179055722e8e575c2960f018fe6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pg")
    def pg(self) -> IGraphItem:
        '''The graph item associated with the prompt group session.'''
        return typing.cast(IGraphItem, jsii.get(self, "pg"))

    @pg.setter
    def pg(self, value: IGraphItem) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a10ccd81f1f207caf8c9b067806e95f3d700d627555c0540cecd5fd05a845aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pg", value) # pyright: ignore[reportArgumentType]


class PromptGroupSessionsList(
    metaclass=jsii.JSIIMeta,
    jsii_type="xpander-sdk.PromptGroupSessionsList",
):
    '''Manages a collection of prompt group sessions, providing functionalities to start, manage, and retrieve tools for active sessions in xpanderAI.'''

    def __init__(
        self,
        graphs: typing.Sequence[IGraphItem],
        pg_oas: typing.Sequence[IAgentTool],
        sessions: typing.Optional[typing.Sequence[PromptGroupSession]] = None,
    ) -> None:
        '''
        :param graphs: Collection of graph items associated with prompt groups.
        :param pg_oas: Array of agent tools specific to prompt groups.
        :param sessions: List of active prompt group sessions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6fbc4d3e6e94e025105c39a10374eaf47be2eae03255e73531b6b7a8a9494a)
            check_type(argname="argument graphs", value=graphs, expected_type=type_hints["graphs"])
            check_type(argname="argument pg_oas", value=pg_oas, expected_type=type_hints["pg_oas"])
            check_type(argname="argument sessions", value=sessions, expected_type=type_hints["sessions"])
        jsii.create(self.__class__, self, [graphs, pg_oas, sessions])

    @jsii.member(jsii_name="getToolsForActiveSession")
    def get_tools_for_active_session(
        self,
        all_tools: typing.Sequence[typing.Any],
    ) -> typing.List[typing.Any]:
        '''Retrieves the available tools for the currently active session, filtering tools based on their position in the graph and local tool prefix.

        :param all_tools: - A list of all tools available for the session.

        :return: A filtered list of tools available for the active session.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c422d3dabe9ef8abba2c3bbbd65cb211404930f96fa869276b763d0a958241a3)
            check_type(argname="argument all_tools", value=all_tools, expected_type=type_hints["all_tools"])
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "getToolsForActiveSession", [all_tools]))

    @jsii.member(jsii_name="resetSessions")
    def reset_sessions(self) -> None:
        '''Resets all active prompt group sessions.'''
        return typing.cast(None, jsii.invoke(self, "resetSessions", []))

    @jsii.member(jsii_name="startPgSession")
    def start_pg_session(self, tool: "ToolCall") -> builtins.str:
        '''Starts a new session for a specified tool call, associating it with a prompt group.

        If the prompt group or graph cannot be matched, an error is thrown.

        :param tool: - The tool call used to start the prompt group session.

        :return: A system message indicating the prompt group was successfully selected.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be23542c51313e85e41f7c13dc0faa8e100ea059aa4042e725c2259b23797102)
            check_type(argname="argument tool", value=tool, expected_type=type_hints["tool"])
        return typing.cast(builtins.str, jsii.invoke(self, "startPgSession", [tool]))

    @builtins.property
    @jsii.member(jsii_name="activeSession")
    def active_session(self) -> PromptGroupSession:
        '''Returns the currently active session, if one exists.'''
        return typing.cast(PromptGroupSession, jsii.get(self, "activeSession"))

    @builtins.property
    @jsii.member(jsii_name="pgOas")
    def pg_oas(self) -> typing.List[IAgentTool]:
        '''Array of agent tools specific to prompt groups.'''
        return typing.cast(typing.List[IAgentTool], jsii.get(self, "pgOas"))

    @pg_oas.setter
    def pg_oas(self, value: typing.List[IAgentTool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dffcbbe7fe24829d0eac81f8a4e4a405acfb409cd895f58abf92291feb457c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgOas", value) # pyright: ignore[reportArgumentType]


class RealTimeOpenAISupportedModels(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="xpander-sdk.RealTimeOpenAISupportedModels",
):
    '''Contains constants representing various models supported by OpenAI.

    :remarks:

    This abstract class defines static constants for the supported models
    by xpanderAI's OpenAI real-time integrations.
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="GPT_4_O_AUDIO_PREVIEW")
    def GPT_4_O_AUDIO_PREVIEW(cls) -> builtins.str:
        '''OpenAI GPT-4o Audio Preview model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "GPT_4_O_AUDIO_PREVIEW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GPT_4_O_REALTIME_PREVIEW")
    def GPT_4_O_REALTIME_PREVIEW(cls) -> builtins.str:
        '''OpenAI GPT-4o Realtime Preview model.'''
        return typing.cast(builtins.str, jsii.sget(cls, "GPT_4_O_REALTIME_PREVIEW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WHISPER_1")
    def WHISPER_1(cls) -> builtins.str:
        '''OpenAI Whisper model for speech-to-text tasks.'''
        return typing.cast(builtins.str, jsii.sget(cls, "WHISPER_1"))


class _RealTimeOpenAISupportedModelsProxy(RealTimeOpenAISupportedModels):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, RealTimeOpenAISupportedModels).__jsii_proxy_class__ = lambda : _RealTimeOpenAISupportedModelsProxy


@jsii.enum(jsii_type="xpander-sdk.SourceNodeType")
class SourceNodeType(enum.Enum):
    '''Enum representing different source node types for agents.'''

    SDK = "SDK"
    TASK = "TASK"
    ASSISTANT = "ASSISTANT"
    WEBHOOK = "WEBHOOK"


class ToolCall(Base, metaclass=jsii.JSIIMeta, jsii_type="xpander-sdk.ToolCall"):
    def __init__(
        self,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional["ToolCallType"] = None,
        payload: typing.Any = None,
        tool_call_id: typing.Optional[builtins.str] = None,
        is_pg: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: -
        :param type: -
        :param payload: -
        :param tool_call_id: -
        :param is_pg: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b1512c48e4c0a4b618d417e46f7c83b02989356f2412aa0eae9d63b626ce0e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument tool_call_id", value=tool_call_id, expected_type=type_hints["tool_call_id"])
            check_type(argname="argument is_pg", value=is_pg, expected_type=type_hints["is_pg"])
        jsii.create(self.__class__, self, [name, type, payload, tool_call_id, is_pg])

    @builtins.property
    @jsii.member(jsii_name="isPg")
    def is_pg(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isPg"))

    @is_pg.setter
    def is_pg(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca5092cdc5afd247201929b020a5a265e0bad7897d1e22e4b133be3ae8295bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPg", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7cce041752b4e95ae25466ea39d32f51ec0301e64015b66ccf20bb9b23db25e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1940e09fdc14592acfce7003f99bcc770eb4b17ea62e53e30d6cbfd4d3d3707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="toolCallId")
    def tool_call_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "toolCallId"))

    @tool_call_id.setter
    def tool_call_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d9b994824033489cb2b3b806044405bcb06c1d72048f017c89bb422b16b35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolCallId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "ToolCallType":
        return typing.cast("ToolCallType", jsii.get(self, "type"))

    @type.setter
    def type(self, value: "ToolCallType") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2059ec549c7384dd73be7be379faf6256c60a8ec7b55fdb9082692bbdc4bac54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


class ToolCallResult(
    Base,
    metaclass=jsii.JSIIMeta,
    jsii_type="xpander-sdk.ToolCallResult",
):
    def __init__(
        self,
        function_name: typing.Optional[builtins.str] = None,
        tool_call_id: typing.Optional[builtins.str] = None,
        payload: typing.Any = None,
        status_code: typing.Optional[jsii.Number] = None,
        result: typing.Any = None,
        is_success: typing.Optional[builtins.bool] = None,
        is_error: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param function_name: -
        :param tool_call_id: -
        :param payload: -
        :param status_code: -
        :param result: -
        :param is_success: -
        :param is_error: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2debc725768136a46976eacab873877fdcc3efbb47c357e0973193213896e283)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument tool_call_id", value=tool_call_id, expected_type=type_hints["tool_call_id"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument result", value=result, expected_type=type_hints["result"])
            check_type(argname="argument is_success", value=is_success, expected_type=type_hints["is_success"])
            check_type(argname="argument is_error", value=is_error, expected_type=type_hints["is_error"])
        jsii.create(self.__class__, self, [function_name, tool_call_id, payload, status_code, result, is_success, is_error])

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fffc9823e52bc6b5b2f4aa72f7ed94614aad7d55b77f29de8574547aa73f28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isError")
    def is_error(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isError"))

    @is_error.setter
    def is_error(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12e85757c6557cdf77248e76a660df04102b8873b38236827fb882d1fa6439a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isSuccess"))

    @is_success.setter
    def is_success(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0ae8339ae925874f36d96caaf593a776e69a5def415e6cd597660d7e9c011e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSuccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2de087a3432f7b811bf4e98dd110380b61cb2d0cdcd014af55ea9c493c5e516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "result"))

    @result.setter
    def result(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b512e8cc2e3d13362bf29e552b8dff26b147cd4cf7b3fc2ac09efd5bd6e5bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "result", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7de4c43b1bcc39cb1dbd154a581a3c2a35f429555b50d12f81d0c6662c787a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="toolCallId")
    def tool_call_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "toolCallId"))

    @tool_call_id.setter
    def tool_call_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e548be6ee41a966ad4e21e38458b2dc18fde679b9017e65e4f088b5b0d8c3580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolCallId", value) # pyright: ignore[reportArgumentType]


@jsii.enum(jsii_type="xpander-sdk.ToolCallType")
class ToolCallType(enum.Enum):
    '''Enum representing types of tool calls.'''

    XPANDER = "XPANDER"
    LOCAL = "LOCAL"


class XpanderClient(metaclass=jsii.JSIIMeta, jsii_type="xpander-sdk.XpanderClient"):
    '''XpanderClient provides methods for configuring and interacting with xpanderAI tools, managing agents, and extracting tool calls from LLM responses.'''

    def __init__(
        self,
        api_key: builtins.str,
        base_url: typing.Any = None,
        with_metrics_report: typing.Optional[builtins.bool] = None,
        custom_params: typing.Any = None,
    ) -> None:
        '''Constructs a new XpanderClient instance.

        :param api_key: -
        :param base_url: -
        :param with_metrics_report: -
        :param custom_params: -

        :throws: Will throw an error if an invalid API key is specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ada04f0df01e9b462e0b973aee5f69eda17ab0f22e7345f33423f0acca9ad36)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument with_metrics_report", value=with_metrics_report, expected_type=type_hints["with_metrics_report"])
            check_type(argname="argument custom_params", value=custom_params, expected_type=type_hints["custom_params"])
        jsii.create(self.__class__, self, [api_key, base_url, with_metrics_report, custom_params])

    @jsii.member(jsii_name="extractToolCalls")
    @builtins.classmethod
    def extract_tool_calls(
        cls,
        llm_response: typing.Any,
        llm_provider: typing.Optional[LLMProvider] = None,
    ) -> typing.List[ToolCall]:
        '''Extracts tool calls from an LLM response based on the specified LLM provider.

        :param llm_response: - The LLM response to analyze for tool calls.
        :param llm_provider: - The LLM provider, defaults to OPEN_AI.

        :return: An array of tool calls extracted from the LLM response.

        :throws: Error if the specified LLM provider is not supported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89a5c88d1a2ed62ab765c38358d4adda81980f27657e34b4fe23fc61eca9217)
            check_type(argname="argument llm_response", value=llm_response, expected_type=type_hints["llm_response"])
            check_type(argname="argument llm_provider", value=llm_provider, expected_type=type_hints["llm_provider"])
        return typing.cast(typing.List[ToolCall], jsii.sinvoke(cls, "extractToolCalls", [llm_response, llm_provider]))

    @builtins.property
    @jsii.member(jsii_name="agents")
    def agents(self) -> Agents:
        '''Instance of Agents to manage xpanderAI agents.'''
        return typing.cast(Agents, jsii.get(self, "agents"))

    @agents.setter
    def agents(self, value: Agents) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50de96ce44613a7f9044134d55c384c9cbc69918873535eed55a2d9c1f2cafbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> Configuration:
        '''Configuration settings for the xpanderAI client.'''
        return typing.cast(Configuration, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: Configuration) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f24bf46a0a96d6e069bcfdce151aa22264da15a80125c376dbad457bf91d1c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]


class Agent(Base, metaclass=jsii.JSIIMeta, jsii_type="xpander-sdk.Agent"):
    '''Represents an agent in xpanderAI, managing the tools, sessions, and operations associated with the agent.

    This class enables loading agents, handling tool executions,
    and managing prompt group sessions.
    '''

    def __init__(
        self,
        configuration: Configuration,
        id: builtins.str,
        organization_id: builtins.str,
        status: AgentStatus,
        name: builtins.str,
        source_nodes: typing.Sequence[ISourceNode],
        pg_switch_allowed: typing.Optional[builtins.bool] = None,
        tools: typing.Optional[typing.Sequence[IAgentTool]] = None,
        graphs: typing.Optional[typing.Sequence[IGraphItem]] = None,
        pg_oas: typing.Optional[typing.Sequence[IAgentTool]] = None,
        auto_load: typing.Optional[builtins.bool] = None,
        pg_schemas: typing.Optional[typing.Sequence[IPGSchema]] = None,
        pg_node_description_override: typing.Optional[typing.Sequence[INodeDescription]] = None,
        general_instructions: typing.Optional[builtins.str] = None,
        judge_instructions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param configuration: Configuration settings for the agent.
        :param id: Unique identifier for the agent.
        :param organization_id: Organization ID to which the agent belongs.
        :param status: Current status of the agent.
        :param name: Human-readable name of the agent.
        :param source_nodes: List of source nodes associated with the agent.
        :param pg_switch_allowed: Whether prompt group switching is allowed for the agent.
        :param tools: Array of tools available to the agent.
        :param graphs: Array of graph items related to the agent.
        :param pg_oas: Array of agent tools specific to prompt groups.
        :param auto_load: Whether the agent should automatically load its resources.
        :param pg_schemas: Array of agent tools specific to prompt groups.
        :param pg_node_description_override: Array of agent tools specific to prompt groups.
        :param general_instructions: -
        :param judge_instructions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3ca6ba27cec860aa869deb2eaf5d80822747214c50652c074c1fd995c12295)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_nodes", value=source_nodes, expected_type=type_hints["source_nodes"])
            check_type(argname="argument pg_switch_allowed", value=pg_switch_allowed, expected_type=type_hints["pg_switch_allowed"])
            check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
            check_type(argname="argument graphs", value=graphs, expected_type=type_hints["graphs"])
            check_type(argname="argument pg_oas", value=pg_oas, expected_type=type_hints["pg_oas"])
            check_type(argname="argument auto_load", value=auto_load, expected_type=type_hints["auto_load"])
            check_type(argname="argument pg_schemas", value=pg_schemas, expected_type=type_hints["pg_schemas"])
            check_type(argname="argument pg_node_description_override", value=pg_node_description_override, expected_type=type_hints["pg_node_description_override"])
            check_type(argname="argument general_instructions", value=general_instructions, expected_type=type_hints["general_instructions"])
            check_type(argname="argument judge_instructions", value=judge_instructions, expected_type=type_hints["judge_instructions"])
        jsii.create(self.__class__, self, [configuration, id, organization_id, status, name, source_nodes, pg_switch_allowed, tools, graphs, pg_oas, auto_load, pg_schemas, pg_node_description_override, general_instructions, judge_instructions])

    @jsii.member(jsii_name="addLocalTools")
    def add_local_tools(
        self,
        tools: typing.Union[typing.Sequence[typing.Any], typing.Sequence[ILocalTool]],
    ) -> None:
        '''Adds local tools to the agent with prefixed function names.

        :param tools: - The list of local tools to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a4e9d238bcd6575542fe126282fe717dabbed97bd4b5d5f0906439f6debd49)
            check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
        return typing.cast(None, jsii.invoke(self, "addLocalTools", [tools]))

    @jsii.member(jsii_name="getTools")
    def get_tools(
        self,
        llm_provider: typing.Optional[LLMProvider] = None,
        return_all_tools: typing.Optional[builtins.bool] = None,
    ) -> typing.List[typing.Any]:
        '''Retrieves tools compatible with the specified LLM provider.

        :param llm_provider: - The LLM provider to filter tools by.
        :param return_all_tools: -

        :return: A list of tools that match the specified provider.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773e3afa26f8b79fe00973c69c9983fbf523bfd2f52c02c0a473df8878934452)
            check_type(argname="argument llm_provider", value=llm_provider, expected_type=type_hints["llm_provider"])
            check_type(argname="argument return_all_tools", value=return_all_tools, expected_type=type_hints["return_all_tools"])
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "getTools", [llm_provider, return_all_tools]))

    @jsii.member(jsii_name="load")
    def load(self, source_node_type: typing.Optional[SourceNodeType] = None) -> None:
        '''Loads the agent data from the specified source node type.

        :param source_node_type: - The type of source node to load.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083e27f1b35697c0dc5dd7bec052ea93d4a2fd3d2ee05d66ed6dfd7754537ddb)
            check_type(argname="argument source_node_type", value=source_node_type, expected_type=type_hints["source_node_type"])
        return typing.cast(None, jsii.invoke(self, "load", [source_node_type]))

    @jsii.member(jsii_name="retrieveAllGraphTools")
    def retrieve_all_graph_tools(
        self,
        llm_provider: typing.Optional[LLMProvider] = None,
    ) -> typing.List[typing.Any]:
        '''
        :param llm_provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8585cd601813225ff26808de89a1760108cbe32a7c1faf0681da25145fd71d1)
            check_type(argname="argument llm_provider", value=llm_provider, expected_type=type_hints["llm_provider"])
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "retrieveAllGraphTools", [llm_provider]))

    @jsii.member(jsii_name="runTool")
    def run_tool(
        self,
        tool: ToolCall,
        payload_extension: typing.Any = None,
    ) -> ToolCallResult:
        '''Executes a single tool call and returns the result.

        :param tool: - The tool call to execute.
        :param payload_extension: -

        :return: The result of the tool execution.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1ca0e533f7a6dc6cf8465ad7809ba4a450abee064ca45429a80a258a5e2e65)
            check_type(argname="argument tool", value=tool, expected_type=type_hints["tool"])
            check_type(argname="argument payload_extension", value=payload_extension, expected_type=type_hints["payload_extension"])
        return typing.cast(ToolCallResult, jsii.invoke(self, "runTool", [tool, payload_extension]))

    @jsii.member(jsii_name="runTools")
    def run_tools(
        self,
        tool_calls: typing.Sequence[ToolCall],
        payload_extension: typing.Any = None,
    ) -> typing.List[ToolCallResult]:
        '''Executes multiple tool calls sequentially and returns their results.

        :param tool_calls: - The list of tool calls to execute.
        :param payload_extension: -

        :return: A list of results for each tool execution.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307c287f13e8189f59310f2e5a43f33ebb271c35e1502a531966c06bbe13ef32)
            check_type(argname="argument tool_calls", value=tool_calls, expected_type=type_hints["tool_calls"])
            check_type(argname="argument payload_extension", value=payload_extension, expected_type=type_hints["payload_extension"])
        return typing.cast(typing.List[ToolCallResult], jsii.invoke(self, "runTools", [tool_calls, payload_extension]))

    @jsii.member(jsii_name="schemasByNodeName")
    def schemas_by_node_name(self) -> typing.Mapping[builtins.str, INodeSchema]:
        '''Retrieves schemas grouped by node name based on the active prompt group session.

        This method returns an object where each key is a node name, and the value is the corresponding schema.
        It ensures that schemas are only fetched if there is an active session with a valid ``promptGroupId``
        and if ``pgSchemas`` is not empty.

        :return: A record of schemas indexed by their node name, or an empty object if conditions are not met.
        '''
        return typing.cast(typing.Mapping[builtins.str, INodeSchema], jsii.invoke(self, "schemasByNodeName", []))

    @jsii.member(jsii_name="selectPromptGroup")
    def select_prompt_group(self, prompt_group_name: builtins.str) -> None:
        '''
        :param prompt_group_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa4e5a49bb8271c31eb566a9a8225672df671cea13eeb9e9905e74babd69207)
            check_type(argname="argument prompt_group_name", value=prompt_group_name, expected_type=type_hints["prompt_group_name"])
        return typing.cast(None, jsii.invoke(self, "selectPromptGroup", [prompt_group_name]))

    @builtins.property
    @jsii.member(jsii_name="hasLocalTools")
    def has_local_tools(self) -> builtins.bool:
        '''Checks if the agent has any local tools loaded.'''
        return typing.cast(builtins.bool, jsii.get(self, "hasLocalTools"))

    @builtins.property
    @jsii.member(jsii_name="isCustom")
    def is_custom(self) -> builtins.bool:
        '''Checks if the agent is a custom-defined agent.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCustom"))

    @builtins.property
    @jsii.member(jsii_name="sourceNodeType")
    def source_node_type(self) -> SourceNodeType:
        '''Retrieves the type of source node for the agent.'''
        return typing.cast(SourceNodeType, jsii.get(self, "sourceNodeType"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''Constructs the API URL for this agent.'''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> Configuration:
        '''Configuration settings for the agent.'''
        return typing.cast(Configuration, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: Configuration) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2acddc917b6b415bc14dfb9a7094cbd1b0319e93c3c4b3298f8cb5d9ec8206a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generalInstructions")
    def general_instructions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generalInstructions"))

    @general_instructions.setter
    def general_instructions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9976a447b388116d636066c048c970ab1f17c82f976d03a7ec90ffc1a1b6a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generalInstructions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="graphs")
    def graphs(self) -> typing.List[IGraphItem]:
        '''Array of graph items related to the agent.'''
        return typing.cast(typing.List[IGraphItem], jsii.get(self, "graphs"))

    @graphs.setter
    def graphs(self, value: typing.List[IGraphItem]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0a173561a6fcf731927ebbb3416e3e62701420fb7b719b46c04620b077300e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for the agent.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b9d8c488cea43db21adbef0723558d2e632d07b3f9134efdeb872de791fa1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="judgeInstructions")
    def judge_instructions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "judgeInstructions"))

    @judge_instructions.setter
    def judge_instructions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c8947d898e59570c44266cf149a9dc66dd2058cb95225c8af2063652d876a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "judgeInstructions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localTools")
    def local_tools(self) -> typing.List[ILocalTool]:
        '''Collection of local tools specific to this agent.'''
        return typing.cast(typing.List[ILocalTool], jsii.get(self, "localTools"))

    @local_tools.setter
    def local_tools(self, value: typing.List[ILocalTool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc78718c4e88ad0687034fec3393a9b0dd4518c626fe4c60d2244cefaadbe37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localTools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Human-readable name of the agent.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22da1a47b30804817cea4f52e46761946f71d0d3436d3236d8ab8bbd3f9a2364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        '''Organization ID to which the agent belongs.'''
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @organization_id.setter
    def organization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b78331aeaf11efbf7d44a1bd4ce9783ac8b3be074090b3f146520a09bb2ff99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originalToolNamesReMapping")
    def _original_tool_names_re_mapping(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Maps original tool names to renamed versions for consistency.'''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "originalToolNamesReMapping"))

    @_original_tool_names_re_mapping.setter
    def _original_tool_names_re_mapping(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6762bda91838241a6ee34d79cd8660a8ecf1de3ef553cabb0bd5130090bc15a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originalToolNamesReMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pgNodeDescriptionOverride")
    def pg_node_description_override(self) -> typing.List[INodeDescription]:
        '''Array of agent tools specific to prompt groups.'''
        return typing.cast(typing.List[INodeDescription], jsii.get(self, "pgNodeDescriptionOverride"))

    @pg_node_description_override.setter
    def pg_node_description_override(
        self,
        value: typing.List[INodeDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62cf407b75bf35549e026b2eb3b2137665e585c1e08b5b490e8bbd6f09edd2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgNodeDescriptionOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pgOas")
    def pg_oas(self) -> typing.List[IAgentTool]:
        '''Array of agent tools specific to prompt groups.'''
        return typing.cast(typing.List[IAgentTool], jsii.get(self, "pgOas"))

    @pg_oas.setter
    def pg_oas(self, value: typing.List[IAgentTool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c521ac8a0b5aa23bc0f993a5766f3392fb2d55936c5685fa6cd3639bf4ddb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgOas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pgSchemas")
    def pg_schemas(self) -> typing.List[IPGSchema]:
        '''Array of agent tools specific to prompt groups.'''
        return typing.cast(typing.List[IPGSchema], jsii.get(self, "pgSchemas"))

    @pg_schemas.setter
    def pg_schemas(self, value: typing.List[IPGSchema]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d25a9906544708d29f756b9d05b5c9086454a6e860208533e7f3b2df5c67ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgSchemas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pgSwitchAllowed")
    def pg_switch_allowed(self) -> builtins.bool:
        '''Whether prompt group switching is allowed for the agent.'''
        return typing.cast(builtins.bool, jsii.get(self, "pgSwitchAllowed"))

    @pg_switch_allowed.setter
    def pg_switch_allowed(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae13b705d7d8977c7d3ad122cb11bb833d5688df9b90b593297a9976411d11b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgSwitchAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptGroupSessions")
    def prompt_group_sessions(self) -> PromptGroupSessionsList:
        '''Manages prompt group sessions for this agent.'''
        return typing.cast(PromptGroupSessionsList, jsii.get(self, "promptGroupSessions"))

    @prompt_group_sessions.setter
    def prompt_group_sessions(self, value: PromptGroupSessionsList) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7c66cd0fc6261d32287e8f4fbf7a0ee65a2f7d77886ad120d893353ebbe709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptGroupSessions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ready")
    def ready(self) -> builtins.bool:
        '''Indicates whether the agent is ready with tools loaded.'''
        return typing.cast(builtins.bool, jsii.get(self, "ready"))

    @ready.setter
    def ready(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bc6384ff613546183aa4186ddfac11deaaf2c2b3c4f43fd64f205dee4ad649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ready", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNodes")
    def source_nodes(self) -> typing.List[ISourceNode]:
        '''List of source nodes associated with the agent.'''
        return typing.cast(typing.List[ISourceNode], jsii.get(self, "sourceNodes"))

    @source_nodes.setter
    def source_nodes(self, value: typing.List[ISourceNode]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1dff1fd2031b8c10437260cbaae7a1861611afa24cb0ca6b7126c825461d0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> AgentStatus:
        '''Current status of the agent.'''
        return typing.cast(AgentStatus, jsii.get(self, "status"))

    @status.setter
    def status(self, value: AgentStatus) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f657c5abb4af14138072346cc87aee77138c4171cd0fc2bf21f903fd6c6299ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tools")
    def tools(self) -> typing.List[IAgentTool]:
        '''Array of tools available to the agent.'''
        return typing.cast(typing.List[IAgentTool], jsii.get(self, "tools"))

    @tools.setter
    def tools(self, value: typing.List[IAgentTool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d712115a2ab298e5d50d49c632fab67794a7409f1db441e663ee069fabba3ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tools", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Agent",
    "AgentStatus",
    "Agents",
    "AmazonBedrockSupportedModels",
    "Base",
    "Configuration",
    "FriendliAISupportedModels",
    "IAgentTool",
    "IBedrockTool",
    "IBedrockToolOutput",
    "IBedrockToolSpec",
    "IBedrockToolSpecInputSchema",
    "IConfiguration",
    "IGraphItem",
    "ILocalTool",
    "ILocalToolFunction",
    "INodeDescription",
    "INodeSchema",
    "IOpenAIToolFunctionOutput",
    "IOpenAIToolOutput",
    "IOperationNodeInstructions",
    "IPGSchema",
    "ISourceNode",
    "ITool",
    "IToolCallPayload",
    "IToolExecutionResult",
    "IToolInstructions",
    "IToolParameter",
    "IXpanderClientCustomParams",
    "LLMProvider",
    "NvidiaNIMSupportedModels",
    "OpenAISupportedModels",
    "PromptGroupSession",
    "PromptGroupSessionsList",
    "RealTimeOpenAISupportedModels",
    "SourceNodeType",
    "ToolCall",
    "ToolCallResult",
    "ToolCallType",
    "XpanderClient",
]

publication.publish()

def _typecheckingstub__56c927c42c835c774c6f5f1f6f97fed3b3214baccc5c46df58f7f5cf97262992(
    configuration: Configuration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb382a0499d6ff9252ba35bb8f4c90a05697129cfe9cad98a7f8a1a14da8e1d4(
    agent_id: builtins.str,
    source_node_type: typing.Optional[SourceNodeType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2dae6950d6e1716f079e39f5f02b0b55d94d51d936cd9d0017bfc2c7e8a7109(
    source_node_type: typing.Optional[SourceNodeType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea39ecf496725a5bdaabe40097604046c959e93c71defecacfbe7b2ca0b8d98(
    refetch: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f37932ab42616ef0215f3190c6c4bfa79237ec478d6c77803ea5cc9260af1f3(
    value: typing.List[Agent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4b41eaf57993f4b49ed6bc9995e9ed9fa2685fb355f0d948717f7ea7e34c2f(
    value: Configuration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dab3da5f8c0475ccab1873969e148ad9dcbdb0ddf88c9ecc6b02b751238b6e5(
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4d603584cc9880629c407e84565dc862d0614d798748f7556e51d6023943cb(
    data: typing.Mapping[typing.Any, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafae5b4445df1b4c673783f144d770b151e831e63bc8be999b4708f966d5caa(
    __0: IConfiguration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135b56998170832cdd7296e91cdddd9c57d7b17d36e505bee4468b800785e5a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6025924c03e9981cc1b85f95320de6d369f9970a79f6ee17298111769cddfa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57aadab9068339b18a9a9bd0a0c861024d57eee8e2450a27a4cf5da13f417253(
    value: IXpanderClientCustomParams,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66c1cb417d578246e8364e66bde633c4843b6604b43b28c0a1768e3d971c32a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013ed94cf5075f5bf0c5bc74a0e8036501c284d35e4392ea6f15080eddc2a7ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b25237ddc5e6038acd2ee375459e97263388f5a79c9b19df1509b8ad33817e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba86af1a111c4132196288035231114364f7fd5846ba31b895e28cf0263f6b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd4d28b7b8f38ee90640906c0dfa66779e13f1537479bfac62236199af53599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb31aa04b21eb4806b8482aa225a11b478a08f9a3d8fe6ed1ff02f818c62244(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7629b10507753cd17f8a141e1f5acf42aa3ad6279b11466521e8e879158f1c0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1639f3cf0ce4876316784b66d4eb55d50082b87dcaa56347a0ebcb4c5be615(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76420473c4800542a5c924d1375223fda76771d1a194354c646c87a134351b2d(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d18303f76ca1cea7f0333afa6e171a5ff4c99c53601d4772e5d916b00ae6de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686bee2f9cc4cb8e5e46bd20309c912c48752fa01feec49d211288fe414d9879(
    value: IBedrockToolSpec,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50442d45bad8e7fa927b6be3feac263e79712091c62056e831a391b5a17c13bc(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab15f7ad29e9cbdf37869d4d12b1eca4937a0130eb1409bb74f1149d0dfc26b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dfbf6fa195f65cf55b428cbf9c7e700af738bcd9c47ebdda318cfedf78e70a(
    value: IBedrockToolSpecInputSchema,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0534d2b1daae9caffc87b99f4b6cc09e1a9eac3888374c04e9c619375c2f1b35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1454322c6f1b39bdf36a5d88226526fce2d55d1e13ada58cf00d44f12fd64366(
    value: typing.Mapping[builtins.str, IToolParameter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e8b15e3c3381cc6704c1ee29aa4c16d1b4a86e2ac011b6e441b3e0b431f930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83454a3c655acd05227e58cd1768d64624b4c0ca0c928ab30fe2d5404c1c20a(
    value: IXpanderClientCustomParams,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a526e81165d7b0acee70572029a007577d042379f52fcd7844f14a292ff14e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1540b2d417df65eae973c655ee643690a0dcd51cb4e6c7e9d779c317f9cec97a(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dac3f67c0f52d800dcd097be9ddb6eb98f70c71ea8289dbaad0e94a58d47f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cbdb3cb6871f560d5a0a78bd2ceff7528297ba8da6e71aa3da216d1c0284f2(
    value: typing.Mapping[builtins.str, typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa5a9bfea7b1902145aadecc5674d2699888d69e501b26b8c8c3ad694675881(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a9c3fc5cff09316502fc55db2175287af1ef6831a515963059bd6de019711a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c77329d9ea483c6111ccb444f6e30c3a08d7baf27c81a55cc015bb38ed9369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6269099b38fe2e344fbcf8d67e4d22c04f53523963a6b49a82311bfff413a54b(
    value: typing.Optional[typing.List[IOperationNodeInstructions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5029eec55150a99d387bd33a241844941678a723123f576ab5ca1dbe8560ac7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a691e85b135dcb7a3455055b40b75c9fd087eccfa1e4530a0d3b72f8779ae8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734c9db79aa3475cc0b924e42ac63aa8d52b10288609ab049f61de3218eb4e27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6782cb166f668691a7b4be7b743380ed50722ee1549291808eee66d6a811fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf5d7d569b37ac0c974cabb49c4e85f99273856f9fc2bdac40d66bc3412561d(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ff19b4a8024e50148ba3c27b2519b80a78e68bd64da8c9b6837e86b5f0c4e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f4b1df8a6a0b38fd90f64ad03fcab2e6e4c28016977ac1461fc18c8a932c1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0db8ab6f32bead8676f5d65edb0c8465aea43ef940f7b1d7b2ba9d2d577c39(
    value: SourceNodeType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f56ea2b548b4cdfe22f0f80bf2c3f88697c04aedd2bf7fe61755b4eb9cee55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5396ff1ffb06161e7b92840a35a663b1f418ffdcc7dde0e2593addf6ca31936a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682720a04a90eb0d29239c0baf8e36b53b239f76f1079edf9cd418a69ddb97ac(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf23d7676e5d1c7e307b10d99651d3e323b4741175a001eec3d04daa9f6a063(
    value: typing.Optional[typing.Mapping[builtins.str, IToolParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9832f75123fcf9d9b942f4c173edc15dd68204b28ad5d4260488d6c5c649f9e(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a367c116b987fb49136a9814177e4d056c61593dd022f63355bb894da7fc9988(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e21845a97036e31f029489182b71f645274dafcc99c56e102732ed75019f377(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893f015e220df05bf7b08ec5d24e2064db840604744494f599f33b596f114ee0(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45442afc737189c680b610029e36c0388f812ca6addfc20d90f2255236a7a1d(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f354465848d57d08212584493a7b8ebb70e6a4185a12514d09d39089267cc34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd332b88cb4f7bb75ce8e88200df9b702232ca7807d466896031bba1bac55a15(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdc5a25cd119bc40de0970a3da5a996792b481e3623e5692f2220f66858eaff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116d46c0c30294630e565344bb001679a311f6d4bdf7fde9def35de5f5e69bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09181db93f9b9267ab92d06c025f7bac4699c1fdac9ca798c651a63559aa913f(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187dae4a63a6fee1ee6e1cb395b2f91742bd245c20c13ab04570590726c5ef61(
    value: typing.Mapping[builtins.str, IToolParameter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16039ce6185f742cd5865e412fc0342905a7a6d458331abeea0c8aea52fd0eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b13164b7161ac045d14f7c4212e2fc304cf9b4c0234c2221c11807a860fee0(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5b89168bd30319b7dbf2cd29845dadc5a899be20dfb299d48ff8e8c473f752(
    pg: IGraphItem,
    last_node: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d006c5bddd9b020c15566de3c68941f0760179055722e8e575c2960f018fe6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a10ccd81f1f207caf8c9b067806e95f3d700d627555c0540cecd5fd05a845aa(
    value: IGraphItem,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6fbc4d3e6e94e025105c39a10374eaf47be2eae03255e73531b6b7a8a9494a(
    graphs: typing.Sequence[IGraphItem],
    pg_oas: typing.Sequence[IAgentTool],
    sessions: typing.Optional[typing.Sequence[PromptGroupSession]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c422d3dabe9ef8abba2c3bbbd65cb211404930f96fa869276b763d0a958241a3(
    all_tools: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be23542c51313e85e41f7c13dc0faa8e100ea059aa4042e725c2259b23797102(
    tool: ToolCall,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dffcbbe7fe24829d0eac81f8a4e4a405acfb409cd895f58abf92291feb457c(
    value: typing.List[IAgentTool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b1512c48e4c0a4b618d417e46f7c83b02989356f2412aa0eae9d63b626ce0e(
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[ToolCallType] = None,
    payload: typing.Any = None,
    tool_call_id: typing.Optional[builtins.str] = None,
    is_pg: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca5092cdc5afd247201929b020a5a265e0bad7897d1e22e4b133be3ae8295bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cce041752b4e95ae25466ea39d32f51ec0301e64015b66ccf20bb9b23db25e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1940e09fdc14592acfce7003f99bcc770eb4b17ea62e53e30d6cbfd4d3d3707(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d9b994824033489cb2b3b806044405bcb06c1d72048f017c89bb422b16b35e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2059ec549c7384dd73be7be379faf6256c60a8ec7b55fdb9082692bbdc4bac54(
    value: ToolCallType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2debc725768136a46976eacab873877fdcc3efbb47c357e0973193213896e283(
    function_name: typing.Optional[builtins.str] = None,
    tool_call_id: typing.Optional[builtins.str] = None,
    payload: typing.Any = None,
    status_code: typing.Optional[jsii.Number] = None,
    result: typing.Any = None,
    is_success: typing.Optional[builtins.bool] = None,
    is_error: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fffc9823e52bc6b5b2f4aa72f7ed94614aad7d55b77f29de8574547aa73f28f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12e85757c6557cdf77248e76a660df04102b8873b38236827fb882d1fa6439a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0ae8339ae925874f36d96caaf593a776e69a5def415e6cd597660d7e9c011e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2de087a3432f7b811bf4e98dd110380b61cb2d0cdcd014af55ea9c493c5e516(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b512e8cc2e3d13362bf29e552b8dff26b147cd4cf7b3fc2ac09efd5bd6e5bd8(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7de4c43b1bcc39cb1dbd154a581a3c2a35f429555b50d12f81d0c6662c787a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e548be6ee41a966ad4e21e38458b2dc18fde679b9017e65e4f088b5b0d8c3580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ada04f0df01e9b462e0b973aee5f69eda17ab0f22e7345f33423f0acca9ad36(
    api_key: builtins.str,
    base_url: typing.Any = None,
    with_metrics_report: typing.Optional[builtins.bool] = None,
    custom_params: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89a5c88d1a2ed62ab765c38358d4adda81980f27657e34b4fe23fc61eca9217(
    llm_response: typing.Any,
    llm_provider: typing.Optional[LLMProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50de96ce44613a7f9044134d55c384c9cbc69918873535eed55a2d9c1f2cafbd(
    value: Agents,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f24bf46a0a96d6e069bcfdce151aa22264da15a80125c376dbad457bf91d1c0(
    value: Configuration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3ca6ba27cec860aa869deb2eaf5d80822747214c50652c074c1fd995c12295(
    configuration: Configuration,
    id: builtins.str,
    organization_id: builtins.str,
    status: AgentStatus,
    name: builtins.str,
    source_nodes: typing.Sequence[ISourceNode],
    pg_switch_allowed: typing.Optional[builtins.bool] = None,
    tools: typing.Optional[typing.Sequence[IAgentTool]] = None,
    graphs: typing.Optional[typing.Sequence[IGraphItem]] = None,
    pg_oas: typing.Optional[typing.Sequence[IAgentTool]] = None,
    auto_load: typing.Optional[builtins.bool] = None,
    pg_schemas: typing.Optional[typing.Sequence[IPGSchema]] = None,
    pg_node_description_override: typing.Optional[typing.Sequence[INodeDescription]] = None,
    general_instructions: typing.Optional[builtins.str] = None,
    judge_instructions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a4e9d238bcd6575542fe126282fe717dabbed97bd4b5d5f0906439f6debd49(
    tools: typing.Union[typing.Sequence[typing.Any], typing.Sequence[ILocalTool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773e3afa26f8b79fe00973c69c9983fbf523bfd2f52c02c0a473df8878934452(
    llm_provider: typing.Optional[LLMProvider] = None,
    return_all_tools: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083e27f1b35697c0dc5dd7bec052ea93d4a2fd3d2ee05d66ed6dfd7754537ddb(
    source_node_type: typing.Optional[SourceNodeType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8585cd601813225ff26808de89a1760108cbe32a7c1faf0681da25145fd71d1(
    llm_provider: typing.Optional[LLMProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1ca0e533f7a6dc6cf8465ad7809ba4a450abee064ca45429a80a258a5e2e65(
    tool: ToolCall,
    payload_extension: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307c287f13e8189f59310f2e5a43f33ebb271c35e1502a531966c06bbe13ef32(
    tool_calls: typing.Sequence[ToolCall],
    payload_extension: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa4e5a49bb8271c31eb566a9a8225672df671cea13eeb9e9905e74babd69207(
    prompt_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2acddc917b6b415bc14dfb9a7094cbd1b0319e93c3c4b3298f8cb5d9ec8206a7(
    value: Configuration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9976a447b388116d636066c048c970ab1f17c82f976d03a7ec90ffc1a1b6a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0a173561a6fcf731927ebbb3416e3e62701420fb7b719b46c04620b077300e(
    value: typing.List[IGraphItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b9d8c488cea43db21adbef0723558d2e632d07b3f9134efdeb872de791fa1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c8947d898e59570c44266cf149a9dc66dd2058cb95225c8af2063652d876a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc78718c4e88ad0687034fec3393a9b0dd4518c626fe4c60d2244cefaadbe37(
    value: typing.List[ILocalTool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22da1a47b30804817cea4f52e46761946f71d0d3436d3236d8ab8bbd3f9a2364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b78331aeaf11efbf7d44a1bd4ce9783ac8b3be074090b3f146520a09bb2ff99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6762bda91838241a6ee34d79cd8660a8ecf1de3ef553cabb0bd5130090bc15a3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62cf407b75bf35549e026b2eb3b2137665e585c1e08b5b490e8bbd6f09edd2b(
    value: typing.List[INodeDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c521ac8a0b5aa23bc0f993a5766f3392fb2d55936c5685fa6cd3639bf4ddb1(
    value: typing.List[IAgentTool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d25a9906544708d29f756b9d05b5c9086454a6e860208533e7f3b2df5c67ee1(
    value: typing.List[IPGSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae13b705d7d8977c7d3ad122cb11bb833d5688df9b90b593297a9976411d11b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7c66cd0fc6261d32287e8f4fbf7a0ee65a2f7d77886ad120d893353ebbe709(
    value: PromptGroupSessionsList,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bc6384ff613546183aa4186ddfac11deaaf2c2b3c4f43fd64f205dee4ad649(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dff1fd2031b8c10437260cbaae7a1861611afa24cb0ca6b7126c825461d0aa(
    value: typing.List[ISourceNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f657c5abb4af14138072346cc87aee77138c4171cd0fc2bf21f903fd6c6299ce(
    value: AgentStatus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d712115a2ab298e5d50d49c632fab67794a7409f1db441e663ee069fabba3ef8(
    value: typing.List[IAgentTool],
) -> None:
    """Type checking stubs"""
    pass
