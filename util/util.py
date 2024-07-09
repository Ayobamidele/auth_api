
error_message_templates = {
			"firstName": {
				"missing": "First name is missing. Please provide a  first name.",
				"required": "First name is required. Please provide a valid first name.",
				"invalid": "Invalid First name format. Please enter a valid First name."
			},
			"lastName": {
				"missing": "Last name is missing. Please provide a last name.",
				"required": "Last name is required. Please provide a valid last name.",
				"invalid": "Invalid Last name format. Please enter a valid Last name."
			},
			"email": {
				"missing": "Email is missing. Please provide a valid email address.",
				"required": "Email is required. Please provide a valid email address.",
				"invalid": "Invalid email format. Please enter a valid email address."
			},
			"password": {
				"missing": "Password is missing. Please provide a valid Password.",
				"required": "Password is required. Please provide a valid Password.",
				"invalid": "Invalid Password format. Please enter a valid Password.",
				"string_too_short": "Password is too short"
			},
			"phone": {
				"invalid": "Invalid Phone format. Please enter a valid Phone number.",
				"missing": "Phone is missing. Please provide a valid Phone.",
				"required": "Phone is required. Please provide a valid Phone.",
			}
   }

def process_error(data):
	result = data
	print(data)
	data = []
	for i in result:
		field = i['loc'][-1]
		error_type = i['type']
		try:
			data.append({
				"field": field,
				"message": error_message_templates[field].get(error_type, f"Invalid {field} field format.")
			})
		except KeyError:
			data.append({
				"fields": "format",
				"message": "Invalid Request Format. Hint: missing fields."
			})

	return {"errors": data}

