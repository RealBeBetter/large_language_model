# 首先安装 certifi
# pip install --upgrade certifi

# Before run this, you should set NLTK Download Source:
# export NLTK_DATA=https://mirrors.tuna.tsinghua.edu.cn/nltk_data/

import os
import ssl
import certifi
import nltk

# 设置使用 certifi 的证书包
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# 配置 SSL 使用 certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
