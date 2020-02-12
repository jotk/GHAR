import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


class DBconnect:
	""" Creates a mysql database connection and can retreive data from and manipulate database
	"""
	def __init__(self, myhost, mydatabase, myuser, mypassword):
		try:
			self.connection = psycopg2.connect('postgres://fobbrjymfkyckh:fd8354e7a3dc154e0091e2d76517b8db16ee089ecc9f99fba382a55829be0f0f@ec2-174-129-33-27.compute-1.amazonaws.com:5432/dcav41js00j9a5')
			# self.connection = psycopg2.connect(host=myhost, dbname=mydatabase, user=myuser, password=mypassword)
			self.cursor = self.connection.cursor()
		except Exception as e:
			print("Error while connecting to MySQL", e)

	def commitTime(self):
		self.connection.commit()

	def closeConnection(self):
		try:
			self.cursor.close()
			self.connection.close()
			print("PostgreSQL connection is closed successfully.")
		except Exception as e:
			print("Cannot close, maybe connection or cursor not open")

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

	def getEmail(self, userID):
		sql = "select email from landlords where id_landlord= %s"
		val = (userID,)
		self.cursor.execute(sql, val)
		name = self.cursor.fetchone()
		if name is not None:  # if no lines are returned then acronym doesn't exist
			return name[0]
		else:
			return "Cannot get email"

	def getLastName(self, userID):
		sql = "select lastname from landlords where id_landlord= %s"
		val = (userID,)
		self.cursor.execute(sql, val)
		name = self.cursor.fetchone()
		if name is not None:  # if no lines are returned then acronym doesn't exist
			return name[0]
		else:
			return "Cannot get name"

	def getPropertyList(self, userID):
		sql = "select id_property from properties where id_landlord = %s;"
		val = (userID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchall()
		if result is not None:  # if no lines are returned then acronym doesn't exist
			propIDList = []
			for x in result:
				print(x)
				propIDList.append(x[0])
			return propIDList
		else:
			return "Cannot get list"

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

	def checkUser(self, email, password):
		sql = "select id_landlord, password from landlords where email= %s"
		val = (email,)
		self.cursor.execute(sql, val)
		id = self.cursor.fetchone()
		if id is None:
			return (False, None)
		else:
			hash = id[1]
			# hash = generate_password_hash(id[1]) #**
			if check_password_hash(hash, password):
				return (True, id[0])
			else:
				return (False, None)

	def checkUserWithHash(self, id, passHash):
		sql = "select password from landlords where id_landlord= %s"
		val = (id,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res is None:
			return (False, None)
		else:
			hash = generate_password_hash(res[1])
			if hash == passHash:
				return (True, id)
			else:
				return (False, None)

	def retHashedPass(self, id):
		sql = "select password from landlords where id_landlord= %s"
		val = (id,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res is None:
			return (False, None)
		else:
			hash = generate_password_hash(res[0])
			return (True, hash)

	def addMaintainenceReq(self, userID, propID, contractorID, issueType, notes, dateScheduled):
		sql = "insert into maintainence(requestor_id, properties_id_property, contractors_id_contractor, issueType, dayOf, notes) values(%s,%s,%s,%s,%s,%s);"
		val = (userID, propID, contractorID, issueType, notes, dateScheduled)
		self.cursor.execute(sql, val)
		self.connection.commit()

	def getAlerts(self, userID):
		paramList = ["id_maintainence", "notes", "dateOfAlert", "id_contractor", "id_property", "id_landlord",
					 "issueType"]
		sql = "select * from maintainence where requestor_id= %s"
		val = (userID,)
		self.cursor.execute(sql, val)
		alerts = self.cursor.fetchall()
		# print("Result:", alerts)
		if alerts is None:
			return []
		else:
			listOfAlerts = []
			for row in alerts:
				alertDict = dict(zip(paramList, list(row)))
				listOfAlerts.append(alertDict)
			return listOfAlerts

	def addAlert(self, userID, title, description, cont, prop, dat):
		sql = "insert into maintainence(issueType, notes, contractors_id_contractor, properties_id_property, dayOf, requestor_id)" \
			  "values (%s,%s,%s,%s,%s)"
		val = (title, description, cont, prop, dat, userID)
		print("val", val)
		self.cursor.execute(sql, val)
		self.connection.commit()

	def changeFirstname(self, userID, fname):
		sql1 = "update landlords set firstname=%s where id_landlord=%s"
		val1 = (fname, userID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def changeLastname(self, userID, lname):
		sql1 = "update landlords set lastname=%s where id_landlord=%s"
		val1 = (lname, userID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def changeEmail(self, userID, email):
		sql1 = "update landlords set email=%s where id_landlord=%s"
		val1 = (email, userID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def changePassword(self, userID, passw):
		sql1 = "update landlords set password=%s where id_landlord=%s"
		val1 = (passw, userID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setUniqueIdent(self, uniqID, userID):  # TODO: Make the rand int be created within sql
		sql = "select * from uniq_to_id where id_landlord=%s"  # checks if the uniqID entry for that user already exists
		val = (userID,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res is not None:  # update value
			sql1 = "update uniq_to_id set uniq=%s where id_landlord=%s"
			val1 = (uniqID, userID)
			self.cursor.execute(sql1, val1)
			self.connection.commit()  # prob don't want this here, idk how to put this after the final check in this fun
		else:  # insert value
			sql1 = "insert into uniq_to_id(uniq, id_landlord) values (%s,%s)"
			val1 = (uniqID, userID)
			self.cursor.execute(sql1, val1)
			self.connection.commit()
		sql2 = "select uniq from uniq_to_id where id_landlord=%s"
		val2 = (userID,)
		self.cursor.execute(sql2, val2)
		res = self.cursor.fetchone()
		print(res)
		if res is not None and res[0] == uniqID:
			print("The unique ID: ", uniqID)
			return uniqID
		else:
			return None

	def getIdFromUniq(self, uniqID):
		sql = "select id_landlord from uniq_to_id where uniq=%s"
		val = (uniqID,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res != None:
			return res[0]
		else:
			return None

	def getContractorListofDict(self, userID):
		# implement propName if possible, only val giving error
		paramList = ["id_contractor", "firstname", "lastname", "speciality", "phone", "email",
					 "active", "id_landlord"]
		sql = "select * from contractors where id_landlord = %s;"
		val = (userID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchall()
		if result is not None:  # if no lines are returned then acronym doesn't exist
			listOfDicts = []
			for row in result:
				contIDDict = dict(zip(paramList, list(row)))
				listOfDicts.append(contIDDict)
			return listOfDicts
		else:
			return []
			print("Cannot get dictionary of contractors")

	def getLeaseListofDict(self, propertyID):
		# implement propName if possible, only val giving error
		paramList = ["id_tenant", "id_lease", "leaseLen", "startDate", "begCondition", "endCondition",
					 "damages", "active", "propertyID", "monthlyRent", "id_landlord", "isRentPayed"]
		sql = "select * from leaseDetails where propertyID=%s;"
		val = (propertyID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchall()
		if result is not None:  # if no lines are returned then acronym doesn't exist
			listOfDicts = []
			for row in result:
				contIDDict = dict(zip(paramList, list(row)))
				listOfDicts.append(contIDDict)
			return listOfDicts
		else:
			return []
			print("Cannot get dictionary of lease details")

	def getPropertyListofDict(self, userID):
		# implement propName if possible, only val giving error
		paramList = ["id_property", "buyingPrice", "sellingPrice", "active", "buyDate", "sellDate",
					 "avgRentalArea", "marketGrowth", "id_landlord", "streetAddress", "city", "state", "zipcode",
					"propName", "imageName", "monthlyMortgage"]
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

	def getImageName(self, userID):
		sql = "select imageName from landlords where id_landlord=%s"
		val = (userID,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res != None:
			return res[0]
		else:
			return None

	# return "default.png"

	def setImageName(self, userID, imgname):
		sql1 = "update landlords set imageName=%s where id_landlord=%s"
		val1 = (imgname, userID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setRentPayed(self, stat, leaseID):
		sql1 = "update leaseDetails set isRentPayed=%s where id_lease=%s"
		val1 = (stat, leaseID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def getTenantInfo(self, homeID):
		# implement propName if possible, only val giving error
		paramList = ["id_tenant", "prevAdress", "forwardingAdress", "firstname", "lastname", "phone", "email",
					 "homeID"]
		sql = "select * from tenants where homeID = %s;"
		val = (homeID,)
		self.cursor.execute(sql, val)
		result = self.cursor.fetchone()
		if result is not None:  # if no lines are returned then acronym doesn't exist
			contIDDict = dict(zip(paramList, list(result)))
			return contIDDict
		else:
			return {}
			print("Cannot get tenant info")

	def setPropertyName(self, newname, propID):
		sql1 = "update properties set propName=%s where id_property=%s"
		val1 = (newname, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setPropertyStreetAddress(self, newaddress, propID):
		sql1 = "update properties set streetAddress=%s where id_property=%s"
		val1 = (newaddress, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setPropertyCity(self, city, propID):
		sql1 = "update properties set city=%s where id_property=%s"
		val1 = (city, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setPropertyZipcode(self, zipcode, propID):
		sql1 = "update properties set zipcode=%s where id_property=%s"
		val1 = (zipcode, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setPropertyState(self, state, propID):
		sql1 = "update properties set state=%s where id_property=%s"
		val1 = (state, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setPropertyActivation(self, isactive, propID):
		sql1 = "update properties set active=%s where id_property=%s"
		val1 = (isactive, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def setBoughtPrice(self, newprice, propID):
		sql1 = "update properties set buyingPrice=%s where id_property=%s"
		val1 = (newprice, propID)
		self.cursor.execute(sql1, val1)
		self.connection.commit()

	def hasAPIBeenCalled(self, propID):
		sql = "select id_property from apicall where id_property=%s"
		val = (propID,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res != None:
			return True
		else:
			return False


	def getApiCallJSON(self, propID):
		sql = "select JSONdata from apicall where id_property=%s"
		val = (propID,)
		self.cursor.execute(sql, val)
		res = self.cursor.fetchone()
		if res != None:
			return res[0]
		else:
			return None

	def setAPICallJSON(self, propID, jsonresponse):
		if self.hasAPIBeenCalled(propID) == True:  # update value
			sql1 = "update apicall set JSONdata=%s where id_property=%s"
			val1 = (jsonresponse, propID)
			self.cursor.execute(sql1, val1)
		else:  # insert value
			sql1 = "insert into apicall(JSONdata, id_property) values (%s,%s)"
			val1 = (jsonresponse, propID)
			self.cursor.execute(sql1, val1)

	def checkEmail(self, email):
		sql = "select id_landlord, password from landlords where email= %s"
		val = (email,)
		self.cursor.execute(sql, val)
		id = self.cursor.fetchone()
		if id is None: # User does not exist
			return False
		else: # User exists
			return True

	def addUser(self, fname, lname, email, password):
		hashed = generate_password_hash(password)
		sql = "insert into landlords (firstname, lastname, email, password) values (%s, %s, %s, %s);"
		val = (fname, lname, email, hashed)
		try:
			self.cursor.execute(sql, val)
		except Exception as e:
			print("ERROR:", e)

