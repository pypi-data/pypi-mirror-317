from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from aclvl_permissions.models import AccessLevel


class Command(BaseCommand):
    help = 'Sets view keys for all declared views and ensures AccessLevel objects are created.'

    def handle(self, *args, **kwargs):
        # Get the root URL resolver
        url_resolver = get_resolver()
        self.stdout.write("Processing Declared Views:\n")

        # Recursively process URL patterns
        self._process_patterns(url_resolver.url_patterns)

    def _process_patterns(self, patterns, prefix=""):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):  # A single view pattern
                self._process_view(pattern, prefix)
            elif isinstance(pattern, URLResolver):  # A nested resolver
                self.stdout.write(f"Entering nested pattern: {pattern.pattern}")
                self._process_patterns(pattern.url_patterns, prefix + str(pattern.pattern))

    def _process_view(self, pattern, prefix):
        try:
            # Get the view callback
            view = pattern.callback
            view_key = getattr(view, 'view_key', None)
            required_access_levels = getattr(view, 'required_access_levels', None)

            # For viewsets, extract attributes from the view class
            if hasattr(view, 'cls'):
                view_key = getattr(view.cls, 'view_key', view_key)
                required_access_levels = getattr(view.cls, 'required_access_levels', required_access_levels)

            if view_key and required_access_levels:
                self.stdout.write(f"\nView: {view.__module__}.{view.__name__}")
                self.stdout.write(f"URL Pattern: {prefix}{pattern.pattern}")
                self.stdout.write(f"View Key: {view_key}")
                self.stdout.write(f"Required Access Levels: {required_access_levels}")

                # Create or get AccessLevel objects
                for access_key in required_access_levels:
                    access_level, created = AccessLevel.objects.get_or_create(
                        name=access_key.replace('_', ' ').title(),
                        access_key=access_key
                    )
                    if created:
                        self.stdout.write(f"  - Created AccessLevel: {access_level.name} ({access_level.access_key})")
                    else:
                        self.stdout.write(f"  - AccessLevel Exists: {access_level.name} ({access_level.access_key})")
            else:
                self.stdout.write(f"\nPattern {prefix}{pattern.pattern} has no view_key or required_access_levels.")
        except Exception as e:
            self.stdout.write(f"Error processing pattern {prefix}{pattern.pattern}: {e}")
