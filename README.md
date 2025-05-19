# LLM-Reranker

LLM-Reranler能够在给定多篇chunk的情况下选择有助于回答query的chunk，使得重排阶段的chunk数量不局限于TopK。LLM-Reranker通过使用HotpotQA和Musique微调Qwen2.5-7B-Instrucrt实现。

## 环境准备
```bash
pip install ms-swift -U
```
LLM-Reranker使用ms-swift微调，更多详细内容可以参考[swift官方文档](https://swift.readthedocs.io/zh-cn/latest/Instruction/%E9%A2%84%E8%AE%AD%E7%BB%83%E4%B8%8E%E5%BE%AE%E8%B0%83.html#%E9%83%A8%E7%BD%B2%E5%BE%AE%E8%B0%83%E5%90%8E%E6%A8%A1%E5%9E%8B)

## 部署（微调后模型）
- 将`qwen2.5_hot_mus_sft\`放到当前文件夹下

- 使用以下脚本启动部署服务端。
```bash
bash deploy.sh
```


- 客户需要安装vllm
```bash
pip install vllm -U
```

若不通过vllm部署直接使用微调后的模型进行推理，可以参照[swift官方文档](https://swift.readthedocs.io/zh-cn/latest/Instruction/%E9%A2%84%E8%AE%AD%E7%BB%83%E4%B8%8E%E5%BE%AE%E8%B0%83.html#%E9%83%A8%E7%BD%B2%E5%BE%AE%E8%B0%83%E5%90%8E%E6%A8%A1%E5%9E%8B)


## 样例数据
例如对于文件`example_data.json`中的样例数据：
```data
{"title":"Ed Wood (film)","context":"Ed Wood is a 1994 American biographical period comedy-drama film directed and produced by Tim Burton, and starring Johnny Depp as cult filmmaker Ed Wood.\n\n The film concerns the period in Wood's life when he made his best-known films as well as his relationship with actor Bela Lugosi, played by Martin Landau.\n\n Sarah Jessica Parker, Patricia Arquette, Jeffrey Jones, Lisa Marie, and Bill Murray are among the supporting cast."}
{"title":"Scott Derrickson","context":"Scott Derrickson (born July 16, 1966) is an American director, screenwriter and producer.\n\n He lives in Los Angeles, California.\n\n He is best known for directing horror films such as \"Sinister\", \"The Exorcism of Emily Rose\", and \"Deliver Us From Evil\", as well as the 2016 Marvel Cinematic Universe installment, \"Doctor Strange.\""}
{"title":"Woodson, Arkansas","context":"Woodson is a census-designated place (CDP) in Pulaski County, Arkansas, in the United States.\n\n Its population was 403 at the 2010 census.\n\n It is part of the Little Rock\u2013North Little Rock\u2013Conway Metropolitan Statistical Area.\n\n Woodson and its accompanying Woodson Lake and Wood Hollow are the namesake for Ed Wood Sr., a prominent plantation owner, trader, and businessman at the turn of the 20th century.\n\n Woodson is adjacent to the Wood Plantation, the largest of the plantations own by Ed Wood Sr."}
```

通过`example_deploy.py`中的如下代码转换
```bash
docs = []
with open ('example_data.json','r',encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        doc = f"Title:{data['title']}, context:{data['context']}"
        docs.append(doc)

retrieved_docs = [f'[{i + 1}]{doc}\n' for i, doc in enumerate(docs)]
```

## 使用
- 运行样例`example_deploy.py`
```bash
python example_deplot.py
```
- 期望输出为chunk的标号
```data
2, 5 
```


