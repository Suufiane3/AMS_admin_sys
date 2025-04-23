import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Adresse Gmail (personnelle)
email_expediteur = "ton.email@gmail.com"
mdp = "mot_de_passe_application"

# Adresse universitaire de destination
email_destinataire = "prenom.nom@univ-exemple.fr"

# Sujet et contenu
sujet = "Crisis situation!"
corps = "Bonjour,\n\nCeci est un test d’envoi d’email depuis un script Python vers mon email universitaire.\n\nBien cordialement."

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
