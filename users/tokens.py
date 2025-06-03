from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TenMinuteTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

token_generator = TenMinuteTokenGenerator()
