import spacy

# python -m spacy download en_core_web_sm

# 加载英文模型
nlp = spacy.load("en_core_web_sm")
# 示例文本
text = "Apple is looking at buying U.K. startup for $1 billion."
# 处理文本
doc = nlp(text)
# 词性标注
print("POS Tagging:")
for token in doc:
    print((token.text, token.pos_))
# 命名实体识别
print("\nNamed Entity Recognition:")
for ent in doc.ents:
    print((ent.text, ent.label_))
