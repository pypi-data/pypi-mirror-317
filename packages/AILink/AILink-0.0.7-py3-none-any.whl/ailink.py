from openai import OpenAI
from typing_extensions import Literal
import httpx
from typing import Dict, List, Union, Iterable, Optional, Mapping
from openai._types import NOT_GIVEN, Body, Query, Headers, NotGiven, Timeout
from openai.types.chat_model import ChatModel
from openai.types.chat import (
    ChatCompletionAudioParam,
    ChatCompletionReasoningEffort,
    completion_create_params,
)
from openai._base_client import (
    DEFAULT_MAX_RETRIES
)
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_modality import ChatCompletionModality
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_audio_param import ChatCompletionAudioParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_reasoning_effort import ChatCompletionReasoningEffort
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from openai.types.chat.chat_completion_prediction_content_param import ChatCompletionPredictionContentParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
import os


base_url_mapping = {
    "ALIYUN": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "BAICHUAN": "https://api.baichuan-ai.com/v1",
    "BAIDU": "https://qianfan.baidubce.com/v2",
    "TENCENT": "https://api.hunyuan.cloud.tencent.com/v1",
    "ZHIPU": "https://open.bigmodel.cn/api/paas/v4",
    "XFYUN": "https://spark-api-open.xf-yun.com/v1",
    "BYTEDANCE": "https://ark.cn-beijing.volces.com/api/v3",
    "SENSETIME": "https://api.sensenova.cn/compatible-mode/v1/",
    "MOONSHOT": "https://api.moonshot.cn/v1"

}


class AILink(OpenAI):
    def __init__(
        self,
        *,
        model = None,
        api_key: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        base_url: str | httpx.URL | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ):
        if model:
            if ':' not in model:
                raise ValueError("model参数的格式为:[厂商名称]:[模型名称]，如 aliyun:qwen-plus")
            self.provider, self.model_name = model.split(":")
            if api_key is None:
                api_key = os.getenv(f"{self.provider.upper()}_API_KEY")
                if api_key is None:
                    raise ValueError(f"需要提前设置环境变量 {self.provider.upper()}_API_KEY")
            if base_url is None:
                base_url = base_url_mapping.get(self.provider.upper())
        super().__init__(api_key=api_key,
                         organization=organization,
                         project=project,
                         base_url=base_url,
                         websocket_base_url=websocket_base_url,
                         timeout=timeout,
                         max_retries=max_retries,
                         default_headers=default_headers,
                         default_query=default_query,
                         http_client=http_client,
                         _strict_response_validation=_strict_response_validation
        )
        self.__chat_reserve = self.chat.completions.create
        self.chat.completions.create = self.__chat_create

    def __chat_create(self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, ChatModel] = None,
        audio: Optional[ChatCompletionAudioParam] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        modalities: Optional[List[ChatCompletionModality]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Optional[ChatCompletionPredictionContentParam] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        reasoning_effort: ChatCompletionReasoningEffort | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        service_tier: Optional[Literal["auto", "default"]] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        store: Optional[bool] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN
    ) -> ChatCompletion:
        if model is None:
            model = self.model_name
        return self.__chat_reserve(
            messages=messages,
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
            reasoning_effort=reasoning_effort,
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
