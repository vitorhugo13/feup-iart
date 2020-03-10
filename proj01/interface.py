def main_menu():
    draw_interface()

def draw_interface():
    top_line = make_top_line()
    bot_line = make_bot_line()

    draw_line(top_line)
    draw_content()
    draw_line(bot_line)

def make_top_line():
    line = ""

    for i in range(1,60):
        line = line + '\u005F'
    
    return line

def make_bot_line():
    line = ""

    for i in range(1,60):
        line = line + '\u203E'
    
    return line


def draw_line(line):
    print(" " + line)
   
def draw_content():
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
    print('\uff5c'+ "                                                         " + '\uff5c')
