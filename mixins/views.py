from django.core.exceptions import PermissionDenied

__all__ = ["ViewPassesTestMixin"]


class ViewPassesTestMixin:
    """
    Deny a request with PermissionError if test_func fails.
    Does not require the user to be authenticated.
    """

    def dispatch(self, *args, **kwargs):
        """Override dispatch to check the result of test_func."""
        if not self.test_func():
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)
