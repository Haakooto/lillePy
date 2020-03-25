def superscript(input):
    # this only supports numbers for now. when letter support is aded, the below
    # try-except can be removed
    superscriptdict = {
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "0": "⁰",
    }
    try:
        float(input)
    except:
        print("superscript for now only takes numbers!")
        import sys

        sys.exit([1])
    if input not in superscriptdict.keys():
        return input

    # assert isinstance(input, String), f'Expected type string got {type(input)}'

    res = ""
    for i in input:
        res += superscriptdict[i]
    return res
