from django.test import TestCase, override_settings


@override_settings(
	STORAGES={
		"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
		"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
	},
)
class LanguageMiddlewareTests(TestCase):
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
