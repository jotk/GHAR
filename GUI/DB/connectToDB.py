import mysql.connector


class DBconnect:
	""" Creates a mysql database connection and can retreive data from and manipulate database
	"""
	def __init__(self, myhost, mydatabase, myuser, mypassword):
		try:
			self.connection = mysql.connector.connect(host=myhost, database=mydatabase, user=myuser, password=mypassword)

			if self.connection.is_connected():
				self.db_Info = self.connection.get_server_info()
				self.printServerSpec()
				self.cursor = self.connection.cursor()
				self.cursor.execute("select database();")
				self.record = self.cursor.fetchone()
				self.printDBSpec()

		except Exception as e:
			print("Error while connecting to MySQL", e)

	def printServerSpec(self):
		print("Connected to MySQL Server version ", self.db_Info)

	def printDBSpec(self):
		print("You're connected to database: ", self.record)

	def closeConnection(self):
		try:
			if self.connection.is_connected():
				self.cursor.close()
				self.connection.close()
				print("MySQL connection is closed successfully.")
		except Exception:
			print("No connection extablished in the first place.")

	def addUser(self, firstname, lastname, email, password):
		self.cursor.execute("insert into landlords(firstname, lastname, email, password) values (:1, :2, :3, :4);",
							(firstname, lastname, email, password))
		return self.cursor.execute("select id_landlord from landlords where email = ?", (email,))


	def checkUser(self, email, password):
		sql = "select id_landlord from landlords where (email= %s) AND (password= %s)"
		val = (email, password)
		self.cursor.execute(sql, val)
		id = self.cursor.fetchone()
		if id is None:  # if no lines are returned then acronym doesn't exist
			return (False, id)
		else:
			print("ID in connect to DB: ", id, " and ", id[0])
			return (True, id[0])

	def getFirstName(self, userID):
		sql = "select firstname from landlords where id_landlord= %s"
		print("This is user id: ", userID)
		val = (userID,)
		self.cursor.execute(sql, val)
		name = self.cursor.fetchone()
		if name is not None:  # if no lines are returned then acronym doesn't exist
			return name[0]
		else:
			return "Unknown Name"
	def getLastName(self, userID):
		sql = "select lastname from landlords where id_landlord= %s"
		val = (userID,)
		self.cursor.execute(sql, val)
		name = self.cursor.fetchone()
		if name is not None:  # if no lines are returned then acronym doesn't exist
			return name[0]
		else:
			return "Cannot get name"

	# def getPropertyList(self, userID):
	# 	sql = "select id_property from properties where id_landlord = %s;"
	# 	val = (userID,)
	# 	self.cursor.execute(sql, val)
	# 	result = self.cursor.fetchall()
	# 	if result is not None:  # if no lines are returned then acronym doesn't exist
	# 		propIDList = []
	# 		for x in result:
	# 			print(x)
	# 			propIDList.append(x[0])
	# 		return propIDList
	# 	else:
	# 		return "Cannot get list"

	def getFullAdrress(self, propID):
		sql = "select streetAddress, city, state, zipcode from properties where id_property = %s;"
		val = (propID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchone()
		if result is not None:  # if no lines are returned then acronym doesn't exist
			address = ""
			for x in result:
				address = address + str(x) + " "
			return address
		else:
			return "Cannot get full address"

	def getPropertyName(self, propID):
		sql = "select propertyName from properties where id_property = %s;"
		#print("In connecttodb: ",type(propID))
		val = (propID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchone()
		if result is not None:  # if no lines are returned then acronym doesn't exist
			return result
		else:
			return "Cannot get list"

	def getPropertyListofDict(self, userID):
		# implement propName if possible, only val giving error
		paramList = ["id_property", "buyingPrice", "sellingPrice", "active", "buyDate", "sellDate",
					 "avgRentalArea", "marketGrowth", "id_landlord", "streetAddress", "city", "state", "zipcode",
					 "id_tenant", "propName", "imageName", "monthlyMortgage"]
		sql = "select * from properties where id_landlord = %s;"
		val = (userID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchall()

		if result is not None:  # if no lines are returned then acronym doesn't exist
			listOfDicts = []
			for row in result:
				propIDDict = dict(zip(paramList, list(row)))
				listOfDicts.append(propIDDict)
			return listOfDicts
		else:
			return []
			print("Cannot get list of property dictionaries")
