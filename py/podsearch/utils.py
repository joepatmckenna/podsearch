# if 'model' not in flask.session:
#     flask.session['model'] = ...
# return flask.session['model']

import html
import torch


def _mean_pool(output, mask):
    mask = mask.unsqueeze(-1).expand(output.size())
    output *= mask.float()
    return torch.sum(output, 1) / torch.clamp(mask.sum(1), min=1e-9)


def encode(sentences, tokenizer, model):
    inputs = tokenizer(sentences,
                       padding=True,
                       truncation=True,
                       return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    encodings = outputs['last_hidden_state']
    attention_mask = inputs['attention_mask']
    encodings = _mean_pool(encodings, attention_mask)
    encodings = torch.nn.functional.normalize(encodings, p=2, dim=1)
    return encodings


def preprocess(text):
    text = text.lower()
    text = html.unescape(text)
    text = text.strip()
    return text


def recvall(sock, buffer_size=4096):
    data = b''
    while chunk := sock.recv(buffer_size):
        data += chunk
    return data
