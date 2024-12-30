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