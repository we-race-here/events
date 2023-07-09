from django.db import models


# Will remove the following from WRH
# class USACEvent(models.Model):
# class USACClubTeam(models.Model):
# class USACClub(models.Model):
# class USACRider(models.Model):


# This model was named
# class USACRiderLicense(models.Model):
class UsacDownload(models.Model):
    """This is imported from the racer download"""

    license_number = models.IntegerField(db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    race_age = models.IntegerField(blank=True, null=True)
    race_gender = models.CharField(max_length=1, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    license_expiration = models.DateField(null=True, blank=True)
    license_type = models.CharField(max_length=32, null=True, blank=True)
    license_status = models.CharField(max_length=32, null=True, blank=True)
    local_association = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    data_hash = models.CharField(max_length=64, unique=True, editable=False)
    create_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.license_type}-{self.license_number}[{self.license_status}]"


# Create your models here.
