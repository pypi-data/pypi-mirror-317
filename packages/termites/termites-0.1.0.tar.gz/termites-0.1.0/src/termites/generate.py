from typing import Any, Dict, List
import litellm
import sys
import json
from termites.tools import get_tool_schemas, AVAILABLE_TOOLS
from termites.cache import get_cached_response, get_cached_response_weave, cache_response


def generate_response(prompt: str, model: str, messages: List[Dict[str, Any]] = [], use_cache: bool = True, use_weave: bool = False) -> str:
    """Generate response from LLM using litellm with tools."""
    try:
        if prompt:
            # Try to get from cache first if caching is enabled
            if use_cache:
                cache_fn = get_cached_response_weave if use_weave else get_cached_response
                if cached_response := cache_fn(prompt, model):
                    print("(cached response)")
                    return cached_response
            
            messages.append({"role": "user", "content": prompt})

        completion = litellm.completion(
            model=model,
            messages=messages,
            tools=get_tool_schemas(),
            tool_choice="auto",
        )

        response_message = completion.choices[0].message
        tool_calls = response_message.tool_calls
        
        # Handle tool calls if present
        if tool_calls:
            return _handle_tool_calls(tool_calls, model, messages, use_cache, use_weave)
        
        response = completion.choices[0].message.content
        
        # Cache the response if it's a new prompt
        if prompt and use_cache:
            cache_response(prompt, response, model)
            
        return response
    except Exception as e:
        print(f"Error generating response: {e}", file=sys.stderr)
        sys.exit(1)

def _handle_tool_calls(
    tool_calls: List[Any], 
    model: str, 
    messages: List[Dict[str, Any]] = [], 
    use_cache: bool = True,
    use_weave: bool = False
) -> str:
    """Handle tool calls from the LLM and generate final response."""
    available_functions = {tool["name"]: tool["function"] for tool in AVAILABLE_TOOLS}

    tool_results = []
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name in available_functions:
            result = available_functions[function_name](**function_args)
            tool_results.append({
                "tool": function_name,
                "args": function_args,
                "result": result
            })
    
    # Create a new prompt with tool results
    tool_results_str = "\n".join(
        f"Tool: {r['tool']}\nArgs: {r['args']}\nResult: {r['result']}"
        for r in tool_results
    )
    
    return generate_response(tool_results_str, model, messages, use_cache, use_weave)