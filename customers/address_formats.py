"""
Country-specific address formats and field configurations
"""

# Address format configuration by country
ADDRESS_FORMATS = {
    'US': {
        'name': 'United States',
        'fields': ['street_address', 'apartment_suite', 'city', 'state', 'postal_code'],
        'postal_label': 'ZIP Code',
        'postal_pattern': r'^\d{5}(-\d{4})?$',
        'field_order': [
            {'name': 'street_address', 'label': 'Street Address', 'required': True},
            {'name': 'apartment_suite', 'label': 'Apt, Suite, etc.', 'required': False},
            {'name': 'city', 'label': 'City', 'required': True},
            {'name': 'state', 'label': 'State', 'required': True, 'type': 'select'},
            {'name': 'postal_code', 'label': 'ZIP Code', 'required': True},
        ],
        'phone_format': '(XXX) XXX-XXXX',
        'language': 'en-US'
    },
    'GB': {
        'name': 'United Kingdom',
        'fields': ['street_address', 'apartment_suite', 'city', 'postal_code'],
        'postal_label': 'Postcode',
        'postal_pattern': r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Street Address', 'required': True},
            {'name': 'apartment_suite', 'label': 'Flat/Building', 'required': False},
            {'name': 'city', 'label': 'City/Town', 'required': True},
            {'name': 'postal_code', 'label': 'Postcode', 'required': True},
        ],
        'phone_format': '+44 XXXX XXXXXX',
        'language': 'en-GB'
    },
    'NL': {
        'name': 'Netherlands',
        'fields': ['street_address', 'apartment_suite', 'postal_code', 'city'],
        'postal_label': 'Postcode',
        'postal_pattern': r'^\d{4}\s?[A-Z]{2}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Straatnaam', 'required': True},
            {'name': 'apartment_suite', 'label': 'Huisnummer/Toevoeging', 'required': False},
            {'name': 'postal_code', 'label': 'Postcode', 'required': True},
            {'name': 'city', 'label': 'Stad', 'required': True},
        ],
        'phone_format': '+31 6 XXXX XXXX',
        'language': 'nl-NL'
    },
    'DE': {
        'name': 'Germany',
        'fields': ['street_address', 'apartment_suite', 'postal_code', 'city'],
        'postal_label': 'Postleitzahl',
        'postal_pattern': r'^\d{5}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Straße', 'required': True},
            {'name': 'apartment_suite', 'label': 'Hausnummer/Zusatz', 'required': False},
            {'name': 'postal_code', 'label': 'Postleitzahl', 'required': True},
            {'name': 'city', 'label': 'Stadt', 'required': True},
        ],
        'phone_format': '+49 XXX XXXXXX',
        'language': 'de-DE'
    },
    'FR': {
        'name': 'France',
        'fields': ['street_address', 'apartment_suite', 'postal_code', 'city'],
        'postal_label': 'Code Postal',
        'postal_pattern': r'^\d{5}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Adresse', 'required': True},
            {'name': 'apartment_suite', 'label': 'Appartement/Bâtiment', 'required': False},
            {'name': 'postal_code', 'label': 'Code Postal', 'required': True},
            {'name': 'city', 'label': 'Ville', 'required': True},
        ],
        'phone_format': '+33 X XX XX XX XX',
        'language': 'fr-FR'
    },
    'BE': {
        'name': 'Belgium',
        'fields': ['street_address', 'apartment_suite', 'postal_code', 'city'],
        'postal_label': 'Code Postal',
        'postal_pattern': r'^\d{4}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Rue/Straße', 'required': True},
            {'name': 'apartment_suite', 'label': 'Numéro/Nummer', 'required': False},
            {'name': 'postal_code', 'label': 'Code Postal', 'required': True},
            {'name': 'city', 'label': 'Ville/Stad', 'required': True},
        ],
        'phone_format': '+32 X XX XX XX XX',
        'language': 'nl-BE'
    },
    'IT': {
        'name': 'Italy',
        'fields': ['street_address', 'apartment_suite', 'postal_code', 'city'],
        'postal_label': 'CAP',
        'postal_pattern': r'^\d{5}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Via/Strada', 'required': True},
            {'name': 'apartment_suite', 'label': 'Numero/Civico', 'required': False},
            {'name': 'postal_code', 'label': 'CAP', 'required': True},
            {'name': 'city', 'label': 'Città', 'required': True},
        ],
        'phone_format': '+39 XXX XXX XXXX',
        'language': 'it-IT'
    },
    'ES': {
        'name': 'Spain',
        'fields': ['street_address', 'apartment_suite', 'postal_code', 'city'],
        'postal_label': 'Código Postal',
        'postal_pattern': r'^\d{5}$',
        'field_order': [
            {'name': 'street_address', 'label': 'Calle', 'required': True},
            {'name': 'apartment_suite', 'label': 'Número/Piso', 'required': False},
            {'name': 'postal_code', 'label': 'Código Postal', 'required': True},
            {'name': 'city', 'label': 'Ciudad', 'required': True},
        ],
        'phone_format': '+34 XXX XX XX XX',
        'language': 'es-ES'
    },
}

# Default format (fallback)
DEFAULT_FORMAT = ADDRESS_FORMATS['NL']


def get_address_format(country_code):
    """
    Get address format for a specific country
    
    Args:
        country_code (str): ISO 3166-1 alpha-2 country code (e.g., 'NL', 'US')
    
    Returns:
        dict: Address format configuration for the country
    """
    return ADDRESS_FORMATS.get(country_code.upper(), DEFAULT_FORMAT)


def get_browser_language_to_country(language):
    """
    Map browser language code to country code
    
    Args:
        language (str): Browser language code (e.g., 'en-US', 'nl-NL')
    
    Returns:
        str: ISO country code (e.g., 'US', 'NL')
    """
    language_map = {
        'en-US': 'US',
        'en-GB': 'GB',
        'en-CA': 'US',
        'en-AU': 'GB',
        'nl': 'NL',
        'nl-NL': 'NL',
        'nl-BE': 'BE',
        'de': 'DE',
        'de-DE': 'DE',
        'de-AT': 'DE',
        'de-CH': 'DE',
        'fr': 'FR',
        'fr-FR': 'FR',
        'fr-BE': 'BE',
        'fr-CH': 'FR',
        'it': 'IT',
        'it-IT': 'IT',
        'es': 'ES',
        'es-ES': 'ES',
        'be': 'BE',
    }
    
    # Try exact match first
    if language in language_map:
        return language_map[language]
    
    # Try language prefix (e.g., 'en' from 'en-US')
    base_language = language.split('-')[0].lower()
    for lang_code, country in language_map.items():
        if lang_code.startswith(base_language):
            return country
    
    # Default fallback
    return 'NL'


def get_us_states():
    """Get list of US states for address form"""
    return [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    ]
