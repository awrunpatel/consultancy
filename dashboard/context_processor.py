from dashboard.models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.first()  
    
    if settings:
        return {
            'website_name': settings.website_name,
            'location': settings.location,
            'website_fav': settings.website_fav,
            'website_logo': settings.website_logo,


            'contact_email': settings.contact_email,
            'contact_number': settings.contact_number,
        }
    
    return {
        'website_name': '',
        'location': '',
        'website_fav': '',
        'website_logo': '',
        'contact_email': '',
        'contact_number': '',
    }