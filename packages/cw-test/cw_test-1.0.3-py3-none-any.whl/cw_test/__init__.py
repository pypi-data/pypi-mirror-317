
ipy = get_ipython()

def mscene_magic(line):

  line_magic = f"-m cw_test {line}"

  ipy.run_line_magic("run", line_magic)

ipy.register_magic_function(mscene_magic, "line", "mscene")
