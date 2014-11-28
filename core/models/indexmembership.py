##
# indexmembership.py - Created by Timothy Morey on 9/20/2014
#

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


class IndexMembership(models.Model):
    class Meta:
        app_label = 'core'


    index = models.ForeignKey('Index',
                              blank=False,
                              null=False,
                              on_delete=models.CASCADE,
                              related_name='contents')

    content_content_type = models.ForeignKey(ContentType,
                                            related_name='+')
    content_id = models.CharField(max_length=22)
    content = generic.GenericForeignKey('content_content_type', 
                                        'content_id')

    content_order = models.IntegerField()



