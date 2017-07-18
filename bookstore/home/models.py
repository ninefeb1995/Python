# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class BookImage(models.Model):
    #book_image_id = models.AutoField(primary_key=True)
    book_image_path = models.TextField()  # This field type is a guess.


class Category(models.Model):
    #cate_id = models.AutoField(primary_key=True)
    cate_name = models.TextField()  # This field type is a guess.
    cate_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.NullBooleanField()


class Book(models.Model):
    #book_id = models.AutoField(primary_key=True)
    cate_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_name = models.TextField()  # This field type is a guess.
    book_quantity = models.IntegerField()
    book_image_id = models.ForeignKey(BookImage, on_delete=models.CASCADE)
    book_author = models.TextField()  # This field type is a guess.
    detail = models.TextField()  # This field type is a guess.
    book_is_new = models.BooleanField()


# class User(AbstractBaseUser):
#     #user_id = models.AutoField(primary_key=True)
#     user_username = models.TextField(unique=True)  # This field type is a guess.
#     user_password = models.TextField()  # This field type is a guess.
#     user_email = models.TextField(unique=True)  # This field type is a guess.
#     user_name = models.TextField()  # This field type is a guess.
#     user_type = models.TextField()  # This field type is a guess.
#
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     USERNAME_FIELD = 'user_username'
#     REQUIRED_FIELDS = []
#
#     objects = BaseUserManager()
#
#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.user_name
#
#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.user_name
#
#     def __unicode__(self):
#         return self.user_name
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin


class Order(models.Model):
    #order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.CASCADE)
    order_date = models.DateTimeField()
    order_status = models.BooleanField()


class OrderDetail(models.Model):
    #order_detail_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, models.CASCADE)
    book_id = models.ForeignKey(Book, models.CASCADE)
    order_detail_from_date = models.DateTimeField()
    order_detail_to_date = models.DateTimeField()


class DjangoMigrations(models.Model):
    #id = models.AutoField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()
