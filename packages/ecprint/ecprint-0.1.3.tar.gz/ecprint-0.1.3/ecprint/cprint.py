def cprint(*s, color='green', back_color=None, style='default', **args):
    color_ids = {'black':30, 'red':31, 'green':32, 'yellow':33, 
                 'blue':34, 'purple':35, 'cyan':36, 'white':37}
    style_ids = {'default':0, 'bold':1, 'underline':4}
    if color is not None:
        if color in list(color_ids.keys()):
            color = color_ids[color]
        elif color in list(color_ids.values()):
            color = color
        else:
            raise ValueError(f"Wrong string color {color}!\nAvailable colors are:\n{color_ids}")
    if back_color is not None:
        if back_color in list(color_ids.keys()):
            back_color = color_ids[back_color] + 10
        elif back_color-10 in list(color_ids.values()):
            back_color = back_color
        else:
            back_color_ids = {key:val+10 for key,val in color_ids.items()}
            raise ValueError(f"Wrong string color {back_color}!\nAvailable colors are:\n{back_color_ids}")
    if style is not None:
        if style in list(style_ids.keys()):
            style = style_ids[style]
        else:
            style = int(style)
    style = f'{style};' if style is not None else ''
    color = f'{color};' if color is not None else ''
    back_color = f'{back_color}' if back_color is not None else ''
    format = f'{style}{color}{back_color}'
    if format.endswith(";"):
        format = format[:-1]
    # print(format)
    s = ' '.join(s)
    print(f'\033[{format}m{s}\033[0m', **args)
