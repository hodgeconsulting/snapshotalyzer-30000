"""Sacrament type definitions for the OCA sacramental records app.

Each sacrament type is described declaratively: the form, detail view,
register listing, CSV export, and certificate merge are all driven by
these definitions, so adding or adjusting a field only requires editing
this file.

Field types: text, date, textarea, select (requires "options").
"""

from collections import OrderedDict

# Parish settings merged into certificates and page headers.
SETTINGS_FIELDS = [
    {"key": "parish_name", "label": "Parish Name",
     "help": "e.g. Holy Trinity Orthodox Church"},
    {"key": "parish_city", "label": "Parish City & State",
     "help": "e.g. Springfield, Illinois"},
    {"key": "parish_address", "label": "Parish Street Address"},
    {"key": "diocese", "label": "Diocese",
     "help": "e.g. Diocese of the Midwest, Orthodox Church in America"},
    {"key": "rector", "label": "Rector",
     "help": "Name as it should appear on the certificate signature line, "
             "e.g. V. Rev. John Smith"},
    {"key": "parish_phone", "label": "Parish Phone (optional)"},
]

# Register-book reference fields, common to every record. These tie the
# electronic record to the physical register kept in the parish binder.
REGISTER_FIELDS = [
    {"key": "record_number", "label": "Entry No.",
     "help": "Sequential entry number in the parish register"},
    {"key": "volume", "label": "Volume"},
    {"key": "page", "label": "Page"},
]

SACRAMENTS = OrderedDict()

SACRAMENTS["baptism"] = {
    "title": "Baptisms & Chrismations",
    "singular": "Baptism / Chrismation",
    "certificate_title": "Certificate of Baptism and Chrismation",
    "date_field": "date_of_baptism",
    "register_columns": ["full_name", "date_of_baptism", "date_of_birth",
                         "sponsors", "celebrant"],
    "sections": [
        {"title": "Person Baptized", "fields": [
            {"key": "full_name", "label": "Full Name", "type": "text",
             "required": True,
             "help": "Legal name of the person baptized"},
            {"key": "name_in_religion", "label": "Name in Religion",
             "type": "text",
             "help": "Baptismal / patron saint name, if different"},
            {"key": "date_of_birth", "label": "Date of Birth",
             "type": "date", "required": True},
            {"key": "place_of_birth", "label": "Place of Birth",
             "type": "text", "help": "City, county, and state or country"},
        ]},
        {"title": "Parents", "fields": [
            {"key": "father_name", "label": "Father's Name", "type": "text"},
            {"key": "mother_name",
             "label": "Mother's Name (including maiden name)",
             "type": "text"},
        ]},
        {"title": "Sacrament", "fields": [
            {"key": "date_of_baptism", "label": "Date of Baptism",
             "type": "date", "required": True},
            {"key": "date_of_chrismation", "label": "Date of Chrismation",
             "type": "date",
             "help": "Leave blank if the same day as the Baptism"},
            {"key": "place_of_sacrament", "label": "Place of Sacrament",
             "type": "text",
             "help": "Leave blank to use the parish church"},
            {"key": "sponsors", "label": "Sponsors (Godparents)",
             "type": "textarea", "required": True},
            {"key": "celebrant", "label": "Officiating Clergy",
             "type": "text", "required": True},
            {"key": "assisting_clergy", "label": "Assisting Clergy",
             "type": "text"},
        ]},
        {"title": "Notes", "fields": [
            {"key": "notes", "label": "Notes", "type": "textarea"},
        ]},
    ],
}

SACRAMENTS["reception"] = {
    "title": "Receptions into the Church",
    "singular": "Reception into the Church",
    "certificate_title": "Certificate of Reception into the Orthodox Church",
    "date_field": "date_of_reception",
    "register_columns": ["full_name", "date_of_reception",
                         "mode_of_reception", "former_confession",
                         "celebrant"],
    "sections": [
        {"title": "Person Received", "fields": [
            {"key": "full_name", "label": "Full Name", "type": "text",
             "required": True},
            {"key": "name_in_religion", "label": "Name in Religion",
             "type": "text",
             "help": "Patron saint name taken upon reception, if any"},
            {"key": "date_of_birth", "label": "Date of Birth",
             "type": "date"},
            {"key": "place_of_birth", "label": "Place of Birth",
             "type": "text"},
        ]},
        {"title": "Prior Ecclesiastical Status", "fields": [
            {"key": "former_confession",
             "label": "Former Church / Confession", "type": "text",
             "required": True,
             "help": "e.g. Roman Catholic, Lutheran, Baptist"},
            {"key": "previous_baptism",
             "label": "Details of Previous Baptism", "type": "textarea",
             "help": "Church, place, and date of the previous baptism, "
                     "if known"},
        ]},
        {"title": "Reception", "fields": [
            {"key": "mode_of_reception", "label": "Mode of Reception",
             "type": "select", "required": True,
             "options": ["Holy Chrismation", "Confession of Faith"]},
            {"key": "date_of_reception", "label": "Date of Reception",
             "type": "date", "required": True},
            {"key": "place_of_sacrament", "label": "Place of Reception",
             "type": "text",
             "help": "Leave blank to use the parish church"},
            {"key": "sponsors", "label": "Sponsor(s)", "type": "textarea"},
            {"key": "celebrant", "label": "Officiating Clergy",
             "type": "text", "required": True},
        ]},
        {"title": "Notes", "fields": [
            {"key": "notes", "label": "Notes", "type": "textarea"},
        ]},
    ],
}

SACRAMENTS["marriage"] = {
    "title": "Marriages",
    "singular": "Marriage",
    "certificate_title": "Certificate of Marriage",
    "date_field": "date_of_marriage",
    "register_columns": ["groom_name", "bride_name", "date_of_marriage",
                         "witnesses", "celebrant"],
    "sections": [
        {"title": "Groom", "fields": [
            {"key": "groom_name", "label": "Full Name", "type": "text",
             "required": True},
            {"key": "groom_religion", "label": "Religion", "type": "text",
             "help": "e.g. Orthodox Christian"},
            {"key": "groom_residence", "label": "Residence", "type": "text"},
            {"key": "groom_marriage_number", "label": "Which Marriage",
             "type": "select", "options": ["First", "Second", "Third"]},
            {"key": "groom_parents", "label": "Parents", "type": "text"},
        ]},
        {"title": "Bride", "fields": [
            {"key": "bride_name", "label": "Full Name", "type": "text",
             "required": True},
            {"key": "bride_religion", "label": "Religion", "type": "text"},
            {"key": "bride_residence", "label": "Residence", "type": "text"},
            {"key": "bride_marriage_number", "label": "Which Marriage",
             "type": "select", "options": ["First", "Second", "Third"]},
            {"key": "bride_parents", "label": "Parents", "type": "text"},
        ]},
        {"title": "Sacrament", "fields": [
            {"key": "date_of_marriage", "label": "Date of Marriage",
             "type": "date", "required": True},
            {"key": "place_of_sacrament", "label": "Place of Marriage",
             "type": "text",
             "help": "Leave blank to use the parish church"},
            {"key": "witnesses", "label": "Witnesses / Sponsors",
             "type": "textarea", "required": True},
            {"key": "license_info", "label": "Civil Marriage License",
             "type": "text",
             "help": "License number and issuing county/state"},
            {"key": "celebrant", "label": "Officiating Clergy",
             "type": "text", "required": True},
        ]},
        {"title": "Notes", "fields": [
            {"key": "notes", "label": "Notes", "type": "textarea"},
        ]},
    ],
}

SACRAMENTS["funeral"] = {
    "title": "Funerals & Burials",
    "singular": "Funeral / Burial",
    "certificate_title": "Certificate of Christian Burial",
    "date_field": "date_of_funeral",
    "register_columns": ["full_name", "date_of_death", "date_of_funeral",
                         "place_of_interment", "celebrant"],
    "sections": [
        {"title": "The Departed", "fields": [
            {"key": "full_name", "label": "Full Name", "type": "text",
             "required": True},
            {"key": "date_of_birth", "label": "Date of Birth",
             "type": "date"},
            {"key": "age_at_death", "label": "Age at Death", "type": "text"},
            {"key": "date_of_death", "label": "Date of Death",
             "type": "date", "required": True},
            {"key": "place_of_death", "label": "Place of Death",
             "type": "text"},
            {"key": "cause_of_death", "label": "Cause of Death",
             "type": "text"},
            {"key": "last_sacraments", "label": "Last Sacraments Received",
             "type": "text",
             "help": "e.g. Confession, Holy Communion, Holy Unction"},
        ]},
        {"title": "Funeral & Interment", "fields": [
            {"key": "date_of_funeral", "label": "Date of Funeral Service",
             "type": "date", "required": True},
            {"key": "place_of_sacrament", "label": "Place of Funeral Service",
             "type": "text",
             "help": "Leave blank to use the parish church"},
            {"key": "place_of_interment",
             "label": "Place of Interment (Cemetery)", "type": "text"},
            {"key": "celebrant", "label": "Officiating Clergy",
             "type": "text", "required": True},
        ]},
        {"title": "Notes", "fields": [
            {"key": "notes", "label": "Notes", "type": "textarea"},
        ]},
    ],
}


def all_field_keys(stype):
    """Ordered list of every data field key for a sacrament type."""
    keys = []
    for section in SACRAMENTS[stype]["sections"]:
        for field in section["fields"]:
            keys.append(field["key"])
    return keys


def field_map(stype):
    """Mapping of field key -> field definition for a sacrament type."""
    fmap = {}
    for section in SACRAMENTS[stype]["sections"]:
        for field in section["fields"]:
            fmap[field["key"]] = field
    return fmap
