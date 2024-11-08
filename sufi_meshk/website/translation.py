# translation.py within your app directory
from modeltranslation.translator import register, TranslationOptions
from .models import GroupMember, FAQ, Update, Event, Category, Tag, BlogPost, Author

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
    fields = ('event_name', 'description', 'place', 'category', 'tags')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_title','meta_description', 'meta_keywords', 'meta_author', 'og_title', 'og_description', 'twitter_card_type', 'short_description' , 'content')


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('position', 'short_description')