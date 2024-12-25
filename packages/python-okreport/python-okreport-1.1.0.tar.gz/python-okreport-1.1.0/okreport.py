# -*- coding: utf-8 -*-
import os
import sys
import base64

from jinja2 import Environment, PackageLoader


class Var:
    """Variable.
    Var, where each Var object represents a piece of variable data within a report, have three sources:
    (1) Results, which are the outcomes of the pipeline being run, corresponding to the parameter "result";
    (2) Configuration, which refers to the parameters when running the process, corresponding to the parameter "conf";
    (3) Environment variables, corresponding to the parameter "env".
    """
    def parse(self, result, conf, env):
        raise NotImplementedError


class Image(Var):
    """Image variable."""
    def get_file(self, result, conf, env):
        raise NotImplementedError

    def parse(self, result, conf, env):
        file = self.get_file(result, conf, env)
        if file is None:
            return None
        with open(file, 'rb') as fp:
            data = fp.read()
        encoding = sys.getdefaultencoding()
        b64text = base64.b64encode(data).decode(encoding)
        ext = os.path.splitext(file)[1][1:]
        return f'data:image/{ext};base64,{b64text}'


class Paragraph:
    """Multiple variables."""

    def parse(self, result, conf, env):
        data = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            var = getattr(self, name)
            if not isinstance(var, Var):
                continue
            data[name] = var.parse(result, conf, env)
        return data


class Report:
    """Report."""
    def get_template(self):
        pkg = self.__module__.split('.')[0]
        env = Environment(loader=PackageLoader(pkg))
        return env.get_template('report.html')

    def render(self, result, conf, env):
        paragraphs = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            paragraph = getattr(self, name)
            if not isinstance(paragraph, Paragraph):
                continue
            paragraphs[name] = paragraph.parse(result, conf, env)
        template = self.get_template()
        return template.render(env=env, conf=conf, **paragraphs)
