# dtx-apis-prompts-utils

## Overview

**dtx-apis-prompts-utils** is a Python library designed for parsing and processing prompts within the Detoxio API ecosystem. This utility provides tools for managing complex prompt structures, base64 decoding, multi-turn interactions, and threat classification. 

## Features

- **Complex Prompt Handling**: Parse and manage structured prompts with roles like `USER`, `SYSTEM`, and `ASSISTANT`.
- **Base64 Decoding**: Automatically decode base64-encoded strings into JSON.
- **Multi-turn Prompts**: Handle multi-turn conversation flows seamlessly.
- **Threat Classification**: Integrate labels and categories for prompt-based threat classification.

## Installation

To install the library, use:

```bash
pip install dtx-apis-prompts-utils
```

## Usage

### Parsing Prompts

```python
from dtx_apis_prompts_utils import ComplexPromptMsgParser

parser = ComplexPromptMsgParser()
parsed_prompt = parser.parse(base64_encoded_or_json_string)

if parsed_prompt:
    print(parsed_prompt.prompt)
```

### Multi-turn Conversations

```python
from dtx_apis_prompts_utils import DtxPrompt

dtx_prompt = DtxPrompt(prompt="Hello, how are you?", safe=True, threat_class="LOW", threat_category="General")
generator = dtx_prompt.get_multi_turn_prompts_gen()

conversation = generator.next_prompt()
print(conversation)
```

## License

This project is licensed under the Custom detoxio License
