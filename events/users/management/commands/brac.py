# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcaAlias(models.Model):
    alias = models.CharField(max_length=500)
    target_value = models.CharField(max_length=5000)
    type = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.BigIntegerField()
    added_by = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'aca_alias'


class AcaAuthclient(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    clientuid = models.CharField(db_column='clientUid', max_length=50)  # Field name made lowercase.
    connecturi = models.CharField(db_column='connectUri', max_length=500)  # Field name made lowercase.
    redirecturi = models.CharField(db_column='redirectUri', max_length=500)  # Field name made lowercase.
    secret = models.CharField(max_length=200, blank=True, null=True)
    approved = models.IntegerField()
    apptable = models.CharField(db_column='appTable', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remoteid = models.IntegerField(db_column='remoteId', blank=True, null=True)  # Field name made lowercase.
    autoscopes = models.CharField(db_column='autoScopes', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    createdon = models.IntegerField(db_column='createdOn')  # Field name made lowercase.
    lastmodifiedon = models.IntegerField(db_column='lastModifiedOn')  # Field name made lowercase.
    firstapprovedon = models.IntegerField(db_column='firstApprovedOn', blank=True, null=True)  # Field name made lowercase.
    lastapprovedon = models.IntegerField(db_column='lastApprovedOn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_authclient'


class AcaAuthcode(models.Model):
    id = models.CharField(primary_key=True, max_length=125)
    clientuid = models.CharField(db_column='clientUid', max_length=50)  # Field name made lowercase.
    redirecturi = models.CharField(db_column='redirectUri', max_length=500)  # Field name made lowercase.
    expires = models.IntegerField()
    scope = models.CharField(max_length=1000, blank=True, null=True)
    refreshcode = models.CharField(db_column='refreshCode', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_authcode'


class AcaAuthscope(models.Model):
    id = models.BigAutoField(primary_key=True)
    clientuid = models.CharField(db_column='clientUid', max_length=50)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    scope = models.CharField(max_length=1000, blank=True, null=True)
    createdon = models.IntegerField(db_column='createdOn', blank=True, null=True)  # Field name made lowercase.
    updatedon = models.IntegerField(db_column='updatedOn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_authscope'


class AcaAuthtoken(models.Model):
    id = models.CharField(primary_key=True, max_length=125)
    clientuid = models.CharField(db_column='clientUid', max_length=50)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    codeid = models.CharField(db_column='codeId', max_length=125, blank=True, null=True)  # Field name made lowercase.
    expires = models.IntegerField()
    scope = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_authtoken'


class AcaBatch(models.Model):
    id = models.BigAutoField(primary_key=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    notification = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_batch'


class AcaChip(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    txnitemid = models.CharField(db_column='txnItemId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dateassigned = models.IntegerField(db_column='dateAssigned')  # Field name made lowercase.
    userfullname = models.CharField(db_column='userFullName', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_chip'


class AcaClub(models.Model):
    id = models.BigAutoField(primary_key=True)
    acaclubnumber = models.CharField(db_column='acaClubNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    usacclubnumber = models.CharField(db_column='usacClubNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    expires = models.IntegerField(blank=True, null=True)
    daterenewed = models.DateField(db_column='dateRenewed', blank=True, null=True)  # Field name made lowercase.
    datejoined = models.DateField(db_column='dateJoined', blank=True, null=True)  # Field name made lowercase.
    amountpaid = models.CharField(db_column='amountPaid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    startdate = models.IntegerField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    sm = models.IntegerField(blank=True, null=True)
    sw = models.IntegerField(blank=True, null=True)
    j = models.IntegerField(blank=True, null=True)
    mm = models.IntegerField(blank=True, null=True)
    mw = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_club'


class AcaClubstate(models.Model):
    id = models.BigAutoField(primary_key=True)
    sponsorname = models.CharField(db_column='sponsorName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    primaryfocus = models.TextField(db_column='primaryFocus', blank=True, null=True)  # Field name made lowercase.
    promotions = models.TextField(blank=True, null=True)
    startdate = models.IntegerField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.IntegerField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    isinbadstanding = models.IntegerField(db_column='isInBadStanding')  # Field name made lowercase.
    reasonforbs = models.CharField(db_column='reasonForBS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    clubid = models.ForeignKey(AcaClub, models.DO_NOTHING, db_column='clubId', blank=True, null=True)  # Field name made lowercase.
    contactperson = models.ForeignKey('AcaUser', models.DO_NOTHING, db_column='contactPerson', blank=True, null=True, related_name='user1')  # Field name made lowercase.
    president = models.ForeignKey('AcaUser', models.DO_NOTHING, db_column='president', blank=True, null=True, related_name='user2')

    class Meta:
        managed = False
        db_table = 'aca_clubstate'


class AcaCredential(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    xfactor = models.IntegerField(db_column='xFactor', blank=True, null=True)  # Field name made lowercase.
    dateadded = models.IntegerField(db_column='dateAdded', blank=True, null=True)  # Field name made lowercase.
    dateexpired = models.IntegerField(db_column='dateExpired', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_credential'


class AcaDepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True, null=True)
    dateadded = models.IntegerField(db_column='dateAdded')  # Field name made lowercase.
    addedby = models.CharField(db_column='addedBy', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_department'


class AcaEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    eventdate = models.IntegerField(db_column='eventDate', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(max_length=255, blank=True, null=True)
    pdf = models.CharField(max_length=255, blank=True, null=True)
    eventtype = models.CharField(db_column='eventType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    calendar = models.IntegerField(blank=True, null=True)
    racesize = models.IntegerField(db_column='raceSize', blank=True, null=True)  # Field name made lowercase.
    eventcity = models.CharField(db_column='eventCity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eventstate = models.CharField(db_column='eventState', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stagecomponent = models.IntegerField(db_column='stageComponent', blank=True, null=True)  # Field name made lowercase.
    pointscompetitionids = models.CharField(db_column='pointsCompetitionIds', max_length=127, blank=True, null=True)  # Field name made lowercase.
    permitnumbers = models.CharField(db_column='permitNumbers', max_length=127, blank=True, null=True)  # Field name made lowercase.
    doublepoints = models.IntegerField(db_column='doublePoints', blank=True, null=True)  # Field name made lowercase.
    pointscompetitionjson = models.CharField(db_column='pointsCompetitionJSON', max_length=127, blank=True, null=True)  # Field name made lowercase.
    calendarfeepaid = models.DecimalField(db_column='calendarFeePaid', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    competitionfeepaid = models.DecimalField(db_column='competitionFeePaid', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    isacaevent = models.IntegerField(db_column='isACAEvent')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='parentId', blank=True, null=True)  # Field name made lowercase.
    pointquantifier = models.FloatField(db_column='pointQuantifier', blank=True, null=True)  # Field name made lowercase.
    promoter = models.ForeignKey('AcaUser', models.DO_NOTHING, db_column='promoter', blank=True, null=True)
    eventdatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_event'


class AcaEventclub(models.Model):
    id = models.BigAutoField(primary_key=True)
    clubid = models.ForeignKey(AcaClub, models.DO_NOTHING, db_column='clubId', blank=True, null=True)  # Field name made lowercase.
    eventid = models.ForeignKey(AcaEvent, models.DO_NOTHING, db_column='eventId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_eventclub'


class AcaEventphotographer(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    eventid = models.ForeignKey(AcaEvent, models.DO_NOTHING, db_column='eventId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_eventphotographer'


class AcaEventpointquantifier(models.Model):
    id = models.BigAutoField(primary_key=True)
    eventid = models.IntegerField(db_column='eventId')  # Field name made lowercase.
    racegroupid = models.IntegerField(db_column='racegroupId')  # Field name made lowercase.
    pointquantifier = models.DecimalField(db_column='pointQuantifier', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_eventpointquantifier'


class AcaEventpoints(models.Model):
    id = models.BigAutoField(primary_key=True)
    pointstype = models.CharField(db_column='pointsType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rsize = models.IntegerField(db_column='rSize', blank=True, null=True)  # Field name made lowercase.
    eventracegroupid = models.ForeignKey('AcaEventracegroup', models.DO_NOTHING, db_column='eventRaceGroupId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_eventpoints'


class AcaEventpointscompetition(models.Model):
    id = models.BigAutoField(primary_key=True)
    pointscompetitionid = models.IntegerField(db_column='pointsCompetitionId', blank=True, null=True)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='eventId', blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(max_length=45, blank=True, null=True)
    pointscompetitiontypeid = models.IntegerField(db_column='pointsCompetitionTypeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_eventpointscompetition'
        unique_together = (('eventid', 'pointscompetitionid'),)


class AcaEventracegroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    eventid = models.ForeignKey(AcaEvent, models.DO_NOTHING, db_column='eventId', blank=True, null=True)  # Field name made lowercase.
    racegroupid = models.ForeignKey('AcaRacegroup', models.DO_NOTHING, db_column='raceGroupId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_eventracegroup'


class AcaEventtype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    ptype = models.CharField(db_column='pType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    utype = models.CharField(db_column='uType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=100, blank=True, null=True)
    discipline = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_eventtype'


class AcaNews(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    categoryid = models.IntegerField(db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    file = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_news'


class AcaNote(models.Model):
    id = models.BigAutoField(primary_key=True)
    objecttype = models.CharField(db_column='objectType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objectid = models.IntegerField(db_column='objectId', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    authorid = models.ForeignKey('AcaUser', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_note'


class AcaPointscompetition(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    seasonbegin = models.DateField(db_column='seasonBegin', blank=True, null=True)  # Field name made lowercase.
    seasonend = models.DateField(db_column='seasonEnd', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    pctype = models.CharField(db_column='pcType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    iconpath = models.CharField(db_column='iconPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    competitiontypesjson = models.CharField(db_column='competitionTypesJSON', max_length=1023, blank=True, null=True)  # Field name made lowercase.
    depthjson = models.CharField(db_column='depthJSON', max_length=500)  # Field name made lowercase.
    lastrun = models.IntegerField(db_column='lastRun', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_pointscompetition'


class AcaPointscompetitionraceresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    racegroupname = models.CharField(db_column='raceGroupName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.IntegerField(blank=True, null=True)
    place = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    racename = models.CharField(db_column='raceName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    racetype = models.CharField(db_column='raceType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clubno = models.IntegerField(db_column='clubNo', blank=True, null=True)  # Field name made lowercase.
    pointscompetitionid = models.IntegerField(db_column='pointsCompetitionId', blank=True, null=True)  # Field name made lowercase.
    racegroupid = models.IntegerField(db_column='raceGroupId', blank=True, null=True)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='eventId', blank=True, null=True)  # Field name made lowercase.
    starters = models.IntegerField(blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)
    special = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_pointscompetitionraceresult'


class AcaPointscompetitionresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    place = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    acamembership = models.IntegerField(db_column='acaMembership', blank=True, null=True)  # Field name made lowercase.
    clubno = models.IntegerField(db_column='clubNo', blank=True, null=True)  # Field name made lowercase.
    team = models.CharField(max_length=255, blank=True, null=True)
    currentcat = models.CharField(db_column='currentCat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    racingage = models.IntegerField(db_column='racingAge', blank=True, null=True)  # Field name made lowercase.
    pointscompetitionid = models.IntegerField(db_column='pointsCompetitionId', blank=True, null=True)  # Field name made lowercase.
    datecreated = models.IntegerField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    racegroupid = models.IntegerField(db_column='raceGroupId', blank=True, null=True)  # Field name made lowercase.
    category = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    special = models.CharField(max_length=45, blank=True, null=True)
    usac = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_pointscompetitionresult'


class AcaPointscompetitionrules(models.Model):
    id = models.BigAutoField(primary_key=True)
    place = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    m_tttpoints = models.IntegerField(blank=True, null=True)
    f_tttpoints = models.IntegerField(blank=True, null=True)
    j_tttpoints = models.IntegerField(blank=True, null=True)
    utype = models.CharField(db_column='uType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    uracesize = models.IntegerField(db_column='uRaceSize', blank=True, null=True)  # Field name made lowercase.
    uracetype = models.CharField(db_column='uRaceType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pointscompetitiontypeid = models.IntegerField(db_column='pointscompetitionTypeId', blank=True, null=True)  # Field name made lowercase.
    applyforgc = models.IntegerField(db_column='applyForGC')  # Field name made lowercase.
    applyforparent = models.IntegerField(db_column='applyForParent')  # Field name made lowercase.
    pointscompetitionid = models.ForeignKey(AcaPointscompetition, models.DO_NOTHING, db_column='pointsCompetitionId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_pointscompetitionrules'


class AcaPointscompetitiontype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    pointscompetitionid = models.IntegerField(db_column='pointscompetitionId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_pointscompetitiontype'


class AcaPrintqueue(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField()
    isdeleted = models.IntegerField(db_column='isDeleted', blank=True, null=True)  # Field name made lowercase.
    lastdateprinted = models.IntegerField(db_column='lastDatePrinted', blank=True, null=True)  # Field name made lowercase.
    approvederrors = models.CharField(db_column='approvedErrors', max_length=127, blank=True, null=True)  # Field name made lowercase.
    queuename = models.CharField(db_column='queueName', max_length=20)  # Field name made lowercase.
    transactionitemid = models.IntegerField(db_column='transactionItemId', blank=True, null=True)  # Field name made lowercase.
    dateadded = models.IntegerField(db_column='dateAdded', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.IntegerField(db_column='dateDeleted', blank=True, null=True)  # Field name made lowercase.
    transactionid = models.ForeignKey('AcaTransaction', models.DO_NOTHING, db_column='transactionId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_printqueue'


class AcaProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)
    dateadded = models.IntegerField(db_column='dateAdded')  # Field name made lowercase.
    addedby = models.CharField(db_column='addedBy', max_length=45)  # Field name made lowercase.
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    units = models.IntegerField(blank=True, null=True)
    visible = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    actions = models.CharField(max_length=500, blank=True, null=True)
    departmentid = models.ForeignKey(AcaDepartment, models.DO_NOTHING, db_column='departmentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_product'


class AcaProductoption(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)
    dateadded = models.IntegerField(db_column='dateAdded')  # Field name made lowercase.
    addedby = models.CharField(db_column='addedBy', max_length=45)  # Field name made lowercase.
    visible = models.IntegerField()
    deleted = models.IntegerField()
    productid = models.ForeignKey(AcaProduct, models.DO_NOTHING, db_column='productId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_productoption'


class AcaProductoptionvalue(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=500)
    dateadded = models.IntegerField(db_column='dateAdded')  # Field name made lowercase.
    addedby = models.CharField(db_column='addedBy', max_length=45)  # Field name made lowercase.
    abbreviation = models.CharField(max_length=500, blank=True, null=True)
    additionalprice = models.DecimalField(db_column='additionalPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    units = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    validation = models.CharField(max_length=500, blank=True, null=True)
    productoptionid = models.ForeignKey(AcaProductoption, models.DO_NOTHING, db_column='productOptionId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_productoptionvalue'


class AcaRacegroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    abbreviation = models.CharField(max_length=255, blank=True, null=True)
    loweragelimit = models.IntegerField(db_column='lowerAgeLimit', blank=True, null=True)  # Field name made lowercase.
    upperagelimit = models.IntegerField(db_column='upperAgeLimit', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    sortorder = models.IntegerField(db_column='sortOrder', blank=True, null=True)  # Field name made lowercase.
    sanctioned = models.IntegerField(blank=True, null=True)
    tttpointstype = models.CharField(db_column='tttPointsType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    category = models.IntegerField(blank=True, null=True)
    minbib = models.IntegerField(db_column='minBib', blank=True, null=True)  # Field name made lowercase.
    maxbib = models.IntegerField(db_column='maxBib', blank=True, null=True)  # Field name made lowercase.
    mincategory = models.IntegerField(db_column='minCategory', blank=True, null=True)  # Field name made lowercase.
    maxcategory = models.IntegerField(db_column='maxCategory', blank=True, null=True)  # Field name made lowercase.
    feeexempt = models.IntegerField(db_column='feeExempt')  # Field name made lowercase.
    alwaysincludepc = models.IntegerField(db_column='alwaysIncludePC')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_racegroup'


class AcaRacegrouptemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    createdat = models.IntegerField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.IntegerField(db_column='updatedAt')  # Field name made lowercase.
    addedby = models.CharField(db_column='addedBy', max_length=45)  # Field name made lowercase.
    disc = models.CharField(max_length=45)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    visible = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aca_racegrouptemplate'


class AcaRacegrouptemplatemap(models.Model):
    id = models.BigAutoField(primary_key=True)
    templateid = models.IntegerField(db_column='templateId', blank=True, null=True)  # Field name made lowercase.
    racegroupid = models.IntegerField(db_column='raceGroupId', blank=True, null=True)  # Field name made lowercase.
    competitionids = models.CharField(db_column='competitionIds', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_racegrouptemplatemap'
        unique_together = (('templateid', 'racegroupid'),)


class AcaResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    rsplace = models.IntegerField(db_column='rsPlace', blank=True, null=True)  # Field name made lowercase.
    place = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    privatenote = models.TextField(db_column='privateNote', blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(max_length=255, blank=True, null=True)
    resultsetid = models.IntegerField(db_column='resultSetId', blank=True, null=True)  # Field name made lowercase.
    usac = models.IntegerField(blank=True, null=True)
    lastnotified = models.IntegerField(db_column='lastNotified', blank=True, null=True)  # Field name made lowercase.
    bib = models.IntegerField(blank=True, null=True)
    eventid = models.ForeignKey(AcaEvent, models.DO_NOTHING, db_column='eventId', blank=True, null=True)  # Field name made lowercase.
    eventracegroupid = models.ForeignKey(AcaRacegroup, models.DO_NOTHING, db_column='eventRaceGroupId', blank=True, null=True)  # Field name made lowercase.
    racerid = models.ForeignKey('AcaUser', models.DO_NOTHING, db_column='racerId', blank=True, null=True)  # Field name made lowercase.
    useronedayid = models.ForeignKey('AcaUsersingleday', models.DO_NOTHING, db_column='userOneDayId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_result'


class AcaResultset(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    starters = models.IntegerField(blank=True, null=True)
    published = models.IntegerField(blank=True, null=True)
    finishphoto = models.CharField(db_column='finishPhoto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    laptimes = models.CharField(db_column='lapTimes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eventid = models.ForeignKey(AcaEvent, models.DO_NOTHING, db_column='eventId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_resultset'


class AcaResultsetracegroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    racegroupid = models.IntegerField(db_column='raceGroupId', blank=True, null=True)  # Field name made lowercase.
    starters = models.IntegerField(blank=True, null=True)
    ugtype = models.CharField(db_column='ugType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    resultsetid = models.ForeignKey(AcaResultset, models.DO_NOTHING, db_column='resultSetId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_resultsetracegroup'


class AcaScheduledaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    action = models.CharField(max_length=255, blank=True, null=True)
    rundate = models.IntegerField(db_column='runDate', blank=True, null=True)  # Field name made lowercase.
    completed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_scheduledaction'


class AcaSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(db_column='createdOn')  # Field name made lowercase.
    lastmodifiedon = models.IntegerField(db_column='lastModifiedOn')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_setting'


class AcaStaticpage(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_staticpage'


class AcaTeamresultsbyevent(models.Model):
    id = models.BigAutoField(primary_key=True)
    competitionid = models.IntegerField(db_column='competitionId')  # Field name made lowercase.
    eventid = models.IntegerField(db_column='eventId', blank=True, null=True)  # Field name made lowercase.
    racetype = models.CharField(db_column='raceType', max_length=16, blank=True, null=True)  # Field name made lowercase.
    clubid = models.IntegerField(db_column='clubId', blank=True, null=True)  # Field name made lowercase.
    racegroupid = models.IntegerField(db_column='raceGroupId', blank=True, null=True)  # Field name made lowercase.
    place = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    riders = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_teamresultsbyevent'


class AcaTrack(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_track'


class AcaTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    txnid = models.CharField(db_column='txnId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dateposted = models.IntegerField(db_column='datePosted', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cardlast4 = models.CharField(db_column='cardLast4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cardfirst = models.CharField(db_column='cardFirst', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardlast = models.CharField(db_column='cardLast', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardexpmonth = models.CharField(db_column='cardExpMonth', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cardexpyear = models.CharField(db_column='cardExpYear', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cardcity = models.CharField(db_column='cardCity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardstate = models.CharField(db_column='cardState', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardzip = models.CharField(db_column='cardZip', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardemail = models.CharField(db_column='cardEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardaddress = models.CharField(db_column='cardAddress', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_transaction'


class AcaTransactionItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    productcode = models.CharField(db_column='productCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    classdescription = models.CharField(db_column='classDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=45)
    datefilled = models.IntegerField(db_column='dateFilled', blank=True, null=True)  # Field name made lowercase.
    datecancelled = models.IntegerField(db_column='dateCancelled', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField()
    targetid = models.IntegerField(db_column='targetId', blank=True, null=True)  # Field name made lowercase.
    productid = models.IntegerField(db_column='productId', blank=True, null=True)  # Field name made lowercase.
    txnid = models.ForeignKey(AcaTransaction, models.DO_NOTHING, db_column='txnId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_transaction_item'


class AcaTransactionItemOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=500)
    productoptionid = models.IntegerField(db_column='productOptionId')  # Field name made lowercase.
    productoptionvalueid = models.IntegerField(db_column='productOptionValueId', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField()
    transactionitemid = models.ForeignKey(AcaTransactionItem, models.DO_NOTHING, db_column='transactionItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_transaction_item_option'


class AcaUsacrider(models.Model):
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
    birthdate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_usacrider'


class AcaUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    acamembership = models.CharField(db_column='acaMembership', max_length=255, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    phonehome = models.CharField(db_column='phoneHome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonework = models.CharField(db_column='phoneWork', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonecell = models.CharField(db_column='phoneCell', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(max_length=255, blank=True, null=True)
    econtact = models.CharField(db_column='eContact', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ephone = models.CharField(db_column='ePhone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    joined = models.DateField(blank=True, null=True)
    replacementtext = models.CharField(db_column='replacementText', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='createdBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    jerseysize = models.CharField(db_column='jerseySize', max_length=5, blank=True, null=True)  # Field name made lowercase.
    optin = models.CharField(db_column='optIn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usac = models.CharField(max_length=255, blank=True, null=True)
    daterenewed = models.DateField(db_column='dateRenewed', blank=True, null=True)  # Field name made lowercase.
    licensetype = models.CharField(db_column='licenseType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amountpaid = models.CharField(db_column='amountPaid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    startdate = models.IntegerField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    expires = models.IntegerField(blank=True, null=True)
    drupalid = models.IntegerField(db_column='drupalId', blank=True, null=True)  # Field name made lowercase.
    changepassword = models.IntegerField(db_column='changePassword', blank=True, null=True)  # Field name made lowercase.
    isnewlicense = models.IntegerField(db_column='isNewLicense')  # Field name made lowercase.
    usacimportdate = models.IntegerField(db_column='usacImportDate', blank=True, null=True)  # Field name made lowercase.
    usacbatch = models.IntegerField(db_column='usacBatch', blank=True, null=True)  # Field name made lowercase.
    notificationdate = models.IntegerField(db_column='notificationDate', blank=True, null=True)  # Field name made lowercase.
    trackcertifiedon = models.IntegerField(db_column='trackCertifiedOn', blank=True, null=True)  # Field name made lowercase.
    lastclubmodification = models.IntegerField(db_column='lastClubModification', blank=True, null=True)  # Field name made lowercase.
    lastcredentialmodification = models.IntegerField(db_column='lastCredentialModification', blank=True, null=True)  # Field name made lowercase.
    lastmodification = models.IntegerField(db_column='lastModification', blank=True, null=True)  # Field name made lowercase.
    sms_optin = models.IntegerField(blank=True, null=True)
    trackcertifiedby = models.ForeignKey(AcaTrack, models.DO_NOTHING, db_column='trackCertifiedBy', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=32, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)
    dob = models.CharField(max_length=16, blank=True, null=True)
    address1 = models.CharField(max_length=128, blank=True, null=True)
    address2 = models.CharField(max_length=1, blank=True, null=True)
    resident = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_user'


class AcaUserbatch(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    batchid = models.IntegerField(db_column='batchId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_userbatch'


class AcaUserclub(models.Model):
    id = models.BigAutoField(primary_key=True)
    startdate = models.IntegerField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.IntegerField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    discipline = models.CharField(max_length=50)
    clubid = models.ForeignKey(AcaClub, models.DO_NOTHING, db_column='clubId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey(AcaUser, models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_userclub'


class AcaUserproxies(models.Model):
    id = models.BigAutoField(primary_key=True)
    parentid = models.IntegerField(db_column='parentId', blank=True, null=True)  # Field name made lowercase.
    childid = models.IntegerField(db_column='childId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aca_userproxies'
        unique_together = (('parentid', 'childid'),)


class AcaUsersingleday(models.Model):
    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dateadded = models.IntegerField(db_column='dateAdded', blank=True, null=True)  # Field name made lowercase.
    racercategory = models.IntegerField(db_column='racerCategory', blank=True, null=True)  # Field name made lowercase.
    usac = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aca_usersingleday'


class AppHomebannerimage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'app_homebannerimage'


class AppHomeinformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'app_homeinformation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    acamembership = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=1024, blank=True, null=True)
    lastname = models.CharField(max_length=1024, blank=True, null=True)
    gender = models.CharField(max_length=1024, blank=True, null=True)
    address1 = models.CharField(max_length=1024, blank=True, null=True)
    address2 = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=1024, blank=True, null=True)
    state = models.CharField(max_length=1024, blank=True, null=True)
    zip = models.CharField(max_length=1024, blank=True, null=True)
    phonehome = models.CharField(max_length=1024, blank=True, null=True)
    phonework = models.CharField(max_length=1024, blank=True, null=True)
    phonecell = models.CharField(max_length=1024, blank=True, null=True)
    fax = models.CharField(max_length=1024, blank=True, null=True)
    econtact = models.CharField(max_length=1024, blank=True, null=True)
    ephone = models.CharField(max_length=1024, blank=True, null=True)
    joined = models.CharField(max_length=1024, blank=True, null=True)
    replacementtext = models.CharField(max_length=1024, blank=True, null=True)
    createdby = models.CharField(max_length=1024, blank=True, null=True)
    jerseysize = models.CharField(max_length=1024, blank=True, null=True)
    resident = models.CharField(max_length=1024, blank=True, null=True)
    optin = models.CharField(max_length=1024, blank=True, null=True)
    usac = models.IntegerField(blank=True, null=True)
    daterenewed = models.CharField(max_length=1024, blank=True, null=True)
    licensetype = models.CharField(max_length=1024, blank=True, null=True)
    amountpaid = models.CharField(max_length=1024, blank=True, null=True)
    startdate = models.IntegerField(blank=True, null=True)
    expires = models.IntegerField(blank=True, null=True)
    drupalid = models.IntegerField(blank=True, null=True)
    changepassword = models.IntegerField(blank=True, null=True)
    isnewlicense = models.IntegerField(blank=True, null=True)
    usacimportdate = models.IntegerField(blank=True, null=True)
    usacbatch = models.IntegerField(blank=True, null=True)
    notificationdate = models.CharField(max_length=1024, blank=True, null=True)
    trackcertifiedon = models.IntegerField(blank=True, null=True)
    trackcertifiedby = models.IntegerField(blank=True, null=True)
    lastclubmodification = models.IntegerField(blank=True, null=True)
    lastcredentialmodification = models.IntegerField(blank=True, null=True)
    lastmodification = models.IntegerField(blank=True, null=True)
    sms_optin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
