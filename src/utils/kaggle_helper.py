import kagglehub
import os
# Download latest version

os.environ['KAGGLEHUB_CACHE'] = f'{os.getcwd()}/asset/wildPlastic'
if not os.path.isdir(f'{os.getcwd()}/asset/wildPlastic/datasets'):
    path = kagglehub.dataset_download("siddharthkumarsah/plastic-bottles-image-dataset")
else:
    print("dataset is exist!!")