from transformers import AutoTokenizer, AutoModelForCausalLM
import re

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


def filter_style_keywords(candidates, top_n=10):
    example_keywords = ["desert", "sunset", "camel", "dunes"]

    example_prompt = f"""
    I have the following list of keywords that were extracted from user prompts intended for image generation:
    - {', '.join(example_keywords)}

    Your task is to analyze these keywords and return a new list of words that relate to:
    *style*, *aesthetic*, *mood*, *genre*, or any other visually relevant concept implied or suggested by the input.
    These new keywords should help inspire or enrich future image generation prompts, enforcing diversity.
    Focus on: Artistic styles (e.g., minimalism, surrealism, vaporwave), Moods and atmosphere (e.g., serene, eerie, chaotic),
    Visual characteristics (e.g., high contrast, muted colors, soft lighting), Cultural or conceptual associations (e.g., cyberpunk, baroque, post-apocalyptic).
    Avoid: Repeating the input keywords exactly, and listing generic or overly broad terms (e.g., "image", "art").
    Only return the most relevant keywords, separated by commas, without any additional text or explanation.
    """

    example_response = "warm tones, golden hour lighting, sparse landscape, nomadic aesthetic, windswept textures, earthy palette"

    keyword_prompt = f"""
    I have the following list of keywords that were extracted from user prompts intended for image generation:
    - {', '.join(candidates)}

    Your task is to analyze these keywords and return a new list of words that relate to:
    *style*, *aesthetic*, *mood*, *genre*, or any other visually relevant concept implied or suggested by the input.
    These new keywords should help inspire or enrich future image generation prompts.
    Focus on: Artistic styles (e.g., minimalism, surrealism, vaporwave), Moods and atmosphere (e.g., serene, eerie, chaotic),
    Visual characteristics (e.g., high contrast, muted colors, soft lighting), Cultural or conceptual associations (e.g., cyberpunk, baroque, post-apocalyptic).
    Avoid: Repeating the input keywords exactly, and listing generic or overly broad terms (e.g., "image", "art").
    Only return the {top_n} most relevant keywords, separated by commas, without any additional text or explanation.
    """

    messages = [
        {"role": "user", "content": example_prompt},
        {"role": "assistant", "content": example_response},
        {"role": "user", "content": keyword_prompt}
    ]

    _, content = prompt_model(messages, max_new_tokens=50, thinking=False)
    print("LLM Response Content:", content)

    try:
        keywords = re.findall(r'\b[a-zA-Z][a-zA-Z ]{2,}\b', content)
    except Exception as e:
        print(f"Keyword parsing failed: {e}")
        keywords = []

    return list(dict.fromkeys(keywords))[:top_n]
