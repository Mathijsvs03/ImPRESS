from transformers import AutoTokenizer, AutoModelForCausalLM

_model = None
_tokenizer = None


def get_llm_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        model_id = "Qwen/Qwen3-4B"
        _tokenizer = AutoTokenizer.from_pretrained(model_id)
        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto",
        )
        _model.eval()
    return _model, _tokenizer


def prompt_model(messages, max_new_tokens=32768, thinking=True):
    model, tokenizer = get_llm_model()

    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=thinking
    )

    model_inputs = tokenizer([input_text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
    )

    output_ids = generated_ids[0][len(model_inputs['input_ids'][0]):].tolist()
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    return thinking_content, content


def get_llm_suggestions(prompt_text, improvement_instruction=None, max_new_tokens=100):
    user_message = (
        f"Based on the following prompt, come up with one that is better suited for generating an image: {prompt_text}."
    )

    if improvement_instruction:
        user_message += f"\n\nInstruction: {improvement_instruction}"

    user_message += "\nRespond only with the newly improved prompt."

    messages = [
        {"role": "system", "content": "Your role is to come up with a better prompt for the user to generate an image. You will respond with the new improved prompt only."},
        {"role": "user", "content": user_message}
    ]

    _, content = prompt_model(messages, max_new_tokens=max_new_tokens, thinking=False)

    return content


def filter_style_keywords(candidates, top_n=3):
    prompt = (
        f"From the following keywords: [{', '.join(candidates)}], "
        f"return only those that describe the *style* or *aesthetic* of images, not objects or scenes. "
        f"Respond with a comma-separated list of the top {top_n} most representative style keywords from this list."
    )
    print("Input to LLM:", prompt)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    thinking_content, content = prompt_model(messages)
    # print("LLM Response Thinking:", thinking_content)
    print("LLM Response Content:", content)

    # TODO - Improve regex to better capture style-related keywords
    import re
    keywords = re.findall(r'\b[a-zA-Z][a-zA-Z ]{2,}\b', content)
    return list(dict.fromkeys(keywords))[:top_n]
