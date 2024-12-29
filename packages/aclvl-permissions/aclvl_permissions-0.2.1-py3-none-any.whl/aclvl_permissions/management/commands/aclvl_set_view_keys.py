from django.core.management.base import BaseCommand
from django.urls import get_resolver
from aclvl_permissions.models import AccessLevel

class Command(BaseCommand):
    help = 'Lists all declared views, their view_key values, and creates/retrieves AccessLevel objects for their required_access_levels'

    def handle(self, *args, **kwargs):
        # Fetch all URL patterns from the root URL resolver
        url_resolver = get_resolver()
        url_patterns = url_resolver.url_patterns

        self.stdout.write("Processing Declared Views:\n")

        for pattern in url_patterns:
            try:
                view = pattern.callback  # Get the view function/class

                # Fetch `view_key` and `required_access_levels` from the view
                view_key = getattr(view, 'view_key', None)
                required_access_levels = getattr(view, 'required_access_levels', None)

                if view_key and required_access_levels:
                    self.stdout.write(f"\nView: {view.__module__}.{view.__name__}")
                    self.stdout.write(f"View Key: {view_key}")
                    self.stdout.write(f"Required Access Levels: {required_access_levels}")

                    # Create or get AccessLevel objects
                    for access_key in required_access_levels:
                        access_level, created = AccessLevel.objects.get_or_create(
                            name=access_key.replace('_', ' ').title(),  # Format name (e.g., "View All User")
                            access_key=access_key
                        )
                        if created:
                            self.stdout.write(f"  - Created AccessLevel: {access_level.name} ({access_level.access_key})")
                        else:
                            self.stdout.write(f"  - AccessLevel Exists: {access_level.name} ({access_level.access_key})")
                else:
                    self.stdout.write(f"\nView: {view.__module__}.{view.__name__} has no view_key or required_access_levels.")
            except AttributeError:
                # Handle patterns without a valid callback
                self.stdout.write(f"\nPattern {pattern} has no callable view.")