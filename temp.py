import numpy as np


class Interpreter:
	def __init__(self, expr):
		self.expr = expr
		self.make_list()

	def make_list(self):
		operator_list = ['+', '-', '*', '/']
		constructor = []
		constructor_type = []
		for symb in self.expr:




			if symb in operator_list:
				constructor_type.append('operator')
			else:
				try:
					int(symb)
					constructor_type.append('number')
				except:
					constructor_type.append('variable')
			constructor.append(symb)

		print(constructor, constructor_type)



expression = '2x+3'
test = Interpreter(expression)
