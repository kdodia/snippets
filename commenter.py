# -*- coding: utf-8 -*-
"""Fancy comments for your Python scripts.

Example usage:
  > h3('Subsection Header')

  Your (system) clipboard will then contain the following padded string:
  '#---------------------------<   Subsection Header   >--------[...]'

  > print(h1('Important Section Header', copy=False))
  #=========================^                            ^======[...]
  #========================<   Important Section Header   >=====[...]
  #=========================v                            v======[...]

  This can be handy when e.g. developing in a code editor: import and run a
  single line with one of the header functions (h1, h2, h3, or h4) and then
  paste the fancy comment into the source file.


MIT License

Copyright (c) [2020] [Karan Dodia]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pyperclip
from toolz import curry
from toolz.dicttoolz import assoc


def _commenter(name: str,
               width: int = 80,
               align: str = '^',
               fill: str = '=',
               **kwargs):

  fancy_comment = f'#{name:{fill}{align}{width}}'
  return fancy_comment


@curry
def decorated_section(name: str,
                      width: int = 80,
                      align: str = '^',
                      fill: str = '=',
                      topline: bool = False,
                      bottomline: bool = False,
                      copy: bool = True):

  top, bottom = None, None

  fancy_name = f"<   {name}   >"
  middle = _commenter(**(assoc(locals(), 'name', fancy_name)))

  if topline:
    fancy_top = "^  {}  ^".format(' ' * len(name))
    top = _commenter(**(assoc(locals(), 'name', fancy_top)))

  if bottomline:
    fancy_bottom = "v  {}  v".format(' ' * len(name))
    bottom = _commenter(
        **(assoc(locals(), 'name', fancy_bottom)))

  output = '\n'.join(x for x in (top, middle, bottom) if x)

  if copy:
    pyperclip.copy(output)
  else:
    return output


h1 = decorated_section(topline=True, bottomline=True)
h2 = decorated_section()
h3 = decorated_section(fill='-')
h4 = decorated_section(fill=' ')
