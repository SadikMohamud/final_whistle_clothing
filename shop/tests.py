from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from .models import HomepageCard


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

	def test_story_page_renders_webp_assets(self):
		response = self.client.get("/story/")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "shop/images/story/fwc-studio-01.webp")
		self.assertContains(response, "shop/images/story/fwc-studio-02.webp")
		self.assertContains(response, "shop/images/story/fwc-detail-main.webp")
		self.assertContains(response, "shop/images/story/fwc-03.webp")
		self.assertContains(response, "shop/images/story/fwc-04.webp")

	def test_privacy_policy_page_renders_professional_copy(self):
		response = self.client.get("/privacy-policy/")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Privacy Policy")
		self.assertContains(response, "Collecting personal information")
		self.assertContains(response, "Cookies and tracking technologies")

	def test_shipping_page_renders_professional_copy(self):
		response = self.client.get("/shipping/")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Shipping Policy")
		self.assertContains(response, "Drop 1 - Ready to ship")
		self.assertContains(response, "Drop 2 - Made to order")

	def test_returns_page_renders_professional_copy(self):
		response = self.client.get("/returns/")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Refund Policy")
		self.assertContains(response, "Orders may be returned within 14 days of receipt")
		self.assertContains(response, "Refunds are typically processed within 7-10 business days")

	def test_terms_page_renders_professional_copy(self):
		response = self.client.get("/terms-of-service/")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Terms of Service")
		self.assertContains(response, "Overview")
		self.assertContains(response, "Governing law and changes")


@override_settings(
	STORAGES={
		"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
		"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
	},
)
class HomepageHeroCardTests(TestCase):
	def test_homepage_uses_admin_managed_hero_card(self):
		HomepageCard.objects.create(
			title="Hero One",
			subtitle="Hero subtitle",
			price_label="FWC",
			is_active=True,
			sort_order=0,
			image=SimpleUploadedFile("hero-one.jpg", b"hero-image", content_type="image/jpeg"),
		)
		non_hero = HomepageCard.objects.create(
			title="Card Two",
			subtitle="Second card",
			price_label="FWC",
			is_active=True,
			sort_order=1,
		)

		with patch("shop.views.fetch_storefront_products", return_value=[]), patch(
			"shop.views.fetch_products_by_query", return_value=[]
		):
			response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["hero_card"].title, "Hero One")
		self.assertEqual(len(response.context["homepage_cards"]), 1)
		self.assertEqual(response.context["homepage_cards"][0].id, non_hero.id)
