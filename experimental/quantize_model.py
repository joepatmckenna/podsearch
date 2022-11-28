import torch
import transformers

model_name = 'sentence-transformers/all-MiniLM-L6-v2'
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
model = transformers.AutoModel.from_pretrained(model_name)
model.eval()

sentences = ['hi there', 'bye for now']

inputs = tokenizer(sentences,
                   padding=True,
                   truncation=True,
                   return_tensors='pt')
with torch.no_grad():
    outputs = model(**inputs)

model.qconfig = torch.quantization.get_default_qconfig('fbgemm')

model_prepared = torch.quantization.prepare(model)

model_prepared(**inputs)

model_int8 = torch.quantization.convert(model_prepared)

res = model_int8(**inputs)
