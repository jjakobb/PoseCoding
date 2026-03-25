import re

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

# Example usage
file_path = "Ndefs/{}.scd".format(2)
result = parse_ndef_file(file_path)
print("a_clean:")
print(result[0])
print("a_mod:")
print(result[1])
print("b_clean:")
print(result[2])
