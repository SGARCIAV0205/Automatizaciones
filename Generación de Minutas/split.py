from llm import count_tokens

def chunk_text(text: str, target_tokens: int = 1800, max_tokens: int = 2200):
    parts, buf, buf_tokens = [], [], 0
    for para in text.split("\n"):
        t = count_tokens(para)
        if buf_tokens + t > target_tokens and buf:
            parts.append("\n".join(buf))
            buf, buf_tokens = [para], t
        else:
            buf.append(para); buf_tokens += t
        if buf_tokens > max_tokens:
            parts.append("\n".join(buf)); buf, buf_tokens = [], 0
    if buf: parts.append("\n".join(buf))
    return parts
