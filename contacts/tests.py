import os, shutil, tempfile
from django.test import TestCase
from contacts.models import Contact, Tag
from contacts.helpers import handle_uploaded_file, create_contact, create_tags
from contacts.factories import TagFactory, ContactFactory
from account.factories import AccountFactory
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned


class ContactModelTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            first_name="Foo",
            last_name="BaR",
            phone_primary="8182884760",
            email="ThENoToRiOuSBuI@GMAIL.com")
        self.contact2 = Contact.objects.create(
            first_name="James",
            last_name="Murphy",
            phone_primary="2123134114",
            email="james@murphy.com")

        self.tag = Tag.objects.create(tag="DONOR")

   
    def test_full_name_with_contact(self):
        """
        full_name() should return First Name + Last Name for a contact
        """
        self.assertEqual(self.contact.full_name(), "Foo Bar")

    def test_contact_is_saved_in_all_lowercase(self):
        """
        save all attributes in all lowercase
        """
        self.assertEqual(self.contact.first_name, "foo")
        self.assertEqual(self.contact.last_name, "bar")
        self.assertEqual(self.contact.phone_primary, "8182884760")
        self.assertEqual(self.contact.email, "thenotoriousbui@gmail.com")

    def test_tag_is_saved_in_all_lowercase(self):
        self.assertEqual(self.tag.tag, "donor")

    def test_create_contact_helper(self):
        # all same but email AND phone
        contact_dict = {}
        contact_dict['first_name'] = "James"
        contact_dict['last_name'] = "Murphy"
        contact_dict['phone_primary'] = "1111111111"
        contact_dict['email'] = "james@differentmurphy.com"
        
        contact, created = create_contact(contact_dict)
        self.assertEqual(True, created)
        self.assertEqual(2, len(Contact.objects.filter(last_name="murphy")))
      
    def test_create_contact_helper_with_dupe_email(self):
        contact_dict = {}
        contact_dict['first_name'] = "Jim"
        contact_dict['last_name'] = "Murphy"
        contact_dict['phone_primary'] = "2223334444"
        contact_dict['email'] = "james@murphy.com"
        
        contact, created = create_contact(contact_dict)

        self.assertEqual(1, len(Contact.objects.filter(email="james@murphy.com")))

        # contact should be updated b/c matching email
        cont = Contact.objects.get(email="james@murphy.com")
        self.assertEqual(False, created)
        self.assertEqual("jim", cont.first_name)
        self.assertEqual("2223334444", cont.phone_primary)
        self.assertEqual("james@murphy.com", cont.email)

    def test_create_contact_helper_with_dupe_phone(self):
        contact_dict = {}
        contact_dict['first_name'] = "Jamie"
        contact_dict['last_name'] = "Murphy"
        contact_dict['phone_primary'] = "2123134114"
        contact_dict['email'] = ""

        contact, created = create_contact(contact_dict)

        self.assertEqual(1, len(Contact.objects.filter(phone_primary="2123134114")))

        # contact should be updated b/c matching phone
        cont = Contact.objects.get(phone_primary="2123134114")
        self.assertEqual(False, created)
        self.assertEqual("jamie", cont.first_name)
        self.assertEqual("2123134114", cont.phone_primary)
        self.assertEqual("james@murphy.com", cont.email)

    def test_create_contact_helper_no_email_or_phone(self):
        contact_dict = {}
        contact_dict['first_name'] = "James"
        contact_dict['last_name'] = "Murphy"
        contact_dict['phone_primary'] = ""
        contact_dict['email'] = ""        

        contact, created = create_contact(contact_dict)
        
        self.assertEqual(True, created)

    def test_handle_uploaded_file(self):
        with open("contacts/test/testcsv.csv", 'r') as f:
            results = handle_uploaded_file(f)

        # all were created
        self.assertEqual(6, len(results))
        self.assertEqual("success", results[0][0])
        self.assertEqual("success", results[1][0])
        self.assertEqual("success", results[2][0])
        self.assertEqual("success", results[3][0])
        self.assertEqual("success", results[4][0])
        self.assertEqual("success", results[5][0])

    def test_handle_uploaded_file_with_updates(self):
        """
        identifies 3 types of contacts: new, update, duplicate
        based on email, or phone # if email not found
        """
        with open('contacts/test/testupdates.csv', 'r') as f:
            results = handle_uploaded_file(f)

        # 3 created, 1 dupe
        self.assertEqual(4, len(results))
        self.assertEqual("success", results[0][0])
        self.assertEqual("error", results[1][0])
        self.assertEqual("success", results[2][0])
        self.assertEqual("error", results[3][0])

    def test_handle_uploaded_file_with_duplicates(self):
        """
        """
        with open('contacts/test/testdupes.csv', 'r') as f:
            results = handle_uploaded_file(f)

        # 3 created, 1 dupe
        self.assertEqual(4, len(results))
        self.assertEqual("success", results[0][0])
        self.assertEqual("success", results[1][0])
        self.assertEqual("error", results[2][0])
        self.assertEqual("error", results[3][0])

    def test_audit_trail_updated_on_crud(self):
        # initial save
        self.assertEqual(1, self.contact.history.count())
        self.assertEqual(1, len(self.contact.history.filter(_audit_change_type="I")))

        # update
        self.contact.last_name = "quxx"
        self.contact.save()
        self.assertEqual(2, self.contact.history.count())
        self.assertEqual(1, len(self.contact.history.filter(_audit_change_type="U")))

        # delete
        history_count = Contact.history.count()
        self.contact.delete()
        self.assertEqual(history_count+1, Contact.history.count())
        self.assertEqual(1, len(Contact.history.filter(_audit_change_type="D")))

        
      
class ContactViewTests(TestCase):
    def test_index_view(self):
        """
        Make sure /contacts responds with 200
        """
        response = self.client.get(reverse("list"))
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        """
        Make sure /contacts/:id responds with 200
        """
        response = self.client.get(reverse("detail", args=(1,)))
        self.assertEqual(response.status_code, 404)

        contact = Contact.objects.create(first_name="Foo", last_name="Bar")
        response = self.client.get(reverse("detail", args=(contact.id,)))
        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """
        Make sure /contacts/new responds with 200
        """
        response = self.client.get(reverse("new"))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse("new"))

    def test_upload_view(self):
        """
        Make sure /contacts/upload responds with 200
        """
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

    def test_upload_csv(self):
        """
        """
        with open('contacts/test/testcsv.csv', 'r') as f:
            response = self.client.post(reverse("upload"), {'docfile': f})

            # check redirect
            # self.assertRedirects(response, reverse("list"))

            # zack morris
            mock_zack = ContactFactory.build(first_name="Zack",
                                        last_name="Morris",
                                        phone_primary="818",
                                        email="a@b.com",
                                        tags="student,attendee,person")
            mock_zack.id = 1
            real_zack = Contact.objects.get(pk=1)
            self.assertEqual(mock_zack, real_zack)
            self.assertEqual(len(mock_zack.tags.all()), len(real_zack.tags.all()))

            # julian threatt
            mock_julian = ContactFactory.build(first_name="Julian",
                                               last_name="Threatt",
                                               phone_primary="213",
                                               email="j@t.com",
                                               tags="donor,student")
            mock_julian.id = 1
            real_julian = Contact.objects.get(pk=1)
            self.assertEqual(mock_julian, real_julian)   
