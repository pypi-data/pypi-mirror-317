"""Form widgets for the django-tomselect package."""

import logging
from typing import Any, Dict, Optional

from django import forms
from django.urls import NoReverseMatch, resolve, reverse, reverse_lazy

from django_tomselect.app_settings import (
    GLOBAL_DEFAULT_CONFIG,
    AllowedCSSFrameworks,
    ProxyRequest,
    TomSelectConfig,
    merge_configs,
)
from django_tomselect.autocompletes import (
    AutocompleteIterablesView,
    AutocompleteModelView,
)
from django_tomselect.middleware import get_current_request

logger = logging.getLogger(__name__)


class TomSelectWidgetMixin:
    """Mixin to provide methods and properties for all TomSelect widgets."""

    template_name = "django_tomselect/tomselect.html"

    def __init__(self, config=None, **kwargs):
        """Initialize shared TomSelect configuration.

        Args:
            config: a TomSelectConfig instance that provides all configuration options
            **kwargs: additional keyword arguments that override config values
        """
        # Merge user provided config with global defaults
        base_config = GLOBAL_DEFAULT_CONFIG
        if config is not None:
            if isinstance(config, TomSelectConfig):
                final_config = merge_configs(base_config, config)
            elif isinstance(config, dict):
                final_config = merge_configs(base_config, TomSelectConfig(**config))
            else:
                raise TypeError(f"config must be a TomSelectConfig or a dictionary, not {type(config)}")
        else:
            final_config = base_config

        # Set common configuration attributes
        self.url = final_config.url
        self.value_field = final_config.value_field
        self.label_field = final_config.label_field
        self.filter_by = final_config.filter_by
        self.exclude_by = final_config.exclude_by
        self.use_htmx = final_config.use_htmx

        self.minimum_query_length = final_config.minimum_query_length
        self.preload = final_config.preload
        self.highlight = final_config.highlight
        self.open_on_focus = final_config.open_on_focus
        self.placeholder = final_config.placeholder
        self.max_items = final_config.max_items
        self.max_options = final_config.max_options
        self.css_framework = final_config.css_framework
        self.use_minified = final_config.use_minified
        self.close_after_select = final_config.close_after_select
        self.hide_placeholder = final_config.hide_placeholder
        self.load_throttle = final_config.load_throttle
        self.loading_class = final_config.loading_class
        self.create = final_config.create

        # Initialize plugin configurations
        self.plugin_checkbox_options = final_config.plugin_checkbox_options
        self.plugin_clear_button = final_config.plugin_clear_button
        self.plugin_dropdown_header = final_config.plugin_dropdown_header
        self.plugin_dropdown_footer = final_config.plugin_dropdown_footer
        self.plugin_dropdown_input = final_config.plugin_dropdown_input
        self.plugin_remove_button = final_config.plugin_remove_button

        # Allow kwargs to override any config values
        for key, value in kwargs.items():
            if hasattr(final_config, key):
                if isinstance(value, dict):
                    setattr(self, key, {**getattr(final_config, key), **value})
                else:
                    setattr(self, key, value)

        super().__init__(**kwargs)

    def render(
        self,
        name: str,
        value: Any,
        attrs: dict[str, str] | None = None,
        renderer=None,
    ) -> str:
        """Render the widget."""
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)

    def get_plugin_context(self) -> dict[str, Any]:
        """Get context for plugins."""
        plugins = {}

        # Add plugin contexts only if plugin is enabled
        if self.plugin_clear_button:
            plugins["clear_button"] = self.plugin_clear_button.as_dict()

        if self.plugin_remove_button:
            plugins["remove_button"] = self.plugin_remove_button.as_dict()

        if self.plugin_dropdown_header:
            header_dict = self.plugin_dropdown_header.as_dict()
            if isinstance(self.plugin_dropdown_header.extra_columns, dict):
                header_dict["extra_headers"] = list(self.plugin_dropdown_header.extra_columns.values())
                header_dict["extra_values"] = list(self.plugin_dropdown_header.extra_columns.keys())
            plugins["dropdown_header"] = header_dict

        if self.plugin_dropdown_footer:
            plugins["dropdown_footer"] = self.plugin_dropdown_footer.as_dict()

        # These plugins don't have additional config
        plugins["checkbox_options"] = bool(self.plugin_checkbox_options)
        plugins["dropdown_input"] = bool(self.plugin_dropdown_input)

        return plugins

    def get_autocomplete_url(self):
        """Hook to specify the autocomplete URL."""
        return self.get_url(self.url, "autocomplete URL")

    def get_autocomplete_params(self):
        """Hook to specify additional autocomplete parameters."""
        params = []
        autocomplete_view = self.get_autocomplete_view()
        if not autocomplete_view:
            return params

        if params:
            return f"{'&'.join(params)}"
        return ""

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)

        # Add required data attributes
        if self.url:
            attrs["data-autocomplete-url"] = reverse_lazy(self.url)
        if self.value_field:
            attrs["data-value-field"] = self.value_field
        if self.label_field:
            attrs["data-label-field"] = self.label_field

        if self.placeholder is not None:
            attrs["placeholder"] = self.placeholder

        return {**attrs, **(extra_attrs or {})}

    @staticmethod
    def get_url(view_name, view_type: str = "", **kwargs):
        """Reverse the given view name and return the path.

        Fail silently with logger warning if the url cannot be reversed.
        """
        if view_name:
            try:
                return reverse_lazy(view_name, **kwargs)
            except NoReverseMatch as e:
                logger.warning(
                    "TomSelectIterablesWidget requires a resolvable '%s' attribute. Original error: %s",
                    view_type,
                    e,
                )
        return ""

    @property
    def media(self):
        """Return the media for rendering the widget."""

        if self.css_framework.lower() == AllowedCSSFrameworks.BOOTSTRAP4.value:
            css = {
                "all": [
                    (
                        "django_tomselect/vendor/tom-select/css/tom-select.bootstrap4.min.css"
                        if self.use_minified
                        else "django_tomselect/vendor/tom-select/css/tom-select.bootstrap4.css"
                    ),
                    "django_tomselect/css/django-tomselect.css",
                ],
            }
        elif self.css_framework.lower() == AllowedCSSFrameworks.BOOTSTRAP5.value:
            css = {
                "all": [
                    (
                        "django_tomselect/vendor/tom-select/css/tom-select.bootstrap5.min.css"
                        if self.use_minified
                        else "django_tomselect/vendor/tom-select/css/tom-select.bootstrap5.css"
                    ),
                    "django_tomselect/css/django-tomselect.css",
                ],
            }
        else:
            css = {
                "all": [
                    (
                        "django_tomselect/vendor/tom-select/css/tom-select.default.min.css"
                        if self.use_minified
                        else "django_tomselect/vendor/tom-select/css/tom-select.default.css"
                    ),
                    "django_tomselect/css/django-tomselect.css",
                ],
            }

        media = forms.Media(
            css=css,
            js=[
                (
                    "django_tomselect/js/django-tomselect.min.js"
                    if self.use_minified
                    else "django_tomselect/js/django-tomselect.js"
                )
            ],
        )
        return media


class TomSelectModelWidget(TomSelectWidgetMixin, forms.Select):
    """A Tom Select widget with model object choices."""

    def __init__(self, config=None, **kwargs):
        """Initialize widget with model-specific attributes."""
        self.model = None

        # Auth override settings
        self.allow_anonymous = kwargs.pop("allow_anonymous", False)
        self.skip_authorization = kwargs.pop("skip_authorization", False)

        # Initialize URL-related attributes
        self.show_list = False
        self.show_detail = False
        self.show_create = False
        self.show_update = False
        self.show_delete = False
        self.create_field = ""
        self.create_filter = None
        self.create_with_htmx = False

        # Update from config if provided
        if config:
            self.show_list = config.show_list
            self.show_detail = config.show_detail
            self.show_create = config.show_create
            self.show_update = config.show_update
            self.show_delete = config.show_delete
            self.create_field = config.create_field
            self.create_filter = config.create_filter
            self.create_with_htmx = config.create_with_htmx

        super().__init__(config=config, **kwargs)

    def get_current_request(self):
        """Get the current request from thread-local storage."""
        return get_current_request()

    def get_autocomplete_context(self) -> dict[str, Any]:
        """Get context for autocomplete functionality."""
        return {
            "value_field": self.value_field or self.model._meta.pk.name,
            "label_field": self.label_field or getattr(self.model, "name_field", "name"),
            "is_tabular": bool(self.plugin_dropdown_header),
            "use_htmx": self.use_htmx,
            "search_lookups": self.get_search_lookups(),
            "autocomplete_url": self.get_autocomplete_url(),
            "autocomplete_params": self.get_autocomplete_params(),
        }

    def get_permissions_context(self, autocomplete_view) -> dict[str, Any]:
        """Get permission-related context for the widget."""
        request = self.get_current_request()

        context = {
            "can_create": autocomplete_view.has_permission(request, "create"),
            "can_view": autocomplete_view.has_permission(request, "view"),
            "can_update": autocomplete_view.has_permission(request, "update"),
            "can_delete": autocomplete_view.has_permission(request, "delete"),
        }

        # Only show buttons/links for permitted actions
        context.update(
            {
                "show_create": self.show_create and context["can_create"],
                "show_list": self.show_list and context["can_view"],
                "show_detail": self.show_detail and context["can_view"],
                "show_update": self.show_update and context["can_update"],
                "show_delete": self.show_delete and context["can_delete"],
            }
        )

        return context

    def get_model_url_context(self, autocomplete_view):
        """Get URL-related context for a model object.

        We retrieve & store list and create URLs, because they are model-specific, not instance-specific.
        These are used when initializing the widget, not when selecting an option.

        Instance-specific URLs are stored in the selected_options.
        """
        request = self.get_current_request()

        try:
            context = {
                "view_list_url": (
                    reverse(autocomplete_view.list_url)
                    if hasattr(autocomplete_view, "list_url") and autocomplete_view.has_permission(request, "view")
                    else None
                ),
                "view_create_url": (
                    reverse(autocomplete_view.create_url)
                    if hasattr(autocomplete_view, "create_url") and autocomplete_view.has_permission(request, "create")
                    else None
                ),
            }
        except NoReverseMatch:
            logger.warning("Unable to reverse list_url or create_url for model %s", self.model)
            context = {"view_list_url": None, "view_create_url": None}

        return context

    def get_instance_url_context(self, obj, autocomplete_view):
        """Get URL-related context for a selected object."""
        request = self.get_current_request()
        urls = {}

        if self.show_detail and autocomplete_view.detail_url and autocomplete_view.has_permission(request, "view"):
            try:
                urls["detail_url"] = reverse(autocomplete_view.detail_url, args=[obj.pk])
            except NoReverseMatch:
                logger.warning(
                    "Unable to reverse detail_url %s with pk %s",
                    autocomplete_view.detail_url,
                    obj.pk,
                )

        if self.show_update and autocomplete_view.update_url:
            try:
                urls["update_url"] = reverse(autocomplete_view.update_url, args=[obj.pk])
            except NoReverseMatch:
                logger.warning(
                    "Unable to reverse update_url %s with pk %s",
                    autocomplete_view.update_url,
                    obj.pk,
                )

        if self.show_delete and autocomplete_view.delete_url:
            try:
                urls["delete_url"] = reverse(autocomplete_view.delete_url, args=[obj.pk])
            except NoReverseMatch:
                logger.warning(
                    "Unable to reverse delete_url %s with pk %s",
                    autocomplete_view.delete_url,
                    obj.pk,
                )

        return urls

    def get_context(self, name: str, value: Any, attrs: dict[str, str] | None = None) -> dict[str, Any]:
        """Get context for rendering the widget."""
        self.get_queryset()  # Ensure we have model info

        # Initial context without autocomplete view
        base_context = {
            "widget": {
                "name": name,
                "value": value,
                "minimum_query_length": self.minimum_query_length,
                "preload": self.preload,
                "highlight": self.highlight,
                "open_on_focus": self.open_on_focus,
                "placeholder": self.placeholder,
                "max_items": self.max_items,
                "max_options": self.max_options,
                "close_after_select": self.close_after_select,
                "hide_placeholder": self.hide_placeholder,
                "load_throttle": self.load_throttle,
                "loading_class": self.loading_class,
                "create": self.create,
                "create_field": self.create_field,
                "create_with_htmx": self.create_with_htmx,
                "attrs": attrs or {},
                "is_multiple": False,
                **self.get_autocomplete_context(),
                "plugins": self.get_plugin_context(),
                "selected_options": [],
            }
        }

        # Add filter/exclude configuration
        if self.filter_by:
            dependent_field, dependent_field_lookup = self.filter_by
            base_context["widget"].update(
                {
                    "dependent_field": dependent_field,
                    "dependent_field_lookup": dependent_field_lookup,
                }
            )

        if self.exclude_by:
            exclude_field, exclude_field_lookup = self.exclude_by
            base_context["widget"].update(
                {
                    "exclude_field": exclude_field,
                    "exclude_field_lookup": exclude_field_lookup,
                }
            )

        autocomplete_view = self.get_autocomplete_view()
        request = self.get_current_request()
        if not autocomplete_view or not request or not self.validate_request(request):
            logger.warning("Autocomplete view or request not available, returning base context")
            return base_context

        # Build full context with autocomplete view
        attrs = self.build_attrs(self.attrs, attrs)
        context = {
            "widget": {
                **base_context["widget"],
                "attrs": attrs,
                **self.get_model_url_context(autocomplete_view),
            }
        }

        # Add permissions context
        context["widget"].update(self.get_permissions_context(autocomplete_view))

        # Add selected options if value is provided
        if value and self.get_queryset() is not None:
            selected_objects = self.get_queryset().filter(
                pk__in=[value] if not isinstance(value, (list, tuple)) else value
            )

            selected = []
            for obj in selected_objects:
                opt = {
                    "value": str(obj.pk),
                    "label": self.get_label_for_object(obj, autocomplete_view),
                    **self.get_instance_url_context(obj, autocomplete_view),
                }
                selected.append(opt)

            context["widget"]["selected_options"] = selected

        return context

    def get_label_for_object(self, obj, autocomplete_view):
        """Get the label for an object using the configured label field."""
        label_field = self.label_field
        try:
            # Try to get value as field or property
            label_value = getattr(obj, label_field, None)
            if label_value is None:
                # Check for prepare method on autocomplete view
                prepare_method = getattr(autocomplete_view, f"prepare_{label_field}", None)
                if prepare_method:
                    label_value = prepare_method(obj)
        except AttributeError:
            # Fallback to string representation
            label_value = str(obj)

        return label_value or str(obj)

    def get_model(self):
        """Get model from field's choices or queryset."""
        if hasattr(self.choices, "queryset"):
            return self.choices.queryset.model
        elif hasattr(self.choices, "model"):
            return self.choices.model
        elif isinstance(self.choices, list) and self.choices:
            return None
        return None

    def validate_request(self, request) -> bool:
        """Validate that a request object is valid for permission checking."""
        if not request:
            return False

        # Check if request has required attributes and methods
        required_attributes = ["user", "method", "GET"]
        has_required = all(hasattr(request, attr) for attr in required_attributes)

        if not has_required:
            return False

        # Verify user attribute has required auth methods
        if not hasattr(request, "user") or not hasattr(request.user, "is_authenticated"):
            return False

        # Verify request methods are callable
        if not callable(getattr(request, "get_full_path", None)):
            return False

        return True

    def get_autocomplete_view(self):
        """Get instance of autocomplete view for accessing queryset and search_lookups."""
        self.model = self.get_model()

        # Get request from thread-local storage
        request = self.get_current_request()
        user = None
        if self.validate_request(request):
            user = request.user
        else:
            logger.warning(
                "Invalid or missing request object when creating proxy request. " "Permissions will be restricted."
            )

        proxy_request = ProxyRequest(model=self.model, user=user)

        autocomplete_view = resolve(self.get_autocomplete_url()).func.view_class()
        if not issubclass(autocomplete_view.__class__, AutocompleteModelView):
            raise ValueError(
                "The autocomplete view for a model-type Tom Select widget must be a subclass of AutocompleteModelView"
            )

        autocomplete_view.setup(model=self.model, request=proxy_request)

        # Apply widget-level auth settings to override view settings
        if hasattr(self, "allow_anonymous"):
            autocomplete_view.allow_anonymous = self.allow_anonymous
        if hasattr(self, "skip_authorization"):
            autocomplete_view.skip_authorization = self.skip_authorization

        return autocomplete_view

    def get_queryset(self):
        """Get queryset from autocomplete view."""
        autocomplete_view = self.get_autocomplete_view()
        return autocomplete_view.get_queryset()

    def get_search_lookups(self):
        """Get search lookups from autocomplete view."""
        autocomplete_view = self.get_autocomplete_view()
        return autocomplete_view.search_lookups


class TomSelectModelMultipleWidget(TomSelectModelWidget, forms.SelectMultiple):
    """A TomSelect widget that allows multiple model object selection."""

    def get_context(self, name: str, value: Any, attrs: dict[str, str] | None = None) -> dict[str, Any]:
        """Get context for rendering the widget."""
        context = super().get_context(name, value, attrs)
        context["widget"]["is_multiple"] = True
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["is-multiple"] = True
        return attrs


class TomSelectIterablesWidget(TomSelectWidgetMixin, forms.Select):
    """A Tom Select widget with iterables, TextChoices, or IntegerChoices choices."""

    def set_request(self, request):
        """Iterables do not require a request object."""
        logger.warning("Request object is not required for iterables-type Tom Select widgets.")

    def get_autocomplete_context(self) -> dict[str, Any]:
        """Get context for autocomplete functionality."""
        return {
            "value_field": self.value_field,
            "label_field": self.label_field,
            "is_tabular": bool(self.plugin_dropdown_header),
            "use_htmx": self.use_htmx,
            "autocomplete_url": self.get_autocomplete_url(),
        }

    def get_context(self, name: str, value: Any, attrs: dict[str, str] | None = None) -> dict[str, Any]:
        """Get context for rendering the widget."""
        attrs = self.build_attrs(self.attrs, attrs)
        context = {
            "widget": {
                "name": name,
                "value": value,
                "minimum_query_length": self.minimum_query_length,
                "preload": self.preload,
                "highlight": self.highlight,
                "open_on_focus": self.open_on_focus,
                "placeholder": self.placeholder,
                "max_items": self.max_items,
                "max_options": self.max_options,
                "close_after_select": self.close_after_select,
                "hide_placeholder": self.hide_placeholder,
                "load_throttle": self.load_throttle,
                "loading_class": self.loading_class,
                "create": self.create,
                "attrs": attrs,
                "is_multiple": False,
                **self.get_autocomplete_context(),
                "plugins": self.get_plugin_context(),
            }
        }

        if value is not None:
            autocomplete_view = self.get_autocomplete_view()

            if autocomplete_view:
                # Handle different types of iterables
                if isinstance(autocomplete_view.iterable, type) and hasattr(autocomplete_view.iterable, "choices"):
                    # TextChoices/IntegerChoices
                    values = [value] if not isinstance(value, (list, tuple)) else value
                    selected = []
                    for val in values:
                        for (
                            choice_value,
                            choice_label,
                        ) in autocomplete_view.iterable.choices:
                            if str(val) == str(choice_value):
                                selected.append({"value": str(val), "label": choice_label})
                                break
                        else:
                            selected.append({"value": str(val), "label": str(val)})

                elif (
                    isinstance(autocomplete_view.iterable, (tuple, list))
                    and autocomplete_view.iterable
                    and isinstance(autocomplete_view.iterable[0], (tuple))
                ):
                    # Tuple iterables
                    values = [value] if not isinstance(value, (list, tuple)) else value
                    selected = []
                    for val in values:
                        for item in autocomplete_view.iterable:
                            if str(item) == str(val):
                                selected.append({"value": str(val), "label": f"{item[0]}-{item[1]}"})
                                break
                        else:
                            selected.append({"value": str(val), "label": str(val)})

                else:
                    # Simple iterables
                    values = [value] if not isinstance(value, (list, tuple)) else value
                    selected = [{"value": str(val), "label": str(val)} for val in values]

                if selected:
                    context["widget"]["selected_options"] = selected

        return context

    def get_autocomplete_view(self):
        """Get instance of autocomplete view for accessing iterable."""
        proxy_request = ProxyRequest()

        try:
            autocomplete_view = resolve(self.get_autocomplete_url()).func.view_class()
            autocomplete_view.setup(request=proxy_request)

            # Check if view has get_iterable method
            if hasattr(autocomplete_view, "get_iterable"):
                return autocomplete_view

            # If not iterables view but has get_iterable, it's compatible
            if not issubclass(autocomplete_view.__class__, AutocompleteIterablesView):
                if not hasattr(autocomplete_view, "get_iterable"):
                    raise ValueError(
                        "The autocomplete view must either be a subclass of "
                        "AutocompleteIterablesView or implement get_iterable()"
                    )
            return autocomplete_view

        except Exception as e:
            logger.error("Error setting up autocomplete view: %s", e)
            raise

    def get_iterable(self):
        """Get iterable or choices from autocomplete view."""
        autocomplete_view = self.get_autocomplete_view()
        return autocomplete_view.get_iterable()


class TomSelectIterablesMultipleWidget(TomSelectIterablesWidget, forms.SelectMultiple):
    """A TomSelect widget for multiple selection of iterables, TextChoices, or IntegerChoices."""

    def get_context(self, name: str, value: Any, attrs: dict[str, str] | None = None) -> dict[str, Any]:
        """Get context for rendering the widget."""
        context = super().get_context(name, value, attrs)
        context["widget"]["is_multiple"] = True
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["is-multiple"] = True
        return attrs
