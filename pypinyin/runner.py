#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
import sys
from . import ( # noqa
    __title__, __version__, pinyin, slug,
    NORMAL, TONE, TONE2, TONE3, INITIALS, FIRST_LETTER,
    FINALS, FINALS_TONE, FINALS_TONE2, FINALS_TONE3,
    BOPOMOFO, BOPOMOFO_FIRST,
    SPLIT
)
from .compat import PY2


class NullWriter(object):
    """数据流黑洞，类似 linux/unix 下 /dev/null 的效果。"""
    def write(self, string):
        pass


def get_parser():
    parser = ArgumentParser(description='convert chinese to pinyin.')
    parser.add_argument('-V', '--version', action='version',
                        version='{0} {1}'.format(__title__, __version__))
    # 要执行的函数名称
    parser.add_argument('--func',
                        help='function name (default: "pinyin")',
                        choices=['pinyin', 'slug'],
                        default='pinyin')
    # 拼音风格
    parser.add_argument('--style',
                        help='pinyin style (default: "TONE")',
                        choices=['NORMAL', 'TONE', 'TONE2', 'TONE3',
                                 'INITIALS', 'FIRST_LETTER', 'FINALS',
                                 'FINALS_TONE', 'FINALS_TONE2', 'FINALS_TONE3',
                                 'BOPOMOFO', 'BOPOMOFO_FIRST', 'SPLIT'],
                        default='TONE')

    parser.add_argument('--separator',
                        help='slug separator (default: "-")',
                        default='-')

    parser.add_argument('--errors',
                        help=('how to handle none-pinyin string '
                              '(default: "default")'),
                        choices=['default', 'ignore', 'replace'],
                        default='default')
    # 输出多音字
    parser.add_argument('--heteronym',
                        help='enable heteronym',
                        action='store_true')
    # 要查询的汉字
    parser.add_argument('--hans',
                        help='chinese string',
                        default='')

    # 要导入的名字
    parser.add_argument('--file', '-f',  help='input file')
    return parser


def main():
    import logging
    # 禁用除 CRITICAL 外的日志消息
    logging.disable(logging.CRITICAL)

    # 获取命令行选项和参数
    args = sys.argv[1:]
    parser = get_parser()
    options = parser.parse_args(args)

    func = globals()[options.func]

    kwargs = {
        "style": globals()[options.style],
        "heteronym": options.heteronym,
        "separator": options.separator,
        "errors": options.errors
    }

    # 命令行参数
    hans = options.hans.decode(sys.stdin.encoding) if PY2 else options.hans

    inputFile = options.file
    with open(inputFile,  'rb') as file_object:
        all_the_text = file_object.read().decode('utf-8')
        # 如果存在文件处理文件的内容
        hans = all_the_text

    print "all_the_text=", hans

    # 重设标准输出流和标准错误流
    # 不输出任何字符，防止污染命令行命令的输出结果
    # 其实主要是为了干掉 jieba 内的 print 语句 ;)
    # sys.stdout = sys.stderr = NullWriter()
    # sys.stderr = NullWriter()

    result = func(hans, **kwargs)
    # 恢复默认
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    if result and isinstance(result, (list, tuple)):
        if isinstance(result[0], (list, tuple)):
            print(' '.join([','.join(s) for s in result]))
        else:
            print(result)
    else:
        print(result)

if __name__ == '__main__':
    main()
