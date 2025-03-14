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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

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


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Buyers(models.Model):
    buyerid = models.AutoField(db_column='BuyerID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', unique=True, max_length=20)  # Field name made lowercase.
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'buyers'


class Conversations(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    buyerid = models.ForeignKey(Buyers, models.DO_NOTHING, db_column='BuyerID')  # Field name made lowercase.
    sellerid = models.ForeignKey('Sellers', models.DO_NOTHING, db_column='SellerID')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conversations'
        unique_together = (('buyerid', 'sellerid'),)


class Dealers(models.Model):
    dealerid = models.AutoField(db_column='DealerID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=50)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    reviewsandratings = models.TextField(db_column='ReviewsAndRatings', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dealers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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


class Favourites(models.Model):
    favouriteid = models.AutoField(db_column='FavouriteID', primary_key=True)  # Field name made lowercase.
    buyerid = models.ForeignKey(Buyers, models.DO_NOTHING, db_column='BuyerID')  # Field name made lowercase.
    producttype = models.CharField(db_column='ProductType', max_length=12)  # Field name made lowercase.
    productid = models.IntegerField(db_column='ProductID')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'favourites'


class Implements(models.Model):
    implementid = models.AutoField(db_column='ImplementID', primary_key=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    power = models.IntegerField(db_column='Power')  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dealerid = models.ForeignKey(Dealers, models.DO_NOTHING, db_column='DealerID', blank=True, null=True)  # Field name made lowercase.
    reviewsandratings = models.TextField(db_column='ReviewsAndRatings', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'implements'


class Messages(models.Model):
    message_id = models.AutoField(db_column='Message_id', primary_key=True)  # Field name made lowercase.
    conversation = models.ForeignKey(Conversations, models.DO_NOTHING)
    content = models.TextField()
    sender_type = models.CharField(max_length=6)
    sender_id = models.IntegerField()
    timestamp = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    reply_to = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'


class Sellers(models.Model):
    sellerid = models.AutoField(db_column='SellerID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', unique=True, max_length=20)  # Field name made lowercase.
    reviewsandratings = models.TextField(db_column='ReviewsAndRatings', blank=True, null=True)  # Field name made lowercase.
    companydetails = models.TextField(db_column='CompanyDetails', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(unique=True, max_length=100)
    logo = models.CharField(db_column='Logo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sellers'


class SocialAuthAssociation(models.Model):
    id = models.BigAutoField(primary_key=True)
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    id = models.BigAutoField(primary_key=True)
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=32)
    next_step = models.PositiveSmallIntegerField()
    backend = models.CharField(max_length=32)
    timestamp = models.DateTimeField()
    data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    extra_data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


class Tractors(models.Model):
    tractorid = models.AutoField(db_column='TractorID', primary_key=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    hppower = models.IntegerField(db_column='HpPower')  # Field name made lowercase.
    ccpower = models.IntegerField(db_column='CcPower')  # Field name made lowercase.
    favorite = models.IntegerField(db_column='Favorite', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    reviewsandratings = models.TextField(db_column='ReviewsAndRatings', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tractors'


class Usedtractors(models.Model):
    tractorid = models.AutoField(db_column='TractorID', primary_key=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    hppower = models.IntegerField(db_column='HpPower')  # Field name made lowercase.
    ccpower = models.IntegerField(db_column='CcPower')  # Field name made lowercase.
    sellerid = models.ForeignKey(Sellers, models.DO_NOTHING, db_column='SellerID', blank=True, null=True)  # Field name made lowercase.
    favorite = models.IntegerField(db_column='Favorite', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hoursused = models.IntegerField(db_column='HoursUsed')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    reviewsandratings = models.TextField(db_column='ReviewsAndRatings', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usedtractors'
