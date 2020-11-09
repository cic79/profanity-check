#! /usr/bin/env python
# encoding:UTF-8

import os
import random
import re
import subprocess
from html.parser import HTMLParser
from io import StringIO


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def error(self, message):
        pass

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def cmd_exist(cmd):
    try:
        with open(os.devnull, 'w') as FNULL:
            subprocess.call(cmd.split(), stdout=FNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False
    return True


def exec_cmd(sys, cmd, verbose=True, skip_error=False):
    if verbose:
        sys.stdout.write('Running command: %s ...' % cmd)
    try:
        result = subprocess.check_output(cmd.split())
    except subprocess.CalledProcessError as e:
        if skip_error:
            return False
        raise sys.stderr.write('Error %s executing:\n%s' % (e, cmd))
    if verbose:
        sys.stdout.write('Output command: %s\n%s' % (cmd, result))
    return result.decode('utf-8', errors='replace')


def get_random_grammar(grammar_dir, grammars_list=()):
    grammars_list = grammars_list or [f for f in os.listdir(grammar_dir) if os.path.isfile(os.path.join(grammar_dir, f))
                                      and f.endswith('.grm') and f.find('pornsite') == -1]
    gf = random.choice(grammars_list)
    return os.path.join(grammar_dir, gf)


def get_random_text(sys, polygen, grammar_file, one_line=False, max_length=None):
    cmd = '%s %s' % (polygen, grammar_file)
    result = exec_cmd(sys=sys, cmd=cmd, verbose=False)
    result = re.sub(' +', ' ', strip_tags(result)).strip()
    if one_line:
        result = result.replace('\n', ' ')
    if max_length:
        result = result[:max_length]
    return result


def get_random_polygen_text(lang='it'):
    import sys

    dict_languages_grammars = {'it': 'ita', 'en': 'eng', 'fr': 'fra'}
    polygen = '/usr/games/polygen'
    polygen_data = '/usr/share/polygen'
    grammar_language = dict_languages_grammars[lang]
    grammar_dir = os.path.join(polygen_data, grammar_language)

    # Check presence of polygen...
    if not cmd_exist(polygen):
        sys.stderr.write('Please install polygen on this PC with:\nsudo apt-get install polygen')
        sys.exit(1)
    # Check presence of polygen-data...
    if not os.path.isdir(polygen_data):
        sys.stderr.write('Please install polygen-data on this PC with:\nsudo apt-get install polygen-data')
        sys.exit(1)
    # Check presence of grammar language...
    if not os.path.isdir(grammar_dir):
        output = exec_cmd(sys=sys, cmd='ls', verbose=False)
        sys.stderr.write('Please choose another grammar; \'%s\' is not available; '
                         'Only this grammars are available:\n%s' % (grammar_language, output))
        sys.exit(1)
    return get_random_text(sys=sys, polygen=polygen, grammar_file=get_random_grammar(grammar_dir=grammar_dir),
                           one_line=True)
