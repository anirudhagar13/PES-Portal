function check_fields()
{
	pass1 = document.getElementById("pass");
	pass2 = document.getElementById("confirmpass");
	passdontmatch = document.getElementById("passdontmatch");
	
	if(pass1.value != pass2.value)
	{
		pass1.value = "";
		pass2.value = "";
		passdontmatch.innerHTML = "Passwords Don't Match. Please Enter Again";
		return false;
	}
	return true;
}