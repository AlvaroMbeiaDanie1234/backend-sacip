import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings


def send_email(to_email, subject, html_content, text_content=None):
    """
    Sends an email using the configured SMTP settings
    """
    # Email configuration from environment variables
    smtp_server = os.getenv('GOOGLE_CLIENTE', 'smtp.gmail.com')
    port = int(os.getenv('GOOGLE_PORT', '587'))
    sender_email = os.getenv('GOOGLE_USER', '')
    password = os.getenv('GOOGLE_PASSWORD_APLICATION', '')
    
    if not sender_email or not password:
        raise ValueError("Email configuration is missing. Please set GOOGLE_USER and GOOGLE_PASSWORD_APLICATION in environment variables.")
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email
    
    # Add HTML content to message
    message.attach(MIMEText(html_content, "html"))
    
    # Add plain text content if provided
    if text_content:
        message.attach(MIMEText(text_content, "plain"))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        print(f"📧 Subject: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def send_target_investigation_email(target, recipient_email, message_body="", subject=""):
    """
    Sends a specific email about a target under investigation
    """
    html_content = f"""
    <html>
      <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
         
          <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd;"><strong>Nome:</strong></td>
              <td style="padding: 8px; border: 1px solid #ddd;">{target.nome}</td>
            </tr>
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd;"><strong>Apelido:</strong></td>
              <td style="padding: 8px; border: 1px solid #ddd;">{target.apelido}</td>
            </tr>
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd;"><strong>Observações:</strong></td>
              <td style="padding: 8px; border: 1px solid #ddd;">{target.observacoes or 'N/A'}</td>
            </tr>
          </table>
          
          {f'<p><strong>Mensagem do Analista:</strong></p><p>{message_body}</p>' if message_body else ''}
          
          <p>Se você recebeu este e-mail, significa que está sendo mantido informado sobre este caso.</p>
          
          <br>
          <p>Atenciosamente,<br>
          <strong>Equipe SACIP</strong></p>
          
          <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
        </div>
      </body>
    </html>
    """
    
    # Use custom subject if provided, otherwise use default
    if subject:
        email_subject = subject
    else:
        email_subject = f"Informações do Alvo Sob Investigação - {target.nome}"
    
    return send_email(
        to_email=recipient_email,
        subject=email_subject,
        html_content=html_content
    )


def send_test_email():
    """
    Sends a test email to verify email configuration
    """
    # Get recipient email from environment or use a default
    recipient_email = os.getenv('TEST_RECIPIENT_EMAIL', 'telegramtesteamdm@gmail.com')
    
    html_content = """
    <html>
      <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #4CAF50;">SACIP - Sistema de Análise Criminal Integrado de Polícia</h1>
          </div>
          <h2 style="color: #4CAF50; text-align: center;">Email de Teste</h2>
          <p>Olá,</p>
          <p>Esta é uma mensagem de teste enviada a partir do sistema SACIP.</p>
          <p>Se você recebeu este e-mail, significa que a configuração de envio de e-mails está funcionando corretamente.</p>
          <br>
          <p>Atenciosamente,<br>
          <strong>Equipe SACIP</strong></p>
        </div>
      </body>
    </html>
    """
    
    subject = "Email de Teste - SACIP"
    
    return send_email(
        to_email=recipient_email,
        subject=subject,
        html_content=html_content
    )