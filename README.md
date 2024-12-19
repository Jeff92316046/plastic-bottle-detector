# image_processing_final

# 特徵提取與 SVM 模型訓練與測試

本項目旨在通過特徵提取和支持向量機（SVM）進行模型訓練與測試，並支持自定義配置文件。

## 使用說明

### 1. 特徵提取

執行以下命令以提取數據集的特徵，輸出將根據配置文件保存至指定路徑。

```bash
python .\src\extract_feature.py -c .\src\setting.json
```

### 2. SVM 模型訓練

使用提取的特徵進行 SVM 模型訓練，結果會保存到配置文件中定義的模型路徑。

```bash
python .\src\svm.py -c .\src\setting.json
```

### 3. 模型測試

使用已訓練的模型對測試數據進行評估。

```bash
python .\src\main.py -c .\src\setting.json
```

## 環境需求

請確保已安裝以下依賴項：

- Python 3.x
- 必要的依賴庫可通過以下命令安裝：

```bash
pip install -r requirements.txt
```
