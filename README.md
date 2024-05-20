# v0.1
安装依赖：
```commandline
pip install -r requirements.txt
```
运行demo：
```commandline
python frontend.py
````
测试用例：
```
int a;
int b;
int c;
a = 1;
b = 2;
c = 0;
while (c < 10)
  a = a + b;
  b = b * 2;
  if (b > 0) b = 0 - b;
  c = c + a;
```