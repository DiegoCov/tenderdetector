import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ORIGEN, EMAIL_PASSWORD, EMAIL_DESTINO

def enviar_correo(reportes, fecha):
    if not reportes:
        asunto = f"TenderDetector — Sin procesos relevantes ({fecha})"
        cuerpo = f"""Escaneo del {fecha} completado.

No se encontraron procesos relevantes para C&N Solutions en SEACE hoy.

— TenderDetector"""
    else:
        asunto = f"TenderDetector — {len(reportes)} proceso(s) relevante(s) ({fecha})"
        cuerpo = f"Escaneo del {fecha} — {len(reportes)} proceso(s) para revisar:\n\n"
        cuerpo += "=" * 60 + "\n\n"
        for r in reportes:
            cuerpo += f"📋 {r['titulo']}\n"
            cuerpo += f"Entidad: {r['entidad']}\n"
            cuerpo += f"Monto: S/. {r['monto']:,.0f}\n"
            cuerpo += f"Score: {r['score']}%\n\n"
            cuerpo += r['reporte']
            cuerpo += "\n\n" + "=" * 60 + "\n\n"
        cuerpo += "— TenderDetector"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ORIGEN

    destinatarios = EMAIL_DESTINO.split(",")
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_ORIGEN, destinatarios, msg.as_string())
        print(f"✅ Correo enviado a {EMAIL_DESTINO}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        return False