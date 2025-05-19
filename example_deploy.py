from openai import OpenAI
import json
client = OpenAI(
    api_key='EMPTY',
    base_url=f'http://127.0.0.1:8005/v1',
)
models = [model.id for model in client.models.list().data]

query = 'Were Scott Derrickson and Ed Wood of the same nationality?'
sys_prompt = "Please carefully read the following content and select the document number that can answer the question."

docs = []
with open ('example_data.json','r',encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        doc = f"Title:{data['title']}, context:{data['context']}"
        docs.append(doc)

retrieved_docs = [f'[{i + 1}]{doc}\n' for i, doc in enumerate(docs)]

messages = [                                                                          
        {"role": "system", "content": sys_prompt},                      
        {"role": "user", "content": f"query: {query}\n\nContext:\n{retrieved_docs}"}   
]  

resp = client.chat.completions.create(model=models[0], messages=messages, temperature=0)
response = resp.choices[0].message.content
print(f'query: {query}')
print(f'response: {response}')


indices = [int(index.strip()) for index in response.split(',')]
selected_docs = [docs[index - 1] for index in indices if 0 < index <= len(docs)]

doc_context_list=[]
for idx, doc in enumerate(selected_docs, start=1):
        doc_context_list.append(f"{idx}. {doc}")
print(doc_context_list)

"""
models: ['Qwen2.5-7B-Instruct', 'lora1', 'lora2']
query: who are you?
response: I am an artificial intelligence model named swift-robot, developed by swift. I can answer your questions, provide information, and engage in conversation. If you have any inquiries or need assistance, feel free to ask me at any time.
query: who are you?
response: I am an artificial intelligence model named Xiao Huang, developed by ModelScope. I can answer your questions, provide information, and engage in conversation. If you have any inquiries or need assistance, feel free to ask me at any time.
"""
