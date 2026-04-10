from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
	EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
	DEFAULT_FROM_EMAIL="no-reply@finalwhistleclothing.com",
	STORAGES={
		"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
		"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
	},
)
class CustomerAuthFlowTests(TestCase):
	def setUp(self):
		self.user_email = "testuser@example.com"
		self.user_password = "StrongPass123!"
		self.user = get_user_model().objects.create_user(
			username=self.user_email,
			email=self.user_email,
			password=self.user_password,
		)

	def test_customer_login_page_renders(self):
		response = self.client.get(reverse("customer_login"))
		self.assertEqual(response.status_code, 200)

	def test_customer_profile_requires_authentication(self):
		response = self.client.get(reverse("customer_profile"))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse("customer_login"), response.url)

	def test_customer_login_success_redirects_to_profile(self):
		response = self.client.post(
			reverse("customer_login"),
			{"email": self.user_email, "password": self.user_password},
		)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("customer_profile"))

	def test_customer_logout_redirects_home(self):
		self.client.login(username=self.user_email, password=self.user_password)
		response = self.client.get(reverse("customer_logout"))
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, "/")

	def test_register_creates_user_and_shows_email_confirm(self):
		payload = {
			"email": "newuser@example.com",
			"password": "AnotherStrongPass123!",
			"password_confirm": "AnotherStrongPass123!",
			"first_name": "New",
			"last_name": "User",
		}
		response = self.client.post(reverse("customer_register"), payload)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "customers/email_confirm.html")
		self.assertTrue(get_user_model().objects.filter(username=payload["email"]).exists())

	def test_customer_password_reset_shortcut_redirects_to_allauth(self):
		response = self.client.get(reverse("customer_password_reset"))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/accounts/password/reset/")

	def test_allauth_password_reset_page_renders(self):
		response = self.client.get("/accounts/password/reset/")
		self.assertEqual(response.status_code, 200)
