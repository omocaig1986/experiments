import time


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    out = ""
    i = 0

    while True:
        if i == 4:
            break

        time.sleep(1)
        out += "Count... " + str(i) + "\n"
        i += 1

    out += "\n\n" + str(req)
    return out
