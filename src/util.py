import copy
file_extension = {
    "C++11": "cc",
    "C++14": "cc",
    "C++17": "cc"
}

compile_options = {
    "C++11": [
        "g++", "-O2", "-o", "${NAME}", "${SRC_PATH}",
        "-Wall", "-std=c++11", "-DONLINE_JUDGE"],
    "C++14": [
        "g++", "-O2", "-o", "${NAME}", "${SRC_PATH}",
        "-Wall", "-std=c++14", "-DONLINE_JUDGE"],
    "C++17": [
        "g++", "-O2", "-o", "${NAME}", "${SRC_PATH}",
        "-Wall", "-std=c++17", "-DONLINE_JUDGE"]
}

execution_options = {
    "C++11": ["${NAME}"],
    "C++14": ["${NAME}"],
    "C++17": ["${NAME}"],
}


# Returns the highest memory usage of the process at any given time in KB.
def get_current_memory_usage(pid):
    with open('/proc/' + str(pid) + "/status") as f:
        status_report = f.read()
        memusage = status_report.split('VmPeak:')
        if (len(memusage) < 2):
            # If it does not contain VmPeak, then return None
            return None
        memusage = memusage[1].split('\n')[0].split()
        memusage = memusage[0]

    return int(memusage)


def find_compile_option(lang, name, src_path=None):
    if lang not in compile_options:
        raise KeyError
    else:
        if src_path == None:
            src_path = '{}.cc'.format(name)
        option = copy.copy(compile_options[lang])
        for i in range(len(option)):
            option[i] = option[i].replace("${NAME}", name)
            option[i] = option[i].replace("${SRC_PATH}", src_path)
        return option

def find_execution_option(lang, name, params=None):
    if lang not in execution_options:
        raise KeyError
    else:
        option = copy.copy(execution_options[lang])
        for i in range(len(option)):
            option[i] = option[i].replace("${NAME}", name)
        if params != None:
            for param in params:
                option.append(param)
        return option
