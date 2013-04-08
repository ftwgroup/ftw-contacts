import csv
from contacts.models import Contact, Tag
from django.core.exceptions import MultipleObjectsReturned

def handle_uploaded_file(doc):
    docreader = csv.reader(doc)
    flash = []     # list of two-ples
    
    for row_id, row in enumerate(docreader):
        if row_id == 0:
            continue
        contact_dict = {}
        contact_dict['first_name'] = row[0].lower()
        contact_dict['last_name'] = row[1].lower()
        contact_dict['phone_primary'] = row[2]
        contact_dict['email'] = row[3].lower()

        tags_list = row[4].split(',')

        contact, created = create_contact(contact_dict)
        if created:
            flash.append(("success", "%s was created." % contact.full_name()))
        else:
            flash.append(("error", "%s already exists. Contact updated." % contact.full_name()))

        create_tags(tags_list, contact)

    return flash

def create_tags(tags_list, contact):
    for el in tags_list:
        tag_dict = {}
        tag_dict['tag'] = el.lower()
        tag, created = Tag.objects.get_or_create(**tag_dict)
        contact.tags.add(tag)
        
def create_contact(contact_dict):
    """
    takes a contact dictionary and gets or creates by email
    if no email, gets or creates by phone #
    if record has not been matched creates a brand new contact, otherwise, updates contact
    
    """
    try:
        # email is present and exists in db
        if contact_dict['email'] and len(Contact.objects.filter(email=contact_dict['email'])):
            contact, created = Contact.objects.get_or_create(email=contact_dict['email'])
        elif contact_dict['phone_primary'] and len(Contact.objects.filter(phone_primary=contact_dict['phone_primary'])):
            contact, created = Contact.objects.get_or_create(phone_primary=contact_dict['phone_primary'])
        else:
            contact, created = Contact.objects.get_or_create(email=contact_dict['email'])
    # probably means that email and/or phone is empty
    except MultipleObjectsReturned:
        contact = Contact()
        created = True

    # this double saves
    for key, value in contact_dict.iteritems():
        if value:     # only update non-blank values
            setattr(contact, key, value)
    contact.save()

    return (contact, created)
