def green(s):
    return "\033[1;32m%s\033[m" % s


def yellow(s):
    return "\033[1;33m%s\033[m" % s


def red(s):
    return "\033[1;31m%s\033[m" % s


def log(*m):
    print(" ".join(map(str, m)))


def log_exit(*m):
    log(red("ERROR:"), *m)
    exit(1)


def log_success(*m):
    log(green("SUCCESS:"), *m)


def log_error(*m):
    log(red("ERROR:"), *m)
