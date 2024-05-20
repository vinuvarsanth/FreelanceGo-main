from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'
def get_default_profile_image():
    return 'default/profile_image.png'
class Account(AbstractBaseUser):
    status = [('c', 'client'), ('f', 'freelancer')]
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    profile_image           = models.ImageField(max_length=255,upload_to=get_profile_image_filepath,null=True,blank=True, default = get_default_profile_image)
    hide_email              = models.BooleanField(default=True)
    phone                   = models.CharField(max_length=12, unique=True)
    user_type               = models.CharField(max_length=50, default='f', choices=status)
    skills                  = models.TextField(max_length=500, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone','user_type']
 
    objects = MyAccountManager()
    def __str__(self):
        return self.username
    
    @property
    def ImageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
