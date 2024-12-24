# code(core): use typing to define types
from typing import List, Dict, Union, Tuple

# code(core): type define
# 编码(核心): 类型定义
NanoPlainValue = str
NanoParsedValue = Union[bool, int, None, str]
NanoArgvs = List[str]
NanoExtras = List[str]
NanoFlags = Dict[str, NanoPlainValue]
NanoParsedFlags = Dict[str, NanoParsedValue]
NanoStrvFlag = NanoFlags
NanoJssvFlag = NanoParsedFlags
NanoArgsMap = List[Tuple[str, NanoPlainValue]]
NanoParsedArgsMap = List[Tuple[str, NanoParsedValue]]

# code(core): define Nano
class Nano:
    def __init__(self, flags: NanoParsedFlags, argv: NanoArgvs, extras: NanoExtras):
        self.flags = flags
        self.argv = argv
        self.extras = extras

# feat(core): parse stro or stra to nano
# docs(core): stra is short of string array
# docs(core): stro is short of string oline
def nanoargs(input: Union[str, List[str]]) -> Nano:
    # 1. 将输入转换为列表
    stra = nano_argv_stra_simple(input)
    # 2. 初始化extras和args
    extras: NanoExtras = []
    args: List[str] = []
    # 3. 分离出extras和头部参数
    result = nano_args_stra_decode(stra)
    extras = result["tail"]
    args = result["head"]
    # 4. 从头部参数中获取参数向量和参数映射
    result = nano_args_head_decode(args)
    argvs = result["argvs"]
    args_map = result["argsMap"]
    # 5. 获取标志（flags）
    flags = nano_args_head_kvp_decode(args_map)
    # 6. 解析标志中的值
    parsed_flags = nano_flag_parse(flags)
    return Nano(parsed_flags, argvs, extras)

def nano_argv_stra_simple(input: Union[str, List[str]]) -> List[str]:
    if isinstance(input, list):
        return input
    return input.split()


def nano_val_is_one_of_them(one: object, them: List[object], case_sensitive: bool = False) -> bool:
    def compare(a, b):
        if case_sensitive and isinstance(a, str) and isinstance(b, str):
            return a.lower() == b.lower()
        return a == b
    return any(compare(one, exp) for exp in them)


def nano_args_stra_decode(handled_input: List[str]) -> Dict[str, List[str]]:
    head = handled_input
    tail: List[str] = []
    if "--" in handled_input:
        index = handled_input.index("--")
        tail = handled_input[index + 1:]
        head = handled_input[:index]
    return {"tail": tail, "head": head}


def nano_args_head_decode(args: List[str]) -> Dict[str, Union[NanoArgvs, NanoArgsMap]]:
    argvs: NanoArgvs = []
    args_map: NanoArgsMap = []
    for i in range(len(args)):
        previous = args[i - 1] if i > 0 else None
        curr = args[i]
        next = args[i + 1] if i < len(args) - 1 else None
        next_is_value = next and not next.startswith("--") and not next.startswith("-")
        def push_with_next(x):
            args_map.append((x, next if next_is_value else "true"))
        if "=" in curr:
            key, value = curr.split("=")
            args_map.append((key, value))
        elif curr.startswith("-") and not curr.startswith("--"):
            current = curr
            if "=" in current:
                index = current.index("=")
                args_map.append((current[index - 1], current[index + 1]))
                current = current[:index - 1] + current[index + 2:]
            xyz = current[1:]
            for char in xyz[:-1]:
                args_map.append((char, "true"))
            final = xyz[-1]
            push_with_next(final)
        elif curr.startswith("--") or curr.startswith("-"):
            push_with_next(curr)
        else:
            value_taken = any(arg[0] == previous for arg in args_map)
            if not value_taken and previous and previous.startswith("-"):
                previous_char = previous[-1]
                value_taken = any(arg[0] == previous_char for arg in args_map)
            if not value_taken:
                argvs.append(curr)
    return {"argvs": argvs, "argsMap": args_map}


def nano_args_head_kvp_decode(args_map: NanoArgsMap) -> NanoFlags:
    result: NanoFlags = {}
    for item in args_map:
        key = item[0].lstrip("-")
        value = item[1]
        if key.startswith("no-") and nano_val_is_one_of_them(value, [None, True, "", "true"]):
            key = key[3:]
            value = "false"
        result[key] = value
    return result


def nano_flag_parse(flag: Union[NanoStrvFlag, NanoJssvFlag]) -> NanoParsedFlags:
    def parse_value(v):
        if v.lower() in ["true", "yes"]:
            return True
        elif v.lower() in ["false", "no"]:
            return False
        try:
            return int(v)
        except ValueError:
            return v
    res: NanoParsedFlags = {}
    for key, value in flag.items():
        res[key] = parse_value(value)
    return res


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_data = sys.argv[1:] if len(sys.argv) > 2 else sys.argv[1]
        parsed = nanoargs(input_data)
        print(f"Parsed argv: {parsed.argv}")
        print(f"Parsed flags: {parsed.flags}")
        print(f"Parsed extras: {parsed.extras}")
    else:
        print("Please provide command line arguments to parse.")

# python python/nano.py --help
# python python/nano.py audio/read -a -b -c -- -a -b -c