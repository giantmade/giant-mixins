from haystack import indexes


class SearchIndexMixin(indexes.SearchIndex):
    """
    Mixin to provide the standard `index_queryset` and
    `update_object` methods
    """

    plain_text = indexes.CharField()

    def index_queryset(self, using=None):
        """
        Overrides the default queryset to return only published objects
        """

        return super().index_queryset(using=using).published()

    def update_object(self, instance, using=None, **kwargs):
        """
        Custom update method to fix objects appearing blank in the index
        """
        if instance.is_published:
            return super().update_object(instance, using=using, **kwargs)
        return self.remove_object(instance, using=using)

    def prepare_plain_text(self, obj):
        """
        In order for a models plugin text to be indexed, we need to add a
        plain_text attribute which renders all of the relevant plugins into a
        single string.
        """
        if hasattr(obj, "plain_text"):
            return obj.plain_text
        return ""
