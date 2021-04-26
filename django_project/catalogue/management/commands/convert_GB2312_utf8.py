__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '3/8/16'

import os
import sys
import glob
from tempfile import mkstemp
from shutil import move
from os import remove, close
from django.core.management.base import BaseCommand


halt_on_error = True
# source_path=('/home/web/django_project/data/CBERS/')

class Command(BaseCommand):
    args = 'path'
    help = 'Convert file from GB2312 encoding to UTF-8'

    def handle(self, *args, **options):
        """Implementation for command

        :param args: path for the main dir '/home/web/django_project/data/CBERS/'
        :type args: str

        :raises: IOError

        """

        if len(args) < 1:
            self.stdout.write("Need argument for directory path "
                              "ex : /home/web/django_project/data/CBERS/")
            return

        path = args[0]

        record_count = 0
        failed_record_count = 0
        print('Starting directory scan...')

        for myFolder in glob.glob(os.path.join(path, '*.XML')):
            record_count += 1
            try:
                # Get the folder name
                product_folder = os.path.split(myFolder)[-1]
                # print product_folder

                # Find the first and only xml file in the folder
                #search_path = os.path.join(str(myFolder), '*.XML')
                # print search_path
                xml_file = glob.glob(myFolder)[0]
                filename = os.path.basename(xml_file)
                print("Converting {} ....".format(filename))
                pattern = 'GB2312'
                subst = 'UTF-8'

                fh, abs_path = mkstemp()
                with open(abs_path,'w') as new_file:
                    with open(xml_file) as old_file:
                        for line in old_file:
                            new_file.write(line.replace(pattern, subst))
                close(fh)
                #Remove original file
                remove(xml_file)
                #Move new file
                move(abs_path, xml_file)

            except Exception as e:
                print('Error when want to convert! : %s' % product_folder)
                failed_record_count += 1
                if halt_on_error:
                    print(e.message)
                    break
                else:
                    continue

        print('===============================')
        print('Products converted : %s ' % record_count)
        print('Products failed to convert : %s ' % failed_record_count)