from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model


@override_settings(
	STORAGES={
		"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
		"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
	},
)
class LanguageMiddlewareTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="cachetest@example.com",
			email="cachetest@example.com",
			password="StrongPass123!",
		)

	def test_defaults_to_english_when_no_language_selected(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.client.session.get("fwc_lang"), "en")

	def test_persists_nl_when_selected(self):
		first_response = self.client.get("/?lang=nl")
		self.assertEqual(first_response.status_code, 200)
		self.assertEqual(self.client.session.get("fwc_lang"), "nl")

		second_response = self.client.get("/")
		self.assertEqual(second_response.status_code, 200)
		self.assertEqual(self.client.session.get("fwc_lang"), "nl")

	def test_invalid_lang_falls_back_to_english(self):
		response = self.client.get("/?lang=fr")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.client.session.get("fwc_lang"), "en")

	def test_homepage_html_is_publicly_cacheable_for_anonymous(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Cache-Control"], "public, max-age=3600, must-revalidate")

	def test_auth_paths_are_never_cacheable(self):
		response = self.client.get("/account/login/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Cache-Control"], "no-store, max-age=0")

	def test_authenticated_profile_page_is_never_cacheable(self):
		self.client.force_login(self.user)
		response = self.client.get("/account/profile/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Cache-Control"], "no-store, max-age=0")
