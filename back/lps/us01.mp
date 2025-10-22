c_channel(calculadora, pc_01, pc_02)

SEQ{
	int a = line();
	int b = line();
	
	calculadora.send('+', a, b, a + b)
	
	print(calculadora.print())
}

