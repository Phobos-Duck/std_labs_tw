def text_welcome():
    with open("text_for_start.txt", 'r', encoding='utf-8') as f:
        welcome = f.read()
        return welcome

def help_inctruction():
    with open("text_to_help.txt", 'r', encoding='utf-8') as f:
        instr = f.read()
        return instr