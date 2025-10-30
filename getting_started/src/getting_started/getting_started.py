from typing import AsyncGenerator

from nat.core.builder import Builder
from nat.core.function import FunctionBaseConfig, FunctionInfo, register_function


class GettingStartedFunctionConfig(FunctionBaseConfig):
	name: str = "getting_started"


@register_function(config_type=GettingStartedFunctionConfig)
def getting_started(config: GettingStartedFunctionConfig, builder: Builder) -> AsyncGenerator[FunctionInfo, None]:
	async def _impl(prompt: str) -> str:
		text = prompt or ""
		lower = text.lower()

		if "current time" in lower or "time now" in lower:
			current_datetime_tool = await builder.get_function(name="current_datetime")
			return await current_datetime_tool(text)

		if "echo" in lower and "name" in lower:
			import re as _re
			match = _re.search(r"name[, ]+([^?!.]+)", text, _re.IGNORECASE)
			if match:
				name = match.group(1).strip(" ?.'\"")
				return f"Your name is {name}."
			return "I can echo your name if you provide it."

		return f"GettingStarted tool received: {text}"

	yield FunctionInfo(fn=_impl, name=config.name)
