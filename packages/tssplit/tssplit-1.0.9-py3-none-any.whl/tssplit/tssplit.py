"""Trivial split for strings with multiple character delimiters, quotes and escaped characters"""


def tssplit(s:str, quote:str='"\'', quote_keep:bool=False, delimiter:str=':;,', escape:str='/^', trim:str='',
            remark:str='#') -> list[str]:

    """Split a string by delimiters with quotes and escaped characters, optionally trimming results

    :param s: A string to split into chunks
    :param quote: Quote chars to protect a part of s from parsing
    :param quote_keep: Preserve quote characters in the output or not
    :param delimiter: A chunk separator character
    :param escape: An escape character
    :param trim: Trim characters from chunks
    :param remark: Ignore all characters after remark sign
    :return: A list of chunks
    """

    in_quotes = in_escape = False
    token = ''
    result:list[str] = []

    for c in s:
        if in_escape:
            token += c
            in_escape = False
        elif c in escape:
            in_escape = True
            if in_quotes:
                token += c
        elif c in quote and not in_escape:
            in_quotes = not in_quotes
            if quote_keep:
                token += c
        elif c in delimiter and not in_quotes:
            if trim:
                token = token.strip(trim)
            result.append(token)
            token = ''
        elif c in remark:
            break
        else:
            token += c

    if trim:
        token = token.strip(trim)
    result.append(token)
    return result


if __name__ == "__main__":
    pass
