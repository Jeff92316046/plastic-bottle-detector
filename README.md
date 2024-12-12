# image_processing_final

## 初始化專案

### init submodule
```bash
git submodule update --init --recursive
```

### build module

刪除pyproject.toml 裡的 dlib 套件的那行  
Remove the line containing the `dlib` package from the `pyproject.toml` file.
```bash
poetry install  
poetry shell 
cd src/dlib
python -m build --wheel
cd ../..
```
version要自己找檔案名稱  
You need to find the version from the file name yourself.
```bash
poetry add src/dlib/dist/dlib-{version}.whl
```

測試testing
```bash
python ./src/test/train_detector.py -c ./asset/stopSign/images/ -a ./asset/stopSign/annotations/ -o ./src/test/output/output
python ./src/test/test_detector.py -d ./scr/test/output/output -t ./asset/stopSign/testing
```

python -m build --wheel --config-setting USE_AVX_INSTRUCTIONS=1 --config-setting DLIB_USE_CUDA=1