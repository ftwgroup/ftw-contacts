import factory
from contacts.models import Tag, Contact
from account.factories import AccountFactory


class TagFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Tag

    tag = 'asdf'

class ContactFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact

    first_name = "first"
    last_name = "last"
    phone_primary = "818-288-4760"
    email = "julian@ftwgroup.com"
#    account = factory.SubFactory(AccountFactory)
    
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
