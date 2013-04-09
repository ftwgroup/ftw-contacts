from django.contrib.auth.models import User
from django.db import models
from pennyblack.module.subscriber.models import NewsletterSubscriber, SubscriberGroup
#from account.models import Account
from django.contrib.localflavor.us.models import PhoneNumberField
import audit


def lower_all_str_attr(obj):
    for key, value in obj.__dict__.iteritems():
        if key == '_state' or not isinstance(value, str):
            continue
        setattr(obj, key, value.lower())

DONATION_TYPES = (
    (u'o', 'Online'),
    (u'c', 'Check')
)
class Donation(models.Model):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    type = models.CharField(max_length=1, choices=DONATION_TYPES)
    contact = models.ForeignKey('Contact')

class Tag(models.Model):
    """
    A tag is meta-data. Meta-data is a label. A label is REALLY a contact list.
    """
    tag = models.CharField(max_length=255)

    def __unicode__(self):
        return self.tag

    def save(self, *args, **kwargs):
        lower_all_str_attr(self)
        return super(Tag, self).save(*args, **kwargs)

class Contact(models.Model):
    """
    A contact is a subscriber is a contact
    """
    title = models.CharField(verbose_name="job title", max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_primary = PhoneNumberField(verbose_name="primary phone", null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    #account = models.ForeignKey(Account, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    donations = models.ManyToManyField(Donation, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    referred_us_to = models.ManyToManyField('self', blank=True, null=True) # we may add in custom join table
    subscriber = models.OneToOneField(NewsletterSubscriber, blank=True, null=True)

    history = audit.AuditTrail(show_in_admin=True)


    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return ("%s %s" % (self.first_name, self.last_name)).title()

    def get_tags(self):
        tags = map(lambda x: x.tag, self.tags.all())
        return ','.join(tags)
    
    def save(self, *args, **kwargs):
        lower_all_str_attr(self)
        if not self.subscriber and self.email:
            subscriber = NewsletterSubscriber(email=self.email)
            subscriber.save()
            subscriber.groups.add(SubscriberGroup.objects.get(name='All'))
            self.subscriber = subscriber
        return super(Contact, self).save(*args, **kwargs)

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Note(models.Model):
    """
    Not using django's models because we want to to be able save a comment and change task details at the same time
    """
    author = models.ForeignKey(User)
    task = models.ForeignKey(Contact, related_name='notes')
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __unicode__(self):
        return '%s - %s' % (self.author, self.date)
