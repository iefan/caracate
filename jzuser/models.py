#coding:utf8
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class MyUserManager(BaseUserManager):
    def create_user(self, unitsn, unitname, unitgroup, operatorname,password=None):
        """
        Creates and saves a User with the given email, unitsn, unitname.
        """
        
        if not unitsn:
            raise ValueError('Users must have an sn.')

        user = self.model(
            unitsn = unitsn,
            # email=MyUserManager.normalize_email(email),
            unitname=unitname,
            unitgroup = unitgroup,
            operatorname = operatorname,
            # is_staff=False,
            # is_active=True,
            # is_superuser=False,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, unitsn, unitname, unitgroup, operatorname, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(unitsn, 
            # email,
            password=password,
            unitname=unitname,
            unitgroup = unitgroup,
            operatorname = operatorname,
        )
        # user.is_staff = True
        # user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        # user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    unitsn = models.CharField(verbose_name='单位编码', max_length=30, unique=True, db_index=True)
    # email = models.EmailField(verbose_name='电子邮箱', max_length=255, unique=True,)
    unitname = models.CharField(max_length=100, verbose_name="单位名称")
    UNITGROUP_CHOICES = (
        ('0', u'市残联'),
        ('1', u'区残联'),
        ('2', u'医院'),
    )
    unitgroup = models.CharField(max_length=30, choices=UNITGROUP_CHOICES, verbose_name="单位类别")
    operatorname = models.CharField(max_length=30, verbose_name="操作人员")
    # unitname = models.DateField()
    is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'unitsn'
    REQUIRED_FIELDS = ['unitname', 'unitgroup', 'operatorname']

    def get_full_name(self):
        # The user is identified by unitsn
        return self.unitsn

    def get_short_name(self):
        # The user is identified by their email address
        return self.unitsn 

    def __unicode__(self):
        s= "%s" % (self.unitsn)
        return s

    class Meta:        
        verbose_name = "用户信息"  
        verbose_name_plural = "用户信息"  
        # app_label = u"信息管理"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin   
# Create your models here.
