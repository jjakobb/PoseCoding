from read_scd_files import parse_ndef_file, parse_combinator_file

ndef_index_dict = {
    1 : 0,
    2 : 1,
    3 : 2,
    4 : 3,
    5 : 4,
    6 : 5,
    10 : 6,
    11 : 7,
    12 : 8,
}

def load_scd_ndefs_and_templates():
    """
    Loads ndef and combination definitions from scd files

    Returns:
        combinators: array containing the three code snipptets for ndef combination
        n_definitions: array of an array containing ndefs each in three versions, as Ndef(\a), Ndef(\b) and modulated Ndef(\a)
    """
    template_file_path = "Ndefs/combination_templates.scd"
    combinators = parse_combinator_file(template_file_path)

    n_definitions = []

    ndef_path_mask = "Ndefs/{}.scd"
    for i in range(0, 10):
        fp = ndef_path_mask.format(i)
        try:
            result = parse_ndef_file(fp)
            n_definitions.append(result)
        except:
            result = ["//file_not_found", "//file_not_found", "//file_not_found"]
            n_definitions.append(result)
            continue
    return combinators, n_definitions

def code_combiner(input_array, combis, n_defs):
    """
    Loads ndef and combination definitions from scd files

    Args:
        input_array: array[3] containing the definition of the desired combination
        combis: array of strings with the combination templates
        n_defs: array of array of strings with the ndef definitions

    Returns:
        string: which can be executed in the SupcerCollider environment
    """
    definition_index_a = input_array[0]
    definition_index_b = input_array[2]
    combinator_index = 0
    mode_index_a = 1
    if input_array[1] == 9: # ADD
        combinator_index = 2
        mode_index_a = 0
    elif input_array[1] == 8: # MULTIPLY
        combinator_index = 1
        mode_index_a = 0
    elif input_array[1] == 7: # MODULATE
        combinator_index = 0
        mode_index_a = 1
    string = combis[combinator_index]
    string = remove_curly_brackets(string)
    string = string.format(n_defs[ndef_index_dict[definition_index_b]][2], n_defs[ndef_index_dict[definition_index_a]][mode_index_a])
    string = return_curly_brackets(string)
    return string

def remove_curly_brackets(string):
    string = string.replace("{}", "§§")
    string = string.replace("{", "°")
    string = string.replace("}", "$")
    string = string.replace("§§", "{}")
    return string

def return_curly_brackets(string):
    string = string.replace("°", "{")
    string = string.replace("$", "}")
    return string
