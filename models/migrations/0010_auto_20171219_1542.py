# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-19 08:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_auto_20171205_0603'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='model',
            options={'ordering': ('cTitle',), 'verbose_name_plural': 'models'},
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bgenericmodel',
            new_name='bGenericModel',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bgetdescription',
            new_name='bGetDescription',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bgetpictures',
            new_name='bGetPictures',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bkeywordrequired',
            new_name='bKeyWordRequired',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bmusthavebrand',
            new_name='bMustHaveBrand',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bsubmodelsok',
            new_name='bSubModelsOK',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='bwanted',
            new_name='bWanted',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='ccomment',
            new_name='cComment',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='cexcludeif',
            new_name='cExcludeIf',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='cfile1spec',
            new_name='cFileSpec1',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='cfile2spec',
            new_name='cFileSpec2',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='cfile3spec',
            new_name='cFileSpec3',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='cfile4spec',
            new_name='cFileSpec4',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='cfile5spec',
            new_name='cFileSpec5',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='ckeywords',
            new_name='cKeyWords',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='ctitle',
            new_name='cTitle',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='ibrand',
            new_name='iBrand',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='icategory',
            new_name='iCategory',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='ilegacykey',
            new_name='iLegacyKey',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='istars',
            new_name='iStars',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='iuser',
            new_name='iUser',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='tcreate',
            new_name='tCreate',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='tlegacycreate',
            new_name='tLegacyCreate',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='tlegacymodify',
            new_name='tLegacyModify',
        ),
        migrations.RenameField(
            model_name='model',
            old_name='tmodify',
            new_name='tModify',
        ),
    ]
