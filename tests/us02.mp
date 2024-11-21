PAR{
	int a = 1;
	int ans = 1;
	while(a < 10000){
		int temp = a + ans;
		print(temp)
		a = temp;
		ans = a;
	}
}

PAR{
	int a = 1;
	int ans = 1;

	while(a < 13){
		a = a * ans;
		print(a);

		ans = a;
		a = a + 1;
	}
}
	
