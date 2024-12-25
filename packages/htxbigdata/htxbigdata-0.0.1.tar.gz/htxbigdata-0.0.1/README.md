https://blog.csdn.net/yifengchaoran/article/details/113447773


打包 
python3 -m pip install  --upgrade setuptools wheel
cd setup.py的同级目录
python3 setup.py sdist bdist_wheel

上传
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository testpypi dist/*

安装
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps bigdata-pypi-zzh

正式环境
python3 -m twine upload dist/*
pip install bigdata-pypi-zzh

pypi-AgEIcHlwaS5vcmcCJDA4NDljYTlmLTc0MmYtNDhhZi05YzNlLTgxOWQ2MTYzNWJkNgACKlszLCJlOTk0OGYzNS1kYTU2LTQ2MjItYTVhMi01MTAyM2QxMDQwODUiXQAABiAGQEOKteSAuCXvQUgyKNP14SZEaO1uDbQVRyVZjTklgA
