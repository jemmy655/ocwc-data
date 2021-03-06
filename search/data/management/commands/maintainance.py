# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import hashlib
from optparse import make_option

from data.models import Course, Source

class Command(BaseCommand):
    help = "One time mantainance operation on data models"
    args = "--fix-hashes"

    option_list = BaseCommand.option_list + (
        make_option("--fix-hashes", action="store_true", dest="fix_hashes", help="Regenerates linkhash and removes duplicates"),
    )

    def handle(self, *args, **options):
        if options.get('fix_hashes'):
            self.fix_hashes()

    def fix_hashes(self):
        # remove wrongly calculated hashes and generate new ones
        for course in Course.objects.order_by('-id'):
          digest = hashlib.md5(course.linkurl.encode('utf-8')).hexdigest()

          if digest != course.linkhash:
              try:
                  Course.objects.get(linkhash=digest)
                  course.delete()
              except Course.DoesNotExist:
                  print 'new digest for', [course.title]
                  course.linkhash = digest
                  course.save()

    def check_broken_links(self):
        pass
        # for jos_course in JosOcwCatalogCourses.objects.filter(pk__gt=6035):
        #   try:
        #       course = Course.objects.get(linkhash=jos_course.linkhash)
        #   except Course.DoesNotExist:
        #       # print jos_course.linkhash, jos_course.source, jos_course.title
        #       # print [jos_course.source]
        #       print jos_course.id, jos_course.linkurl
        #       r = requests.get(jos_course.linkurl)
        #       if r.status_code == 404:
        #           print 'deleting'
        #           jos_course.delete()
        