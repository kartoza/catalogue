from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userena.models import UserenaSignup
from smtplib import SMTPException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Resend activation emails to users who are inactive and have not expired.'

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=False)
        resent_count = 0
        error_count = 0

        for user in users:
            try:
                signup = UserenaSignup.objects.get(user=user)

                if not signup.activation_key_expired():
                    self.stdout.write(f"Attempting to resend activation email to {user.email}...")

                    try:
                        signup.send_activation_email()
                        resent_count += 1
                        self.stdout.write(self.style.SUCCESS(f"✔ Email sent to {user.email}"))
                    except SMTPException as smtp_err:
                        error_count += 1
                        logger.error(f"SMTP error sending to {user.email}: {smtp_err}")
                        self.stderr.write(self.style.ERROR(f"✖ SMTP error sending to {user.email}: {smtp_err}"))
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Failed to send email to {user.email}: {e}")
                        self.stderr.write(self.style.ERROR(f"✖ Failed to send email to {user.email}: {e}"))

                else:
                    self.stdout.write(f"Activation key expired for {user.email}, skipping.")

            except UserenaSignup.DoesNotExist:
                self.stderr.write(self.style.WARNING(f"No UserenaSignup profile for user: {user.username}, skipping."))

        self.stdout.write(self.style.SUCCESS(f"\nFinished: {resent_count} emails sent, {error_count} errors."))
