
from typing import List, Optional
from jinja2 import Environment

from .promptlib import json_schema


DEFAULT_PROMPT = """
{%- if last_try  %}
## RETRY AGAIN
You have tried before using this output:
```
{{ last_try }}
```
Try again, do you best to use the right output format.

{% endif %}
## Output Format:
Your response must strictly adhere to the following output format:
{%- if json_output  %}
{%- if json_output_many  %}
Answer in JSON using any of these schemas in a single block:
{{ output_format }}
{% else %}
Answer in JSON using this schema:
{{ output_format }}
{% endif %}
JUST USE JSON FORMAT FOR THE OUTPUT.
{% else %}
Answer using the type: {{ output_format }}
{% endif %}

Remember: Always use the required output format, even if you believe the conversation has ended or is not needed.
"""

AGENTIC_PROMPT = """
{%- if last_try  %}
## RETRY AGAIN
You have tried before using this output:
```
{{ last_try }}
```
Try again, do you best to use the right output format.

{% endif %}

## Output Format:
Your response must strictly adhere to the following output format:
{%- if json_output  %}
{%- if json_output_many  %}
Answer in JSON using any of these schemas in a single block:
{{ output_format }}
{% else %}
Answer in JSON using this schema:
{{ output_format }}
{% endif %}
JUST USE JSON FORMAT FOR THE OUTPUT.
{% else %}
Answer using the type: {{ output_format }}
{% endif %}

Instructions for processing and responding:

1. Carefully read and understand the system message, conversation history, and output format requirements.

2. In your analysis process, consider the following:
   a. Summarize the conversation history and system message.
   b. Identify any tools that have already been used and their outputs.
   c. List any missing information or clarifications needed.
   d. Outline a output plan, including potential tool usage.
   e. Ensure that your response will fit the required output format.

3. Wrap your analysis in <analysis> tags before formulating your final response.

4. Always provide your final response in the specified output format. Do not skip this step, even if you think the conversation has concluded or is not needed.

5. If the output format requires specific fields or structure, ensure all required elements are included.

6. Double-check that your response adheres to all given instructions and format requirements before submitting.

Example of the analysis and output process:

<analysis>
1. Summary of conversation and system message:
   [Brief summary here]

2. Tools already used and their outputs:
   [List of tools and outputs, or "No tools used yet"]

3. Missing information or needed clarifications:
   [List any unclear points or required information]

4. Output plan:
   [Outline of how to address the user's query, including potential tool usage]

5. Response format considerations:
   [Notes on how to structure the response to fit the required format]
</analysis>

[Your final output in the specified output format]

Remember: Always use the required output format, even if you believe the conversation has ended or is not needed. Pay close attention to the TOOL role in the conversation history and avoid unnecessary tool calls.
"""


def build_prompt(
        prompt_template: str,
        history: List,
        system: Optional[str] = None,
        response_type: type = str,
        last_try: Optional[str] = None,
        **kwargs
):
    messages: List = []
    if system:
        messages.append({"role": "system", "content": system})

    template = Environment().from_string(prompt_template)
    message_content = [{"type": "text", "text": "## Conversation History:\n"}]
    for msg in history:
        content_list = msg['content']
        if isinstance(content_list, str):
            content_list = [{"type": "text", "text": content_list}]
        role_name = msg['role'].upper()
        if role_name == 'TOOL' and 'name' in msg:
            role_name = f"TOOL({msg['name']})"
        message_content.append({"type": "text", "text": f"- {role_name}: "})
        for content in content_list:
            message_content.append(
                {"type": content["type"], content["type"]: content[content["type"]]})

    is_primitive = response_type in (int, float, bool, str)
    schema_str, length = json_schema(
        response_type, use_md=not response_type == str)
    template_content = template.render(
        json_output=not is_primitive,
        json_output_many=length > 1,
        output_format=schema_str,
        last_try=last_try,
        **kwargs
    )
    message_content.append({"type": "text", "text": template_content})
    messages.append({"role": "user", "content": message_content})
    return messages
