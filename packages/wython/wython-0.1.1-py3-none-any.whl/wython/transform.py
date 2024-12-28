from keyword import kwlist


def transform_code(code, id):
    code = code.split('\n')
    for i in range(len(id)):
        para, b, e = id[i]
        code[para - 1] = code[para - 1][:b - 1] + f'w_image_list[{i}]' + code[para - 1][e:]

    return ''.join([x + '\n' for x in code])
