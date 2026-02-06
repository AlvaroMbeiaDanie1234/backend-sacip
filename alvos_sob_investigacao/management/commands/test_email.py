from django.core.management.base import BaseCommand
from alvos_sob_investigacao.email_utils import send_test_email


class Command(BaseCommand):
    help = 'Send a test email to verify email configuration'

    def handle(self, *args, **options):
        self.stdout.write('Sending test email...')
        
        try:
            success = send_test_email()
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Test email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to send test email')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error occurred: {str(e)}')
            )