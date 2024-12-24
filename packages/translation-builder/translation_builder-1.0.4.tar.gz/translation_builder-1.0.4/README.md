
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/translation-builder)![PyPI - Version](https://img.shields.io/pypi/v/translation-builder)[![wakatime](https://wakatime.com/badge/user/90c8afe4-47c1-4f14-9423-4474ab0618ae/project/2a4d5581-e29c-4cd6-b898-103f15fa8b1b.svg)](https://wakatime.com/badge/user/90c8afe4-47c1-4f14-9423-4474ab0618ae/project/2a4d5581-e29c-4cd6-b898-103f15fa8b1b)


## INFO

This is a simple library providing the ability to generate a Python file from a `YML` file. It's make easy to use the data from the original file, for example for translation files.
## Installation

The library is available on PyPi, so you can install it in the standard way:

##### Windows
```bash
  pip install translation-builder
```
##### Ubuntu/macOS
```bash
  pip3 install translation-builder
```
## Example

#### YML file example
```my_file.yml
good-translation:
  cool: "No!"
  one-more-cool:
    - 1
    - 2
    - 3
```

#### File generation
```bash
g-translation --file my_file.yml --py_result ./my_directory/
```

#### Usage in your code
```main.py
from my_directory import my_file_tg

print(my_file_tg.Root.good_translation.cool)
print(my_file_tg.Root.good_translation.one_more_cool[1])
```

#### Result
```bash
No!
2
```
![MEW](https://media1.tenor.com/m/bn7amhoVqkIAAAAd/%D1%81%D0%B8%D0%B4%D0%B8%D1%82-%D0%BA%D0%BE%D0%BC%D0%B0%D1%80%D0%B8%D0%BA.gif)