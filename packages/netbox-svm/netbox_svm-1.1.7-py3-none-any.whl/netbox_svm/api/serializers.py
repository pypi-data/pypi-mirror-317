from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_svm.models import SoftwareProduct, SoftwareProductVersion, SoftwareProductInstallation, SoftwareLicense


class SoftwareLicenseSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_svm-api:softwarelicense-detail")

    class Meta:
        model = SoftwareLicense
        fields = (
            "id",
            "display",
            "url",
            "name",
            "description",
            "type",
            "stored_location",
            "stored_location_url",
            "start_date",
            "expiration_date",
            "support",
            "license_amount",
            "software_product",
            "version",
            "installation",
            "tags",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "url", "name", "description")

    def get_display(self, obj):
        return f"{obj}"


class SoftwareProductSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_svm-api:softwareproduct-detail")

    class Meta:
        model = SoftwareProduct
        fields = (
            "id",
            "display",
            "url",
            "name",
            "manufacturer",
            "description",
            "tags",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "url", "name", "description")

    def get_display(self, obj):
        return f"{obj.manufacturer} - {obj}"


class SoftwareProductInstallationSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_svm-api:softwareproductinstallation-detail"
    )

    class Meta:
        model = SoftwareProductInstallation
        fields = (
            "id",
            "display",
            "url",
            "ipaddress",
            "owner",
            "software_product",
            "version",
            "tags",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "url", "name")

    def get_display(self, obj):
        return f"{obj}"


class SoftwareProductVersionSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_svm-api:softwareproductversion-detail")

    class Meta:
        model = SoftwareProductVersion
        fields = (
            "id",
            "display",
            "url",
            "name",
            "release_date",
            "documentation_url",
            "end_of_support",
            "filename",
            "file_checksum",
            "file_link",
            "release_type",
            "software_product",
            "tags",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "url", "name")

    def get_display(self, obj):
        return f"{obj}"
