from typing import Dict, Any, TypeVar, List, Type

T = TypeVar("T")
R = TypeVar("R", Dict[str, Any], List[Any])


def cc2sc_key(key: str) -> str:
    new_key: str = ""
    for c in key:
        if c.isupper():
            new_key += "_"
            c = c.lower()
        new_key += c
    return new_key


def sc2cc_key(key: str) -> str:
    new_key: str = ""
    u: bool = False

    for c in key:
        if c == "_":
            u = True
        else:
            if u:
                c = c.upper()
                u = False
            new_key += c

    return new_key


def cc2sc(input_dict: R) -> R:
    if isinstance(input_dict, dict):
        output: Dict[str, Any] = {}
        for key in input_dict.keys():
            parsed_key: str = ""
            for e in key:
                if e.isupper():
                    parsed_key += "_"
                    e = e.lower()

                parsed_key += e

            if isinstance(input_dict[key], (dict, list)):
                output[parsed_key] = cc2sc(input_dict[key])
            else:
                output[parsed_key] = input_dict[key]
        return output

    output: List[Any] = []
    for e in input_dict:
        if isinstance(e, (dict, list)):
            output.append(cc2sc(e))

        else:
            output.append(e)

    return output


def parse_type_list(input_list: List[Dict[str, Any]], output_type: Type[T]) -> List[T]:
    output: List[output_type] = []
    iterator: Dict[str, Any]

    for iterator in input_list:
        output.append(output_type.from_dict(iterator))

    return output
