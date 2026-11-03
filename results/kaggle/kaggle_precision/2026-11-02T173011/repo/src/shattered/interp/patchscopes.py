"""Patchscopes detokenization (M1a), replicating FragMend / Tokens2Words (github.com/utahnlp/fragmend, commit b469549):

- representation: the word encoded alone (tokenizer defaults, so BOS where the model uses one); the last token's hidden
  state at every layer (index 0 = embeddings), from `output_hidden_states`;
- target prompt "X, X, X, X," split on "X": every placeholder position gets the patched state in place of its input
  embedding (BOS prepended when the tokenizer has one);
- greedy decoding of 20 new tokens, one batch row per layer;
- a layer "identifies" the word when the stripped output starts with the word and contains it delimited by
  non-letter/non-mark characters; detokenization layer = first identifying layer ("first_id_layer").

`in_context` variant: the state is taken at the word's last token inside a sentence instead of the word alone.
"""
from __future__ import annotations

import regex
import torch

FRAGMEND_PROMPT = "X, X, X, X,"
PLACEHOLDER = "X"


def build_template(tok, prompt: str = FRAGMEND_PROMPT, placeholder: str = PLACEHOLDER):
    ids = [tok.bos_token_id] if tok.bos_token_id is not None else []
    targets = []
    parts = prompt.split(placeholder)
    for i, part in enumerate(parts):
        ids += tok.encode(part, add_special_tokens=False)
        if i < len(parts) - 1:
            targets.append(len(ids))
            ids.append(0)
    return torch.tensor(ids), torch.tensor(targets)


def identifies(word: str, output: str) -> bool:
    out = output.strip()
    if not out.startswith(word):
        return False
    pattern = rf"(?<![\p{{L}}\p{{M}}]){regex.escape(word)}(?![\p{{L}}\p{{M}}])"
    return regex.search(pattern, out) is not None


def encode_with_bos(tok, text: str) -> list[int]:
    """Token ids with BOS prepended whenever the model has one (FragMend relies on tokenizer defaults, which drop BOS
    for Gemma 4; Gemma degenerates without it)."""
    ids = tok(text, add_special_tokens=False)["input_ids"]
    return ([tok.bos_token_id] if tok.bos_token_id is not None else []) + ids


@torch.no_grad()
def word_states(model, tok, word: str) -> torch.Tensor:
    """[n_layers+1, d] last-token hidden states of the word encoded alone (with BOS where the model has one)."""
    ids = torch.tensor([encode_with_bos(tok, word)], device=model.device)
    hs = model(input_ids=ids, output_hidden_states=True).hidden_states
    return torch.stack([h[0, -1] for h in hs])


@torch.no_grad()
def decode_states(model, tok, states: torch.Tensor, template=None, max_new_tokens: int = 20,
                  batch_size: int | None = None) -> list[str]:
    """Patch each state (one per row) into the template and greedily decode; returns one string per row.

    The template is fed as token ids and the patched states replace the input-embedding output at the placeholder
    positions via a forward hook during the prefill pass. For ordinary models this is identical to feeding patched
    `inputs_embeds` (FragMend). It is needed for Gemma 4, whose per-layer embeddings require token ids (from
    `inputs_embeds` alone it reverses the full embedding matrix, which does not fit in memory); there the placeholder
    positions keep the per-layer embedding of the placeholder token id."""
    ids, targets = template if template is not None else build_template(tok)
    ids, targets = ids.to(model.device), targets.to(model.device)
    emb_layer = model.get_input_embeddings()
    outs = []
    bs = batch_size or len(states)
    pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    for i in range(0, len(states), bs):
        s = states[i:i + bs]
        x = ids[None].repeat(len(s), 1)

        def hook(_mod, _inp, out, s=s):
            if out.shape[1] == x.shape[1]:  # prefill only; decode steps see one new position
                out = out.clone()
                out[:, targets] = s.to(out.dtype).to(out.device)[:, None, :]
            return out

        h = emb_layer.register_forward_hook(hook)
        try:
            gen = model.generate(input_ids=x, attention_mask=torch.ones_like(x), do_sample=False, num_beams=1,
                                 max_new_tokens=max_new_tokens, pad_token_id=pad,
                                 repetition_penalty=1.0)  # pure greedy; some generation configs set a penalty
        finally:
            h.remove()
        outs += tok.batch_decode(gen[:, x.shape[1]:], skip_special_tokens=True)
    return outs


def detok_layer(word: str, outputs: list[str]) -> int | None:
    for layer, out in enumerate(outputs):
        if identifies(word, out):
            return layer
    return None


def run_word(model, tok, word: str, target: str | None = None, template=None, batch_size=None) -> dict:
    """Isolated-word Patchscopes for one word. `target` is the string to match (defaults to the word)."""
    outputs = decode_states(model, tok, word_states(model, tok, word), template, batch_size=batch_size)
    return {"word": word, "target": target or word, "n_tokens": len(tok(word, add_special_tokens=False)["input_ids"]),
            "detok_layer": detok_layer(target or word, outputs), "outputs": outputs}
