from __future__ import annotations

from raksha import Parser

input = r"""
<START>

<TEXT> blablabla  blablabla blabla  bliblibli bliblibli blibli|</TEXT>
        <APP>\va <LEM>blabla</LEM> \msCa; bloblu \msCb</APP>
        <PARAL>\vab \similar\ \BhG\ 10.12ab$</PARAL>
        <NOTE>So this is a short note...</NOTE>
        <TR>This is the beginning of the translation...</TR>

<TEXT> blobloblo  blobloblo bloblo  blublublublu blubluṃ blublu||</TEXT>
        <APP>\vd <LEM>blubluṃ</LEM> \msCa; bloblumda \msCb</APP>
        <TR>... and then it contimues.ह</TR>


<TEXT> SANITY CHECK </TEXT>       

</START>
"""


def main() -> int:
    result = Parser.parse(input)

    if result:
        print(Parser.inspect(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
