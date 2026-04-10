"""
Custom password validators for customer account security rules.
"""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomerPasswordPolicyValidator:
	"""
	Enforce password policy:
	- At least 8 characters
	- At least 1 special character
	- At least 3 digits
	"""

	special_pattern = re.compile(r"[^A-Za-z0-9]")

	def validate(self, password, user=None):
		if len(password) < 8:
			raise ValidationError(
				_("Password must be at least 8 characters long."),
				code="password_too_short",
			)

		if not self.special_pattern.search(password):
			raise ValidationError(
				_("Password must contain at least one special character."),
				code="password_no_special",
			)

		digit_positions = [i for i, ch in enumerate(password) if ch.isdigit()]
		if len(digit_positions) < 3:
			raise ValidationError(
				_("Password must contain at least three numbers."),
				code="password_not_enough_digits",
			)

	def get_help_text(self):
		return _(
			"Your password must be at least 8 characters long, include one special "
			"character, and include at least three numbers."
		)
