# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class CyclingOrgCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=256)
    create_datetime = models.DateTimeField()
    create_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey("CyclingOrgOrganization", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_category"
        unique_together = (("title", "organization"),)


class CyclingOrgEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    organizer_email = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)
    create_datetime = models.DateTimeField()
    update_datetime = models.DateTimeField()
    organization = models.ForeignKey("CyclingOrgOrganization", models.DO_NOTHING, blank=True, null=True)
    create_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    registration_website = models.CharField(max_length=500, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    website = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=16, blank=True, null=True)
    prefs = models.JSONField(blank=True, null=True)
    location_lat = models.FloatField(blank=True, null=True)
    location_lon = models.FloatField(blank=True, null=True)
    is_usac_permitted = models.BooleanField()
    permit_no = models.CharField(max_length=25, blank=True, null=True)
    featured_event = models.BooleanField()
    publish_type = models.CharField(max_length=32, blank=True, null=True)
    shared_org_perms = models.JSONField(blank=True, null=True)
    approved = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_event"


class CyclingOrgEventattachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256, blank=True, null=True)
    create_datetime = models.DateTimeField()
    event = models.ForeignKey(CyclingOrgEvent, models.DO_NOTHING)
    upload_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_eventattachment"


class CyclingOrgFieldstracking(models.Model):
    id = models.BigAutoField(primary_key=True)
    object_id = models.CharField(max_length=64)
    fields_data = models.JSONField(blank=True, null=True)
    changed_data = models.JSONField(blank=True, null=True)
    object_repr = models.TextField()
    refs_repr = models.JSONField(blank=True, null=True)
    datetime = models.DateTimeField()
    user_str_id = models.CharField(max_length=64, blank=True, null=True)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    user = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_fieldstracking"


class CyclingOrgFinancialtransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.CharField(max_length=16)
    payment_id = models.CharField(max_length=64)
    create_datetime = models.DateTimeField()
    user = models.ForeignKey("WrhAccountUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_financialtransaction"


class CyclingOrgHistoricalorganizationmember(models.Model):
    id = models.BigIntegerField()
    is_admin = models.BooleanField()
    is_master_admin = models.BooleanField()
    membership_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    membership_plan = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    org_member_uid = models.CharField(max_length=256, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    member_fields = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    datetime = models.DateTimeField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    member_id = models.BigIntegerField(blank=True, null=True)
    organization_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_historicalorganizationmember"


class CyclingOrgMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    gender = models.CharField(max_length=1)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    address1 = models.CharField(max_length=256, blank=True, null=True)
    address2 = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    email_verified = models.BooleanField(blank=True, null=True)
    phone_verified = models.BooleanField(blank=True, null=True)
    social_media = models.JSONField(blank=True, null=True)
    is_verified = models.BooleanField(blank=True, null=True)
    height = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)
    draft = models.BooleanField()
    usac_license_number = models.IntegerField(unique=True, blank=True, null=True)
    usac_license_number_verified = models.BooleanField()

    class Meta:
        managed = False
        db_table = "cycling_org_member"
        unique_together = (
            ("email", "email_verified"),
            ("phone", "phone_verified"),
        )


class CyclingOrgOrganization(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=256)
    type = models.CharField(max_length=32)
    social_media = models.JSONField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    signup_config = models.JSONField(blank=True, null=True)
    member_fields_schema = models.JSONField(blank=True, null=True)
    verified = models.BooleanField()
    website = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    email_verified = models.BooleanField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    phone_verified = models.BooleanField(blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    membership_plans = models.JSONField(blank=True, null=True)
    prefs = models.JSONField(blank=True, null=True)
    rss_url = models.TextField(blank=True, null=True)
    waiver_text = models.TextField(blank=True, null=True)
    membership_open = models.BooleanField(blank=True, null=True)
    approved = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_organization"


class CyclingOrgOrganizationmember(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_admin = models.BooleanField()
    membership_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    datetime = models.DateTimeField()
    member = models.ForeignKey(CyclingOrgMember, models.DO_NOTHING)
    organization = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING)
    is_active = models.BooleanField(blank=True, null=True)
    is_master_admin = models.BooleanField()
    member_fields = models.JSONField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    org_member_uid = models.CharField(max_length=256, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    membership_plan = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_organizationmember"
        unique_together = (
            ("organization", "member", "is_active"),
            ("organization", "org_member_uid", "is_active"),
        )


class CyclingOrgOrganizationmemberorg(models.Model):
    id = models.BigAutoField(primary_key=True)
    membership_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    datetime = models.DateTimeField()
    organization = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING)
    is_active = models.BooleanField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    member_fields = models.JSONField(blank=True, null=True)
    member_org = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING, related_name="cycling_member")
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_organizationmemberorg"
        unique_together = (("organization", "member_org", "is_active"),)


class CyclingOrgRace(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    start_datetime = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(CyclingOrgEvent, models.DO_NOTHING)
    create_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    create_datetime = models.DateTimeField()
    organization = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING, blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_race"
        unique_together = (("name", "event", "organization"),)


class CyclingOrgRaceresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    place = models.IntegerField(blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)
    create_datetime = models.DateTimeField()
    create_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING, blank=True, null=True)
    race = models.ForeignKey(CyclingOrgRace, models.DO_NOTHING)
    rider = models.ForeignKey(CyclingOrgMember, models.DO_NOTHING, blank=True, null=True)
    finish_status = models.CharField(max_length=16)
    category = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cycling_org_raceresult"
        unique_together = (("rider", "race", "organization"),)


class CyclingOrgRaceseries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    points_map = models.JSONField(blank=True, null=True)
    create_datetime = models.DateTimeField()
    create_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_raceseries"
        unique_together = (("name", "organization"),)


class CyclingOrgRaceseriesCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    raceseries = models.ForeignKey(CyclingOrgRaceseries, models.DO_NOTHING)
    category = models.ForeignKey(CyclingOrgCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_raceseries_categories"
        unique_together = (("raceseries", "category"),)


class CyclingOrgRaceseriesEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    raceseries = models.ForeignKey(CyclingOrgRaceseries, models.DO_NOTHING)
    event = models.ForeignKey(CyclingOrgEvent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_raceseries_events"
        unique_together = (("raceseries", "event"),)


class CyclingOrgRaceseriesRaces(models.Model):
    id = models.BigAutoField(primary_key=True)
    raceseries = models.ForeignKey(CyclingOrgRaceseries, models.DO_NOTHING)
    race = models.ForeignKey(CyclingOrgRace, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_raceseries_races"
        unique_together = (("raceseries", "race"),)


class CyclingOrgRaceseriesresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    place = models.IntegerField(blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)
    create_datetime = models.DateTimeField()
    category = models.ForeignKey(CyclingOrgCategory, models.DO_NOTHING)
    create_by = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(CyclingOrgOrganization, models.DO_NOTHING, blank=True, null=True)
    race_series = models.ForeignKey(CyclingOrgRaceseries, models.DO_NOTHING)
    race_result = models.ForeignKey(CyclingOrgRaceresult, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "cycling_org_raceseriesresult"
        unique_together = (("race_series", "race_result", "category", "organization"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey("WrhAccountUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class DynamicPreferencesGlobalpreferencemodel(models.Model):
    section = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150)
    raw_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dynamic_preferences_globalpreferencemodel"
        unique_together = (("section", "name"),)


class UsacyclingUsacclub(models.Model):
    club_id = models.BigIntegerField(primary_key=True)
    club_name = models.CharField(max_length=200, blank=True, null=True)
    club_org_id = models.CharField(max_length=100, blank=True, null=True)
    club_ncaa_id = models.CharField(max_length=100, blank=True, null=True)
    club_updated_by_user = models.CharField(max_length=100, blank=True, null=True)
    club_aff_type_id = models.IntegerField()
    club_type_id = models.IntegerField()
    club_legacy_id = models.IntegerField()
    club_disciplines = models.CharField(max_length=100, blank=True, null=True)
    club_aff_type = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField()
    expiration_date = models.DateField()

    class Meta:
        managed = False
        db_table = "usacycling_usacclub"


class UsacyclingUsacclubClubTeams(models.Model):
    id = models.BigAutoField(primary_key=True)
    usacclub = models.ForeignKey(UsacyclingUsacclub, models.DO_NOTHING)
    usacclubteam = models.ForeignKey("UsacyclingUsacclubteam", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "usacycling_usacclub_club_teams"
        unique_together = (("usacclub", "usacclubteam"),)


class UsacyclingUsacclubteam(models.Model):
    team_id = models.BigIntegerField(primary_key=True)
    team_name = models.CharField(max_length=200)
    team_club_id = models.IntegerField()
    women_only = models.IntegerField()
    masters_only = models.IntegerField()
    juniors_only = models.IntegerField()
    d_elite = models.IntegerField()
    team_legacy_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "usacycling_usacclubteam"


class UsacyclingUsacevent(models.Model):
    event_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    dates = models.JSONField(blank=True, null=True)
    is_featured = models.BooleanField()
    is_weekend = models.BooleanField()
    is_multiday = models.BooleanField()
    is_usac_sanctioned = models.BooleanField()
    event_organizer_email = models.CharField(max_length=300, blank=True, null=True)
    event_status = models.CharField(max_length=300)
    permit = models.CharField(max_length=300, blank=True, null=True)
    labels = models.TextField(blank=True, null=True)  # This field type is a guess.
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    links = models.JSONField(blank=True, null=True)
    data_source = models.CharField(max_length=300)
    created_at = models.DateField()
    updated_at = models.DateField()

    class Meta:
        managed = False
        db_table = "usacycling_usacevent"


class UsacyclingUsacrider(models.Model):
    license = models.IntegerField(primary_key=True)
    suspension = models.IntegerField(blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=2, blank=True, null=True)
    racingage = models.IntegerField(blank=True, null=True)
    expdateroad = models.IntegerField(blank=True, null=True)
    expdatemtn = models.IntegerField(blank=True, null=True)
    rdclub = models.CharField(max_length=255, blank=True, null=True)
    rdteam = models.CharField(max_length=255, blank=True, null=True)
    trackclub = models.CharField(max_length=255, blank=True, null=True)
    trackteam = models.CharField(max_length=255, blank=True, null=True)
    cxclub = models.CharField(max_length=255, blank=True, null=True)
    cxteam = models.CharField(max_length=255, blank=True, null=True)
    mtnclub = models.CharField(max_length=255, blank=True, null=True)
    mtnteam = models.CharField(max_length=255, blank=True, null=True)
    intlteam = models.CharField(max_length=255, blank=True, null=True)
    nccaclub = models.CharField(max_length=255, blank=True, null=True)
    roadcat = models.CharField(max_length=20, blank=True, null=True)
    trackcat = models.CharField(max_length=20, blank=True, null=True)
    crosscat = models.CharField(max_length=20, blank=True, null=True)
    downhillcat = models.CharField(max_length=20, blank=True, null=True)
    mxcat = models.CharField(max_length=20, blank=True, null=True)
    xccat = models.CharField(max_length=20, blank=True, null=True)
    otcat = models.CharField(max_length=20, blank=True, null=True)
    cxcat = models.CharField(max_length=20, blank=True, null=True)
    citizen = models.IntegerField(blank=True, null=True)
    emergencycontact = models.CharField(max_length=255, blank=True, null=True)
    econtactphone = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    foreignteam = models.CharField(max_length=200, blank=True, null=True)
    ucicode = models.CharField(max_length=20, blank=True, null=True)
    team = models.CharField(max_length=200, blank=True, null=True)
    collclub = models.CharField(max_length=200, blank=True, null=True)
    rdclubid = models.IntegerField(blank=True, null=True)
    rdteamid = models.IntegerField(blank=True, null=True)
    trackclubid = models.IntegerField(blank=True, null=True)
    trackteamid = models.IntegerField(blank=True, null=True)
    mtnclubid = models.IntegerField(blank=True, null=True)
    mtnteamid = models.IntegerField(blank=True, null=True)
    cxclubid = models.IntegerField(blank=True, null=True)
    cxteamid = models.IntegerField(blank=True, null=True)
    collclubid = models.IntegerField(blank=True, null=True)
    cxrank = models.FloatField(blank=True, null=True)
    dhcat = models.CharField(max_length=20, blank=True, null=True)
    hsclub = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "usacycling_usacrider"


class UsacyclingUsacriderlicense(models.Model):
    id = models.BigAutoField(primary_key=True)
    license_number = models.IntegerField()
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    race_age = models.IntegerField(blank=True, null=True)
    race_gender = models.CharField(max_length=1, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    license_expiration = models.DateField(blank=True, null=True)
    license_type = models.CharField(max_length=32, blank=True, null=True)
    license_status = models.CharField(max_length=32, blank=True, null=True)
    local_association = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    data_hash = models.CharField(unique=True, max_length=64)
    create_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "usacycling_usacriderlicense"


class WrhAccountHistoricaluser(models.Model):
    id = models.BigIntegerField()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(max_length=254)
    gender = models.CharField(max_length=1)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)
    prefs = models.JSONField(blank=True, null=True)
    draft = models.BooleanField()
    opt_in_email = models.BooleanField(blank=True, null=True)
    terms_of_service = models.BooleanField(blank=True, null=True)
    user_agreement_waiver = models.BooleanField(blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey("WrhAccountUser", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "wrh_account_historicaluser"


class WrhAccountUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    gender = models.CharField(max_length=1)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    more_data = models.JSONField(blank=True, null=True)
    prefs = models.JSONField(blank=True, null=True)
    draft = models.BooleanField()
    opt_in_email = models.BooleanField(blank=True, null=True)
    terms_of_service = models.BooleanField(blank=True, null=True)
    user_agreement_waiver = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "wrh_account_user"


class WrhAccountUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(WrhAccountUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "wrh_account_user_groups"
        unique_together = (("user", "group"),)


class WrhAccountUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(WrhAccountUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "wrh_account_user_user_permissions"
        unique_together = (("user", "permission"),)
