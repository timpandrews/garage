from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(TemplateView):
    template_name = "pages/contact.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"


class FAQView(TemplateView):
    template_name = "pages/faq.html"

