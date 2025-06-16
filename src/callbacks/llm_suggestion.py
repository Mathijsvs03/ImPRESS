from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
model.eval()

def get_llm_suggestions(prompt_text, max_new_tokens=100):
    system_prompt = "<|system|>You are a helpful assistant.<|end|>"
    user_prompt = f"<|user|>{prompt_text}<|end|><|assistant|>"

    full_prompt = system_prompt + user_prompt

    inputs = tokenizer(full_prompt, return_tensors="pt")
    if torch.cuda.is_available() and model.device.type == "cuda":
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1]

    return response.strip()

@callback(
    Output("llm-suggestion-modal", "is_open", allow_duplicate=True),
    Output("llm-suggestion-modal-body", "children"),
    Input("generate-prompt-button", "n_clicks"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def open_modal_immediately(n_clicks, prompt_value):
    if not n_clicks or not prompt_value:
        raise PreventUpdate
    return True, "⏳ Generating prompt suggestion..."

@callback(
    Output("llm-suggestion-modal-body", "children", allow_duplicate=True),
    Input("llm-suggestion-modal", "is_open"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def update_llm_text(is_open, prompt_value):
    if not is_open or not prompt_value:
        raise PreventUpdate
    try:
        suggestion = get_llm_suggestions(prompt_value)
        return suggestion
    except Exception as e:
        return f"❌ Error: {str(e)}"

@callback(
    Output("llm-suggestion-modal", "is_open"),
    Output("Prompt", "value"),
    Input("accept-llm-suggestion", "n_clicks"),
    Input("decline-llm-suggestion", "n_clicks"),
    State("llm-suggestion-modal-body", "children"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def handle_modal_action(accept_click, decline_click, suggestion_text, current_prompt):
    triggered = ctx.triggered_id
    if triggered == "accept-llm-suggestion":
        return False, suggestion_text
    elif triggered == "decline-llm-suggestion":
        return False, current_prompt
    raise PreventUpdate
