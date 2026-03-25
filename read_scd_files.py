import re

# The ndef files defining the sound generators should be under Ndefs/0.scd - Ndefs/8.scd
def parse_ndef_file(file_path):
    """
    Reads a text file and parses it into three strings stored in an array:
     - [0] contents between "//BEGIN_A_CLEAN" and "//END_A_CLEAN"
     - [1] contents between "//BEGIN_A_MOD" and "//END_A_MOD"
     - [2] contents between "//BEGIN_B_CLEAN" and "//END_B_CLEAN"

    Args:
        file_path (str): Path to the text file

    Returns:
        array: An array with three strings containing the content of each block
    """
    blocks = []
    block = ""
    in_block = False
    with open(file_path, "r") as f:
        content = f.read()

    for line in content.splitlines():
        if line.startswith("//BEGIN_A_CLEAN"):
            if in_block and block != "":
                blocks.append(block)
                block = ""
            else:
                block = ""
            in_block = True
        elif line.startswith("//END_A_CLEAN"):
            if in_block and block != "":
                #block += "\n" + line + "\n"
                blocks.append(block)
                block = ""
                in_block = False
        elif line.startswith("//BEGIN_A_MOD"):
            if in_block and block != "":
                blocks.append(block)
                block = ""
            else:
                block = ""
            in_block = True
        elif line.startswith("//END_A_MOD"):
            if in_block:
                #block += "\n" + line + "\n"
                blocks.append(block)
                block = ""
                in_block = False
        elif line.startswith("//BEGIN_B_CLEAN"):
            if in_block and block != "":
                blocks.append(block)
                block = ""
            else:
                block = ""
            in_block = True
        elif line.startswith("//END_B_CLEAN"):
            if in_block:
                #block += "\n" + line + "\n"
                blocks.append(block)
                block = ""
                in_block = False
        else:
            if in_block:
                block += line + "\n"

    # Append the last block, if it's not empty
    if in_block and block != "":
        blocks.append(block)

    return blocks

# The combination_templates file should be under Ndefs/combination_templates.scd
def parse_combinator_file(file_path):
    """
    Reads a text file and parses it into three strings:
     - mod: contents between "//BEGIN_MOD" and "//END_MOD"
     - mul: contents between "//BEGIN_MUL" and "//END_MUL"
     - add: contents between "//BEGIN_ADD" and "//END_ADD"

    Args:
        file_path (str): Path to the text file

    Returns:
        list: A list with three strings containing the content of each block
    """
    blocks = []
    lines = []

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

    mod_block = ""
    mul_block = ""
    add_block = ""

    in_mod_block = False
    in_mul_block = False
    in_add_block = False

    for line in lines:
        if line.startswith("//BEGIN_MOD"):
            in_mod_block = True
        elif line.startswith("//END_MOD"):
            in_mod_block = False
        else:
            if in_mod_block:
                mod_block += line

        if line.startswith("//BEGIN_MUL"):
            in_mul_block = True
        elif line.startswith("//END_MUL"):
            in_mul_block = False
        else:
            if in_mul_block:
                mul_block += line

        if line.startswith("//BEGIN_ADD"):
            in_add_block = True
        elif line.startswith("//END_ADD"):
            in_add_block = False
        else:
            if in_add_block:
                add_block += line

    # Remove //SLOT_A and //SLOT_B from each block
    mod_block = re.sub(r'//SLOT_A', "{}", mod_block)
    mod_block = re.sub(r'//SLOT_B', "{}", mod_block)

    mul_block = re.sub(r'//SLOT_A', "{}", mul_block)
    mul_block = re.sub(r'//SLOT_B', "{}", mul_block)

    add_block = re.sub(r'//SLOT_A', "{}", add_block)
    add_block = re.sub(r'//SLOT_B', "{}", add_block)

    blocks.append(mod_block.strip())
    blocks.append(mul_block.strip())
    blocks.append(add_block.strip())

    return blocks
