from collections import namedtuple

CtxManagerWithPosition = namedtuple('CtxManagerWithPosition', ('node', 'lineno', 'col_offset'))
