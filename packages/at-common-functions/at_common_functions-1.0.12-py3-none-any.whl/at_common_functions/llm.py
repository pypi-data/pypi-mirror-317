from typing import List, Any
import logging
from jinja2 import Template, TemplateError, StrictUndefined
from at_common_functions.utils.storage import get_storage
from at_common_models.system.prompt import PromptModel
from at_common_functions.utils.openai import get_openai
from babel.numbers import format_currency, format_number, format_percent

logger = logging.getLogger(__name__)

def create_jinja_env():
    env = Template.environment_class()
    env.filters['format_currency'] = format_currency
    env.filters['format_number'] = format_number
    env.filters['format_percent'] = format_percent
    env.undefined = StrictUndefined
    return env

async def inference(*, model: str, prompt_name: str, **kwargs: Any) -> str:
    """
    Generate an inference using OpenAI's chat model with templated prompts.
    
    Args:
        model: OpenAI model identifier
        prompt_name: Name of the prompt template to use
        **kwargs: Additional keyword arguments to pass to the prompt template
    
    Returns:
        str: The model's response
        
    Raises:
        ValueError: If prompt is not found or multiple prompts exist
        TemplateError: If template rendering fails
    """
    if not model:
        raise ValueError("Model parameter cannot be empty")

    storage = get_storage()
    prompts: List[PromptModel] = await storage.query(
        model_class=PromptModel,
        filters=[PromptModel.name == prompt_name]
    )

    if len(prompts) == 0:
        raise ValueError(f"No prompt found for name: {prompt_name}")

    if len(prompts) > 1:
        raise ValueError(f"Multiple prompts found for name: {prompt_name}, got {len(prompts)}")
    
    prompt = prompts[0]
    
    try:
        env = create_jinja_env()
        sys_template = env.from_string(prompt.sys_tpl)
        usr_template = env.from_string(prompt.usr_tpl)
        
        system_prompt = sys_template.render(**kwargs)
        user_prompt = usr_template.render(**kwargs)
    except TemplateError as e:
        logger.error(f"Failed to render template for prompt {prompt_name}: {str(e)}")
        raise

    # Get OpenAI service and make inference
    openai = get_openai()
    response = await openai.chat(
        system=system_prompt,
        user=user_prompt,
        model=model,
        temperature=prompt.param_temperature,
        max_tokens=prompt.param_max_tokens
    )
    
    return response
    
    