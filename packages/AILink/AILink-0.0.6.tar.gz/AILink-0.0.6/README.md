# AILink

AILink is a library that mainly connects to the use of domestic large models, which is encapsulated and implemented based on compatible OpenAI interfaces. Through the AILink library, users only need to configure a {PROVIDER}_API_KEY to quickly connect and use domestic large models, which is quite convenient.

## The Supported Providers
their corresponding large models include:
 - 阿里云[aliyun], supporting Tongyi Qianwenllm
 - 百度[baidu], supporting ernie series llm
 - 腾讯[tencent], supporting hunyuan llm
 - 智谱[zhipu], supporting Zhipu llm
 - 科大讯飞[xfyun], supporting Spark llm
 - 百川智能[baichuan], supporting BaiChuan llm
 - 字节跳动[bytedance], supporting Doubao llm
 - 商汤[sensetime], supporting SenseChat llm
 - 月之暗面[moonshot], supporting Moonshot llm

For the model list corresponding to the provider, refer to the article [OpenAI库牵手国产大模型，一键解锁！超全参数配置秘籍来袭](https://mp.weixin.qq.com/s/S2A7FXp2znq1oIX41U9sjg)

## Install

The minimum required version of Python is >=3.10.

The installation command is as follows:
```bash
pip install AILink
```

## Usage

AILink will retain the same interface as OpenAI, and is fully compatible with OpenAI's usage, except for the instantiation of objects.

Before executing the code, you need to set up environment variables, for example:
```bash
export BAICHUAN_API_KEY=sk-?
```
The environment variables for other providers are set in a similar pattern, following the {PROVIDER}_API_KEY format. Here, PROVIDER should be replaced with the name of the provider as listed in "The Supported Providers," using all uppercase letters.

For example, the following case:
```bash
# - 阿里云[aliyun]
export ALIYUN_API_KEY=sk-?
# - 百度[baidu]
export BAIDU_API_KEY=sk-?
#  - 智谱[zhipu]
export ZHIPU_API_KEY=sk-?
#  - 字节跳动[bytedance]
export BYTEDANCE_API_KEY=sk-?
```

1. Standard usage

```python
from ailink import AILink

client = AILink(model="baichuan:Baichuan4-Turbo")
# 创建聊天请求
response = client.chat.completions.create(
    stream=True,
    messages=[{'role': 'user', 'content': '今天是星期几'}] # 用户输入的信息
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
```

2. Another usage is to specify the api_key and base_url parameters in the code, which is generally used when working with providers that are not provided by the AILink library.

```python
from ailink import AILink

client = AILink(api_key='sk-?', base_url='https://api.baichuan-ai.com/v1')
# 创建聊天请求
response = client.chat.completions.create(
    stream=True,
    messages=[{'role': 'user', 'content': '今天是星期几'}] # 用户输入的信息
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
```

3. When connecting to specific providers and if you do not want to set up the environment, you can specify the key directly in the code. This scenario is typically seen during the debugging and testing phase of the code.

```python
from ailink import AILink

client = AILink(model="baichuan:Baichuan4-Turbo", api_key='sk-?')
# 创建聊天请求
response = client.chat.completions.create(
    stream=True,
    messages=[{'role': 'user', 'content': '今天是星期几'}] # 用户输入的信息
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
```
