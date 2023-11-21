from django.urls import path

from .views import AboutView, ContactView, FAQView, PrivacyView, TermsView

app_name = "pages"

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("terms/", TermsView.as_view(), name="terms"),
]