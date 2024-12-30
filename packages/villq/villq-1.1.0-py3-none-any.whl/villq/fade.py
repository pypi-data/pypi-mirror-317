import shutil
import re



def stripansi(txt):
    ansi = re.compile(r"(?:\x1B[@-_][0-?]*[ -/]*[@-~])")
    return ansi.sub("", txt)



def center(txt, end = "\n"):
    columns   = shutil.get_terminal_size().columns
    stripped  = stripansi(txt)
    padding   = (columns - len(stripped)) // 2
    print(" " * padding + txt, end = end)



def purple(txt):
    faded  = ""
    down   = False
    red    = 40
    
    for line in txt.splitlines():
        for character in line:
            if down:
                red -= 3
            
            else:
                red += 3
                
            if red > 254:
                red   = 255
                down  = True
          
            elif red < 1:
                red   = 30
                down  = False
                
            faded += f"\033[38;2;{red};0;220m{character}\033[0m"

    return faded