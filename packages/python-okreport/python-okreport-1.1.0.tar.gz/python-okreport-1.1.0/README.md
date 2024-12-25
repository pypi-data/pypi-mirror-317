# okreport: simple report automatic rendering

## Installation

```shell
pip install python-okreport
```

## Usage

```python
from jinja2 import Template
from okreport import Var, Paragraph, Report

class ResultX(Var):
    def parse(self, result, conf, env):  # noqa
        return result['x']
    
class ResultY(Var):
    def parse(self, result, conf, env):  # noqa
        return result['y']
    
class ResultSum(Var):
    def parse(self, result, conf, env):  # noqa
        return result['x'] + result['y']

class ConfX(Var):
    def parse(self, result, conf, env):  # noqa
        return conf['x']

class ConfY(Var):
    def parse(self, result, conf, env):  # noqa
        return conf['y']

class ConfSum(Var):
    def parse(self, result, conf, env):  # noqa
        return conf['x'] + conf['y']
    
class ResultParagraph(Paragraph):
    x = ResultX()
    y = ResultY()
    sum = ResultSum()

class ConfParagraph(Paragraph):
    x = ConfX()
    y = ConfY()
    sum = ConfSum()


class MyReport(Report):
    """
    In result, x = {{ p1.x }}, y = {{ p1.y }}, sum = {{ p1.sum }}.
    In conf, x = {{ p2.x }}, y = {{ p2.y }}, sum = {{ p2.sum }}.
    """
    p1 = ResultParagraph()
    p2 = ConfParagraph()
    
    def get_template(self):
        return Template(self.__doc__)


result = {'x': 1, 'y': 2}
conf = {'x': 3, 'y': 4}
my_report = MyReport()
text = my_report.render(result, conf, None)
print(text)
```