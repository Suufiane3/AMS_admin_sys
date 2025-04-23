import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Adresse Gmail
email_expediteur = "ton.email@gmail.com"
mdp = "mot_de_passe_application"

# Adresse universitaire de destination
email_destinataire = "prenom.nom@univ-exemple.fr"

# Lire le contenu de template.txt
with open("template.txt", "r", encoding="utf-8") as fichier:
    corps = fichier.read()

# Sujet et contenu
sujet = "Crisis situation!"

# Construction de l'email
message = MIMEMultipart()
message["From"] = email_expediteur
message["To"] = email_destinataire
message["Subject"] = sujet
message.attach(MIMEText(corps, "plain"))

# Connexion sécurisée au serveur SMTP de Gmail
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
    serveur.login(email_expediteur, mdp)
    serveur.send_message(message)

print("Email envoyé avec succès !")
