
def table_body(src):
    for l_column, r_column in src:
        yield f'\t{l_column} & {r_column}'


def with_hline(func):
    def wrapper(*args, **kwargs):
        yield "\t\\hline"
        for line in func(*args, **kwargs):
            yield line + " \\\\ \\hline "
    return wrapper


def with_centering(func):
    def wrapper(*args, **kwargs):
        yield "\t\\centering"
        for line in func(*args, **kwargs):
            yield line
    return wrapper


def with_caption(caption, func):
    def wrapper(*args, **kwargs):
        yield f"\t\\caption{{{caption}}}"
        for line in func(*args, **kwargs):
            yield line
    return wrapper


def with_tabular(pattern, func):
    def wrapper(*args, **kwargs):
        yield f"\t\\begin{{tabular}}{{{pattern}}}"
        for line in func(*args, **kwargs):
            yield f'\t{line}'
        yield f"\t\\end{{tabular}}"
    return wrapper


def make_table(func):
    def wrapper(*args, **kwargs):
        yield f"\\begin{{table}}[h!]"
        for line in func(*args, **kwargs):
            yield line
        yield f"\\end{{table}}"
    return wrapper


def simple_document(func):
    def wrapper(*args, **kwargs):
        yield f"\\documentclass{{article}}"
        yield f"\\begin{{document}}"
        for line in func(*args, **kwargs):
            yield f"\t{line}"
        yield f"\\end{{document}}"
    return wrapper


def make_table(func):
    def wrapper(*args, **kwargs):
        yield f"\\begin{{table}}[h!]"
        for line in func(*args, **kwargs):
            yield line
        yield f"\\end{{table}}"
    return wrapper


class Chain:
    def __init__(self, func, /, *args, **kwargs):
        self.funcs = list()
        self.funcs.append((func, args, kwargs))

    def then(self, func, /, *args, **kwargs):
        self.funcs.append((func, args, kwargs))
        return self

    def run(self):
        for func, args, kwargs in self.funcs:
            yield func(*args, **kwargs)


def usepackage(name):
    yield f"\\usepackage{{{name}}}"


def graphicspath(path):
    yield f"\\graphicspath{{ {{{path}}} }}"


def _emit_values(*args):
    for item in args:
        yield item


def includegraphics(img):
    yield f"\\includegraphics{{{img}}}"


def inclue_graphics(*images):
    result = Chain(includegraphics, images[0])

    for item in images[1:]:
        result.then(includegraphics, item)

    return result


def enable_images(*pathToGraphics):
    result = Chain(usepackage, "graphicx")
    for path in _emit_values(*pathToGraphics):
        result.then(graphicspath, path)
    return result


def complex_document(prefaceGenerator: Chain = None, bodyGenerator: Chain = None):
    yield f"\\documentclass{{article}}"

    if prefaceGenerator is not None:
        for gen in prefaceGenerator.run():
            for item in gen:
                yield item

    yield f"\\begin{{document}}"

    if bodyGenerator is not None:
        for gen in bodyGenerator.run():
            for item in gen:
                yield f"\t{item}"

    yield f"\\end{{document}}"

