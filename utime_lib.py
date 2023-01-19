import requests
from datetime import datetime as dt
import datetime
from datetime import timedelta

class utime_web():
	def __init__(self, user, passwd):
		self.user = user
		self.passwd = passwd
		self.session = requests.Session()

	def login(self):
		""" Login """
		data = {'login': self.user, 'passwd': self.passwd}
		self.session.post('https://utime.cosmotime.be/login.php',  data=data)

	def pointer(self, autologin=True):
		""" Pointe à l'heure actuelle """
		if autologin:
			self.login()
		data = {'clocking': "IN / OUT"}
		self.session.post('https://utime.cosmotime.be/clocking.php',  data=data)

	def récupérer_pointages(self, fromdate, todate, autologin=True):
		""" Récupérer les pointages dans la plage donnée """

		if fromdate > todate:
			raise ValueError("La date de début doit être antérieure à la date de fin !")

		if fromdate.year != todate.year:
			raise ValueError("Les dates de début et de fin doivent être dans la même année !")

		if type(fromdate) != datetime.date or type(todate) != datetime.date:
			raise ValueError("Les dates doivent être au format datetime.date !")

		if autologin:
			self.login()

		# On envoie la requête avec les données du rapport à générer
		data = {
			'report': '11',
			'pdate': dt.strftime(fromdate, "%d-%m-%Y"),
			'pdateto': dt.strftime(todate, "%d-%m-%Y"),
			'format':'CSV',
			'confirm': "Envoyer"
			}
		
		self.session.cookies["rpt_format"] = "CSV"
		response = self.session.post('https://utime.cosmotime.be/reportreq.php', data=data, allow_redirects=False) # 

		# On regarde si on récupère bien le lien du fichier
		file_url = response.headers.get("Location")
		if file_url is None:
			return None

		# On récupère le fichier généré
		response = self.session.get(f"https://utime.cosmotime.be/{file_url}")
		print(response.text)

		# On crée une liste avec le fichier
		data = [item.split(";") for item in response.text.split("\n")[2:-2]]
		data_return = []

		for day in data:
			error = False
			date = dt.strptime(day[0][3:], '%d-%m').date().replace(year=fromdate.year)
			# Selon le type d'horaire, on déduit le temps à prester
			if day[1] == "10":
				temps_à_prester = "0:0"
			elif day[1] == "48":
				temps_à_prester = "8:15"
			elif day[1] == "49":
				temps_à_prester = "7:00"


			# S'il y a un temps à prester, on récupère les pointages
			if temps_à_prester != "0:0":
				heure_debut = dt.strptime(day[3], '%H:%M').time()
				heure_fin = dt.strptime(day[4], '%H:%M').time()
				# Calcul si la différence des pointages est égale à le journée pour détecter un éventuel problème
				heure_debut_delta = timedelta(hours=heure_debut.hour, minutes=heure_debut.minute)
				heure_fin_delta = timedelta(hours=heure_fin.hour, minutes=heure_fin.minute)
				total_jour = dt.strptime(day[6], "%H:%M").time()
				total_jour_delta = timedelta(hours=total_jour.hour, minutes=total_jour.minute)
				# Dans le calcul on ajoute une pause de 30min
				if (heure_fin_delta - heure_debut_delta) != total_jour_delta + timedelta(minutes=45):
					error = True

				print(heure_fin_delta-heure_debut_delta)
			else:
				heure_debut = 0
				heure_fin = 0

			data_return.append([date,heure_debut,heure_fin, error])

		return data_return


		


	def récupérer_effectifs(self, autologin=True):
		""" Récupérer les effectifs par secteur """

		if autologin:
			self.login()

		response = self.session.get("https://utime.cosmotime.be/present.php")
		table_raw = response.text.split("<table class='clocking'")[1].split("</form>")[0].replace("</tr>", "")
		table_lines = table_raw.split("<tr>")[2:-1]
		data = {}
		for line in table_lines:
			
			cells = line.replace("</td>", "").split("<td")[1:]
			# Si service
			if "class='minititletd'" in cells[0]:
				service = cells[0].split("&nbsp;")[-1].replace("&amp;", "&").replace("&rsquo;", "'")
				data[service] = []
			else:
				for cell in cells:
					# print(cell)
					if not "span" in cell:
						continue
					name = cell.split("] ")[1].split("</span>")[0]
					data[service].append(name)

		return data