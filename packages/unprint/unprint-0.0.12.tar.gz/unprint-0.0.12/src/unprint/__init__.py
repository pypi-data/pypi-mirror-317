import time

def unprint(
    num_lines: int = 1,
    delay: int = 0,
) -> None:
    r"""
    This function unprints {num_lines} lines from your terminal
        - this works by printing 2 escape characteres
        - \033[1A moves your cursor up by one line
        - \x1b[2K deletes the line your cursor is on
        - and together, they unprint one line in terminal
    
    This function exists so you don't have to memorize these
    escape characters (lol)
        
    Args
        num_lines (int):  number of lines to unprint
        delay (int): number of seconds to wait before unprinting
    """
    CURSOR_UP = "\033[1A"
    CLEAR_LINE = "\x1b[2K"
    if delay:
        time.sleep(delay)
    print((CURSOR_UP + CLEAR_LINE) * num_lines, end='', flush=True)