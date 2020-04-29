function validateUsername(input)
{
	if (input.value.includes(" "))
		input.setCustomValidity("Spaces aren't allowed")
	else if (!input.value.match("^[_0-9A-Za-z-]+$"))
		input.setCustomValidity("Only numbers, letters, underscores, and dashes are allowed")
	else
		input.setCustomValidity("")		
}
