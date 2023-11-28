# Simple parser for HoI4 state files

from typing import List, Dict, Tuple, Any
import re


class Container:
	def __init__(self, name: str, children: List, parent: Any = None) -> None:
		self.name = name
		self.children = children
		self.parent = parent
		tabulation: int = 0
		self.tabulation = tabulation

	def __repr__(self) -> str:
		return self.name

	def __str__(self) -> str:
		retstr: str = ""
		for _ in range(self.tabulation-2):
			retstr += "\t"
		retstr += "%s = {" % self.name
		for x in self.children:
			retstr += "\n"
			for _ in range(self.tabulation):
				retstr += "\t"	
			if type(x) == Namespace:
				x.tabulation = self.tabulation
				retstr += str(x)
			else:
				x.tabulation = self.tabulation + 1
				retstr += str(x)
		retstr += "\n"
		for _ in range(self.tabulation-1):
			retstr += "\t"
		retstr += "}"
		return retstr


class Namespace:
	def __init__(self, name: str, value: str, parent: Container):
		self.name = name
		self.value = value
		self.parent = parent
		tabulation: int = 0
		self.tabulation = tabulation

	def __str__(self) -> str:
		retstr: str = ""
		for _ in range(self.tabulation):
			retstr += "\t"
		if self.name == self.value:
			# Dont return comments
			if re.match(r"\D+", self.name):
				return ""

			return f"{self.value}"
		else:
			return f"{self.name} = {self.value}"

	def __repr__(self) -> str:
		return self.name

class State:
	def __init__(self, filename: str, raw_text: str, cores: List[str] = [], claims: List[str] = [], owner: str = "", id: int = 0) -> None:
		values = parser(lexer(raw_text))
		#for x in state.children:
			#if x.name == "history":
			#	for idx, y in enumerate(x.children):
			#		print(y.name)
			#		if y.name == "add_core_of":
			#			cores.append(y.value)
			#		elif y.name == "add_claim_by":
			#			claims.append(y.value)
			#		elif y.name == "owner":
			#			owner = y.value
			#if re.match("id", x.name):
			#	id = int(x.value)

		#for x in state.children:
		#	if x.name == "history":
		#		x = [item for item in x.children if item.name != "add_core_of" or item.name != "add_claim_by" or item.name != "owner"]



		self.state = values[0]
		self.cores = values[1]
		self.claims = values[2]
		self.owner = values[3]
		self.id = values[4]
		self.filename = filename

	def write(self) -> None:
		# Convert cores, claims, owner back into namespaces
		self.state.children.insert(0, Namespace("id", self.id, self.state))
		for x in self.state.children:
			if x.name == "history":
				x.children.append(Namespace("owner", self.owner, x))
				for z in self.cores:
					x.children.append(Namespace("add_core_of", z, x))
				for z in self.claims:
					x.children.append(Namespace("add_claim_by", z, x))

		# Convert AST back into proper syntax
		writestr = str(self.state)
		with open("./states/" + self.filename, 'w') as f:
			f.write(writestr)


def lexer(raw_text: str) -> List[Tuple[str, str]]:
	tokens: Dict[str, str] = {
		r'[a-zA-Z_0-9."]+': 'NAMESPACE',
		r'=': 'EQUALS',
		r'{': 'ENTERSCOPE',
		r'}': 'EXITSCOPE',
		r'\s+': 'WHITESPACE',
	}

	lexed: List[Tuple[str, str]] = []

	token: List[str] = [r'[a-zA-Z_0-9."]+', ""]
	for c in list(raw_text):
		for r in tokens.keys():
			if re.match(r, c):
				if token[0] == r:
					token[1] += c
					break
				else:
					lexed_token: Tuple[str, str] = (tokens[token[0]], token[1])
					lexed.append(lexed_token)
					token = [r, c]
					break
	lexed = [x for x in lexed if x[0] != 'WHITESPACE']
	#for x in lexed[4:-1]:
	#	print(x)

	return lexed[2:]

def parser(lexed: List[Tuple[str, str]]) -> List:
	state: Container = Container("state", [])
	cores: List[str] = []
	claims: List[str] = []
	owner: str = ""
	id: int = 0
	parent: List[Container] = [state]
	iterlexed = iter(enumerate(lexed))
	for idx, t in iterlexed:
		if t[0] == "NAMESPACE":
			try:
				if lexed[idx+1][0] == "EQUALS":
					if lexed[idx+2][0] == "ENTERSCOPE":
						container = Container(t[1], [], parent[len(parent)-1])
						parent[len(parent)-1].children.append(container)
						parent.append(container)
						next(iterlexed)
						next(iterlexed)
					else:
						if t[1] == "add_core_of":
							cores.append(lexed[idx+2][1])
						elif t[1] == "add_claim_by":
							claims.append(lexed[idx+2][1])
						elif t[1] == "owner":
							owner = lexed[idx+2][1]
						elif t[1] == "id":
							id = int(lexed[idx+2][1])
						else:
							parent[len(parent)-1].children.append(Namespace(t[1], lexed[idx+2][1], parent[len(parent)-1]))
						next(iterlexed)
						next(iterlexed)
				else:
					parent[len(parent)-1].children.append(Namespace(t[1], t[1], parent[len(parent)-1]))
			except:
				pass
		elif t[0] == "EXITSCOPE":
			parent.pop()

	return [state, cores, claims, owner, id]