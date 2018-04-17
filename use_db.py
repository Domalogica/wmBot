
def add_branches_db(telegram, branch):
	result = connect_mysql.insert('branches', *["telegram", "branch"], **{'telegram': telegram, 'branch': branch})
	return result

def get_branch_db(telegram):
	conditional_query = "telegram = %s"
	result = connect_mysql.select("branches", conditional_query, *["branch"], **{'telegram': telegram})
	return result

def del_branch_db(telegram):
	result = connect_mysql.delete_branch(telegram)
	return result

def get_message_db(telegram):
	conditional_query = "telegram = %s"
	result = connect_mysql.select("message", conditional_query, *["message_id"], **{'telegram': telegram})
	return result

def add_message_db(telegram, message_id):
	result = connect_mysql.insert('message', *["telegram", "branch"], **{'telegram': telegram, 'message_id': message_id})
	return result

def del_message_db(telegram):
	conditional_query = 'telegram = %s'
	result = connect_mysql.delete('message', conditional_query, *[telegram])
	return result