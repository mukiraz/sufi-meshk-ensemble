# translation.py within your app directory
from modeltranslation.translator import register, TranslationOptions
from .models import GroupMember, FAQ, Update, Event

@register(GroupMember)
class GroupMemberTranslationOptions(TranslationOptions):
    fields = ('instrument_duty', 'short_description', 'description')

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

@register(Update)
class UpdateTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description')

@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('event_name', 'description', 'place', 'category', 'organizer', 'status', 'contact_info', 'tags')

    