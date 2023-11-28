# Alternate HoI4 state management tool
# Able to:
# - Set state ownership, claims, and cores on a large scale
# - Make a country 'release' all their cores of a certain tag
# - And more! Built to flexibly do whatever task is needed

from typing import List, Tuple, Any
from parser import State
import os


def main() -> None:
    os.system("cls")
    base_path: str = openAsStr("path.txt")
    states_path: str = base_path + "\\history\\states\\"
    edited_states_path: str = ".\\states\\"
    state_filenames: List[str] = os.listdir(states_path)
    edited_state_filenames: List[str] = os.listdir(edited_states_path)
    # Github stinky
    edited_state_filenames.remove("githubstinky.txt")
    pruned_state_filenames: List[str] = list(set(state_filenames) - set(edited_state_filenames))
    states: List[State] = []
    for x in pruned_state_filenames:
        y = states_path + x
        states.append(State(x, openAsStr(y)))
    for x in edited_state_filenames:
        y = edited_states_path + x
        states.append(State(x, openAsStr(y)))
    stack: List[State] = []
        
	# Display usage information
    print(openAsStr("./help.txt"))

    cmd: str = ""
    while cmd != "exit":
        cmd = input("> ")
        cmd_args: List[str] = cmd.split()
        attributes_strings = cmd_args[1:]
        attributes: List[Tuple[str, str, List[str]]] = []
        for x in attributes_strings:
            attributes.append(parseAttr(x))
        os.system("cls")
        if cmd_args[0] == "pull":
            stack += pull(attributes[0], states)
        elif cmd_args[0] == "set" and len(cmd_args) == 3:
            stack += set_(attributes[0], attributes[1], stack)
        elif cmd_args[0] == "set" and len(cmd_args) == 2:
            stack += set_(("!", "id", ["-1"]), attributes[0], stack)
        elif cmd_args[0] == "clear" and len(cmd_args) == 1:
            stack = []
        elif cmd_args[0] == "clear" and len(cmd_args) == 2:
            stack = list(set(stack) - set(pull(attributes[0], stack)))
        elif cmd_args[0] == "push":
            for x in stack:
                x.write()
            print("Stack written to /states")
            stack = []
        elif cmd_args[0] == "help":
            print(openAsStr("./help.txt"))
        elif cmd_args[0] == "examples":
            print(openAsStr("./examples.txt"))
        elif cmd_args[0] == "implementation":
            print(openAsStr("./implementation.txt"))
        elif cmd_args[0] == "exit":
            break

        stack = list(set(stack))
        stack = sorted(stack, key = lambda x: x.owner + str(x.id))
        print(tabulate(stack))


def parseAttr(attr: str) -> Tuple[str, str, List[str]]:
    # Parses attribute into tuple of (modifier, attribute, [values])
    tokens: List[str] = ["&","@","!"]
    broken_attr: List[str] = list(attr)
    mod: str = "~"
    attr_prime: str = ""
    if broken_attr[0] in tokens:
        mod = broken_attr[0]
        attr_prime = attr[1:attr.index(":")]
    else:
        attr_prime = attr[0:attr.index(":")]
    affected_states: str = attr.split(":")[1]
    affected_states_prime: List[str] = affected_states.split(",")
    return (mod, attr_prime, affected_states_prime)


def any_of(l1: List[Any], l2: List[Any]) -> bool:
    if type(l2) == int:
        l2 = [l2 for x in range(1)]
        l1 = [int(x) for x in l1]
    for x in l1:
        if x in l2:
            return True

    return False


def all_of(l1: List[Any], l2: List[Any]) -> bool:
    for x in l1:
        if x in l2:
            pass
        else:
            return False
        
    return True


def pull(attr: Tuple[str, str, List[str]], states: List[State]) -> List[State]:
    tokens: dict[str, str] = {
            "id":    "id",
            "tag":   "owner",
            "owner": "owner",
            "core":  "cores",
            "claim": "claims"
    }
    return_stack: List[State] = []
    if attr[0] == "~":
        for x in states:
            if any_of(attr[2], getattr(x, tokens[attr[1]])):
                return_stack.append(x)
    if attr[0] == "&":
        for x in states:
            if all_of(attr[2], getattr(x, tokens[attr[1]])):
                return_stack.append(x)
    if attr[0] == "@":
        for x in states:
            if set(attr[2]) == set(getattr(x, tokens[attr[1]])):
                return_stack.append(x)
    if attr[0] == "!":
        for x in states:
            if not any_of(attr[2], getattr(x, tokens[attr[1]])):
                return_stack.append(x)

    return return_stack


def set_(attr1: Tuple[str, str, List[str]], attr2: Tuple[str, str, List[str]], stack: List[State]) -> List[State]:
    return_stack: List[State] = pull(attr1, stack)
    tokens: dict[str, str] = {
        "id":    "id",
        "tag":   "owner",
        "core":  "cores",
        "claim": "claims"
    }
    if attr2[1] == "id":
        print("Error: State IDs are immutable")
    elif attr2[1] == "owner" or attr2[1] == "tag":
        for x in return_stack:
            setattr(x, "owner", attr2[2][0])
    elif attr2[0] == "~":
        for x in return_stack:
            attribute = getattr(x, tokens[attr2[1]])
            setattr(x, tokens[attr2[1]], attribute + attr2[2]) 
#if attr2[0] == "&":
#    for x in return_stack:
#        setattr(x, attr2[1], attribute + attr2[2]) 
    elif attr2[0] == "@":
        for x in return_stack:
            setattr(x, tokens[attr2[1]], attr2[2]) 
    elif attr2[0] == "!":    
        for x in return_stack:
            attribute = getattr(x, tokens[attr2[1]])
            setattr(x, tokens[attr2[1]], list(set(attribute) - set(attr2[2])))
                
    return return_stack

def tabulate(stack: List[State]) -> str:
    if len(stack) == 0:
        return "ID  Tag  Cores  Claims  "
    return_str = ""
    id_col_len: int = max(map(lambda x: x.id, stack))
    id_col_len = len(str(id_col_len))
    owner_col_len: int = 3
    cores_col_len: int = max(map(len, map(lambda x: ", ".join(x.cores), stack)))
    cores_col_len = max(cores_col_len, len("Cores"))
    claims_col_len: int = max(map(len, map(lambda x: ", ".join(x.claims), stack)))
    claims_col_len = max(claims_col_len, len("Claims"))
    # Add some offsets
    id_col_len += 2
    owner_col_len += 2
    cores_col_len += 2
    claims_col_len += 2

    return_str += insertInSpace("ID", id_col_len)
    return_str += insertInSpace("Tag", owner_col_len)
    return_str += insertInSpace("Cores", cores_col_len)
    return_str += insertInSpace("Claims", claims_col_len)
    for x in stack:
        return_str += "\n"
        return_str += insertInSpace(str(x.id), id_col_len)
        return_str += insertInSpace(x.owner, owner_col_len)
        return_str += insertInSpace(", ".join(x.cores), cores_col_len)
        return_str += insertInSpace(", ".join(x.claims), claims_col_len)

    return return_str

def insertInSpace(insert: str, space: int) -> str:
    return_str_list: List[str] = [" " for x in range(space)]
    broken_insert: List[str] = list(insert)
    for i, x in enumerate(broken_insert):
        return_str_list[i] = x
    return "".join(return_str_list)

def openAsStr(path: str) -> str:
    # Opens a file and returns its contents as a string.
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


if __name__ == "__main__":
    main()
