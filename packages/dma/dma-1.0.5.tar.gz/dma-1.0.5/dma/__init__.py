import shutil
import re

from random import randint
###################################################################################################################



class FadeV1():
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

        print(faded)



    def blackwhite(text):
        faded   = ""
        red     = 0
        green   = 0
        blue    = 0
        
        for line in text.splitlines():
            for character in line:
                if not red == 255 and not green == 255 and not blue == 255:
                    red    += 20
                    green  += 20
                    blue   += 20
                    
                    if red > 255 and green > 255 and blue > 255:
                        red    = 255
                        green  = 255
                        blue   = 255
                    
                faded += (f"\033[38;2;{red};{green};{blue}m{character}\033[0m")
    
        print(faded)



    def purplepink(text):
        faded  = ""
        red    = 40
        
        for line in text.splitlines():
            for character in line:
                if not red == 255:
                    red += 15
                    
                    if red > 255:
                        red = 255
                    
                faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
        
        print(faded)



    def greenblue(text):
        faded  = ""
        blue   = 100
        
        for line in text.splitlines():
            for character in line:
                if not blue == 255:
                    blue += 15
                    
                    if blue > 255:
                        blue = 255
                    
                faded += (f"\033[38;2;0;255;{blue}m{character}\033[0m")
        
        print(faded)



    def pinkred(text):
        faded  = ""
        blue   = 255
        
        for line in text.splitlines():
            for character in line:
                if not blue == 0:
                    blue -= 20
                    
                    if blue < 0:
                        blue = 0

                faded += (f"\033[38;2;255;0;{blue}m{character}\033[0m")
    
        print(faded)



    def purpleblue(text):
        faded  = ""
        red    = 110
        
        for line in text.splitlines():
            for character in line:
                if not red == 0:
                    red -= 15
                    
                    if red < 0:
                        red = 0
            
                faded += (f"\033[38;2;{red};0;255m{character}\033[0m")
        
        print(faded)



    def water(text):
        faded  = ""
        green  = 10
        
        for line in text.splitlines():
            for character in line:
                if not green == 255:
                    green += 15
                    
                    if green > 255:
                        green = 255

                faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        
        print(faded)



    def fire(text):
        faded  = ""
        green  = 250
        
        for line in text.splitlines():
            for character in line:
                if not green == 0:
                    green -= 25
                    
                    if green < 0:
                        green = 0
                
                faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
    
        print(faded)



    def brazil(text):
        faded  = ""
        red    = 0
    
        for line in text.splitlines():
            for character in line:
                if not red > 200:
                    red += 30
            
                faded += (f"\033[38;2;{red};255;0m{character}\033[0m")
    
        print(faded)



    def random(text):
        faded = ""
        
        for line in text.splitlines():
            for character in line:
                faded += (f"\033[38;2;{randint(0,255)};{randint(0,255)};{randint(0,255)}m{character}\033[0m")
    
        print(faded)
###################################################################################################################



class CFadeV1():
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



    def blackwhite(text):
        faded   = ""
        red     = 0
        green   = 0
        blue    = 0
        
        for line in text.splitlines():
            for character in line:
                if not red == 255 and not green == 255 and not blue == 255:
                    red    += 20
                    green  += 20
                    blue   += 20
                    
                    if red > 255 and green > 255 and blue > 255:
                        red    = 255
                        green  = 255
                        blue   = 255
                    
                faded += (f"\033[38;2;{red};{green};{blue}m{character}\033[0m")
    
        return faded



    def purplepink(text):
        faded  = ""
        red    = 40
        
        for line in text.splitlines():
            for character in line:
                if not red == 255:
                    red += 15
                    
                    if red > 255:
                        red = 255
                    
                faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
        
        return faded



    def greenblue(text):
        faded  = ""
        blue   = 100
        
        for line in text.splitlines():
            for character in line:
                if not blue == 255:
                    blue += 15
                    
                    if blue > 255:
                        blue = 255
                    
                faded += (f"\033[38;2;0;255;{blue}m{character}\033[0m")
        
        return faded



    def pinkred(text):
        faded  = ""
        blue   = 255
        
        for line in text.splitlines():
            for character in line:
                if not blue == 0:
                    blue -= 20
                    
                    if blue < 0:
                        blue = 0

                faded += (f"\033[38;2;255;0;{blue}m{character}\033[0m")
    
        return faded



    def purpleblue(text):
        faded  = ""
        red    = 110
        
        for line in text.splitlines():
            for character in line:
                if not red == 0:
                    red -= 15
                    
                    if red < 0:
                        red = 0
            
                faded += (f"\033[38;2;{red};0;255m{character}\033[0m")
        
        return faded



    def water(text):
        faded  = ""
        green  = 10
        
        for line in text.splitlines():
            for character in line:
                if not green == 255:
                    green += 15
                    
                    if green > 255:
                        green = 255

                faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        
        return faded



    def fire(text):
        faded  = ""
        green  = 250
        
        for line in text.splitlines():
            for character in line:
                if not green == 0:
                    green -= 25
                    
                    if green < 0:
                        green = 0
                
                faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
    
        return faded



    def brazil(text):
        faded  = ""
        red    = 0
    
        for line in text.splitlines():
            for character in line:
                if not red > 200:
                    red += 30
            
                faded += (f"\033[38;2;{red};255;0m{character}\033[0m")
    
        return faded



    def random(text):
        faded = ""
        
        for line in text.splitlines():
            for character in line:
                faded += (f"\033[38;2;{randint(0,255)};{randint(0,255)};{randint(0,255)}m{character}\033[0m")
    
        return faded
###################################################################################################################



class Fade():
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

            faded += "\n"

        return faded



    def blackwhite(text):
        faded   = ""
        red     = 0
        green   = 0
        blue    = 0
        
        for line in text.splitlines():
            for character in line:
                if not red == 255 and not green == 255 and not blue == 255:
                    red    += 20
                    green  += 20
                    blue   += 20
                    
                    if red > 255 and green > 255 and blue > 255:
                        red    = 255
                        green  = 255
                        blue   = 255
                    
                faded += (f"\033[38;2;{red};{green};{blue}m{character}\033[0m")
            
            faded += "\n"
    
        return faded



    def purplepink(text):
        faded  = ""
        red    = 40
        
        for line in text.splitlines():
            for character in line:
                if not red == 255:
                    red += 15
                    
                    if red > 255:
                        red = 255
                    
                faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
            
            faded += "\n"
        
        return faded



    def greenblue(text):
        faded  = ""
        blue   = 100
        
        for line in text.splitlines():
            for character in line:
                if not blue == 255:
                    blue += 15
                    
                    if blue > 255:
                        blue = 255
                    
                faded += (f"\033[38;2;0;255;{blue}m{character}\033[0m")
            
            faded += "\n"
        
        return faded



    def pinkred(text):
        faded  = ""
        blue   = 255
        
        for line in text.splitlines():
            for character in line:
                if not blue == 0:
                    blue -= 20
                    
                    if blue < 0:
                        blue = 0

                faded += (f"\033[38;2;255;0;{blue}m{character}\033[0m")
            
            faded += "\n"
    
        return faded



    def purpleblue(text):
        faded  = ""
        red    = 110
        
        for line in text.splitlines():
            for character in line:
                if not red == 0:
                    red -= 15
                    
                    if red < 0:
                        red = 0
            
                faded += (f"\033[38;2;{red};0;255m{character}\033[0m")
            
            faded += "\n"
        
        return faded



    def water(text):
        faded  = ""
        green  = 10
        
        for line in text.splitlines():
            for character in line:
                if not green == 255:
                    green += 15
                    
                    if green > 255:
                        green = 255

                faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
            
            faded += "\n"
        
        return faded



    def fire(text):
        faded  = ""
        green  = 250
        
        for line in text.splitlines():
            for character in line:
                if not green == 0:
                    green -= 25
                    
                    if green < 0:
                        green = 0
                
                faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
            
            faded += "\n"
    
        return faded



    def brazil(text):
        faded  = ""
        red    = 0
    
        for line in text.splitlines():
            for character in line:
                if not red > 200:
                    red += 30
            
                faded += (f"\033[38;2;{red};255;0m{character}\033[0m")
            
            faded += "\n"
    
        return faded



    def random(text):
        faded = ""
        
        for line in text.splitlines():
            for character in line:
                faded += (f"\033[38;2;{randint(0,255)};{randint(0,255)};{randint(0,255)}m{character}\033[0m")
            
            faded += "\n"
    
        return faded
###################################################################################################################



class LowTaperFade:
    def __init__(self):
        self.ansi_regex = re.compile(r"(?:\x1B[@-_][0-?]*[ -/]*[@-~])")



    def strip_ansi(self, text):
        return self.ansi_regex.sub("", text)



    def center(self, text, end = "\n"):
        columns  = shutil.get_terminal_size().columns
        lines    = text.splitlines()
        cl       = []
       
        for line in lines:
            stripped  = self.strip_ansi(line)
            padding   = max((columns - len(stripped)) // 2, 0)
            cl.append(" " * padding + line)
        
        print("\n".join(cl), end = end)



    def magic(self, text):
        columns  = shutil.get_terminal_size().columns
        lines    = text.splitlines()
        cl       = []
        
        for line in lines:
            stripped  = self.strip_ansi(line)
            padding   = max((columns - len(stripped)) // 2, 0)
            cl.append(" " * padding + line)
       
        return "\n".join(cl)



    def apply_effect_and_center(self, text, thisone):
        effect = thisone(text)

        return self.magic(effect)