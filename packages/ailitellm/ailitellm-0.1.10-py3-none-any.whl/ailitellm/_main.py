from typing import Literal, Iterable, Callable
import httpx
from openai import OpenAI, NOT_GIVEN, NotGiven
from typing import Optional, Union, List, Dict, Any

from openai._types import Headers, Query, Body
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionAudioParam, ChatCompletionModality, \
    ChatCompletionPredictionContentParam, ChatCompletionStreamOptionsParam, ChatCompletionToolChoiceOptionParam, \
    ChatCompletionToolParam, completion_create_params
from inspect import signature, Parameter


from ._types import HFModelType

def ailite_model(model:HFModelType):
    return model


class AILite(OpenAI):
    def __init__(
        self,*args,**kwargs):
        super().__init__(
            base_url="https://api-inference.huggingface.co/v1/",
            api_key="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",
            *args,
            **kwargs
            )



def stream_ailite_response(chat_completion=None):
    for chunk in chat_completion:
        yield chunk


def get_json_schema(func: Callable) -> Dict[str, Any]:
    sig = signature(func)
    parameters = {}
    required = []

    for name, param in sig.parameters.items():
        param_type = param.annotation if param.annotation != Parameter.empty else "string"
        param_schema = {
            "type": _get_json_type(param_type),
            "description": f"Parameter {name}"
        }
        parameters[name] = param_schema
        if param.default == Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or f"Function {func.__name__}",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required
            }
        }
    }

_global_client = None

def _get_client():
    global _global_client
    if _global_client is None:
        _global_client = AILite()
    return _global_client

def _get_json_type(py_type):
    type_map = {
        int: "integer",
        float: "number",
        str: "string",
        bool: "boolean",
        list: "array",
        dict: "object"
    }
    return type_map.get(py_type, "string")
def ai(
    messages_or_prompt: Union[Iterable[ChatCompletionMessageParam],str],
    model: HFModelType="Qwen/Qwen2.5-72B-Instruct",
    audio: Optional[ChatCompletionAudioParam] | NotGiven = NOT_GIVEN,
    frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
    function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
    functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
    logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
    logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
    max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
    max_tokens: Optional[int] | NotGiven = 4028,
    metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
    modalities: Optional[List[ChatCompletionModality]] | NotGiven = NOT_GIVEN,
    n: Optional[int] | NotGiven = NOT_GIVEN,
    parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
    prediction: Optional[ChatCompletionPredictionContentParam] | NotGiven = NOT_GIVEN,
    presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
    response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
    seed: Optional[int] | NotGiven = NOT_GIVEN,
    service_tier: Optional[Literal["auto", "default"]] | NotGiven = NOT_GIVEN,
    stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
    store: Optional[bool] | NotGiven = NOT_GIVEN,
    stream: Optional[Literal[False]] | Literal[True] | NotGiven = False,
    stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
    temperature: Optional[float] | NotGiven = 0,
    tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
    tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
    top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
    top_p: Optional[float] | NotGiven = NOT_GIVEN,
    user: str | NotGiven = NOT_GIVEN,
    extra_headers: Headers | None = None,
    extra_query: Query | None = None,
    extra_body: Body | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
):
    ailite_client = _get_client()

    if tools:
        tools = [get_json_schema(t) if isinstance(t,Callable) else t for t in tools]

    if isinstance(messages_or_prompt,str):
        messages_or_prompt = [{"role": "user", "content": messages_or_prompt}]

    chat_completion = ailite_client.chat.completions.create(
        messages=messages_or_prompt,
        model=model,
        audio=audio,
        frequency_penalty=frequency_penalty,
        function_call=function_call,
        functions=functions,
        logit_bias=logit_bias,
        logprobs=logprobs,
        max_completion_tokens=max_completion_tokens,
        max_tokens=max_tokens,
        metadata=metadata,
        modalities=modalities,
        n=n,
        parallel_tool_calls=parallel_tool_calls,
        prediction=prediction,
        presence_penalty=presence_penalty,
        response_format=response_format,
        seed=seed,
        service_tier=service_tier,
        stop=stop,
        store=store,
        stream=stream,
        stream_options=stream_options,
        temperature=temperature,
        tool_choice=tool_choice,
        tools=tools,
        top_logprobs=top_logprobs,
        top_p=top_p,
        user=user,
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout
    )
    if stream:
        return stream_ailite_response(chat_completion=chat_completion)
    else:
        return chat_completion


