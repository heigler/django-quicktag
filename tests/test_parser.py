#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mox import Mox
from nose.tools import assert_equals

from quicktag.parser import Parser

def test_parser_iterates_through_chars():
    mox = Mox()

    parser = Parser('ab')
    mox.StubOutWithMock(parser, 'read_char')
    parser.read_char('a')
    parser.read_char('b')

    mox.ReplayAll()

    parser.parse()

    mox.VerifyAll()

def assert_stack_equals(text, expected_stack):
    parser = Parser(text)
    parser.parse()

    assert len(parser.stack) == len(expected_stack)

    for i, item in enumerate(expected_stack):
        assert_equals(parser.stack[i], item)

def test_parser_pushes_stack_at_the_end_of_the_string():
    yield assert_stack_equals, 'ab', ['ab']

def test_parser_splits_on_commas():
    yield assert_stack_equals, 'ab,cd', ['ab', 'cd']
    yield assert_stack_equals, 'ab, cd', ['ab', 'cd']
    yield assert_stack_equals, 'ab ,cd', ['ab', 'cd']

def test_parser_accepts_commas_inside_strings():
    yield assert_stack_equals, '"ab,cd"', ['"ab,cd"']

def test_parser_fix_escaped_quotes():
    yield assert_stack_equals, r'"ab\"cd"', ['"ab"cd"']

def test_parser_doesnt_fix_escaped_single_quotes_inside_double_quotes():
    yield assert_stack_equals, r"'ab\"cd'", [r"'ab\"cd'"]

def test_parser_doesnt_fix_escaped_double_quotes_inside_single_quotes():
    yield assert_stack_equals, r'"ab\'cd"', [r'"ab\'cd"']

def test_sample_arguments():
    kwargs = [
        'kw=',
    ]
    values = [
        'var',
        '"dbl-quotes"',
        "'single-quotes'",
    ]
    filters = [
        '|simple',
    ]

    for v in values:
        filters.append('|witharg:' + v)

    samples = []

    for v in values:
        samples.append(v)

    for v in values:
        samples.append(kwargs[0] + v)

    for v in values:
        for f in filters:
            samples.append(v + f)
            samples.append(kwargs[0] + v + f)

    for v in values:
        for f1 in filters:
            for f2 in filters:
                samples.append(v + f1 + f2)
                samples.append(kwargs[0] + v + f1 + f2)

    for t in samples:
        yield assert_stack_equals, t, [t]

