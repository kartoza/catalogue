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
    help = 'Convert file from GB2312 encoding to UTF-8'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Directory path containing XML files to convert')

    def handle(self, *args, **options):
        """Implementation for command

        :param args: Not used in modern Django
        :param options: Command options including 'path'
        :type options: dict

        :raises: IOError

        """

        path = options['path']
        if not path:
            self.stdout.write("Need argument for directory path "
                              "ex : /home/web/django_project/data/CBERS/")
            return

        record_count = 0
        failed_record_count = 0
        print('Starting directory scan...')
        print(f'Scanning path: {path}')
        
        # Check for both uppercase and lowercase XML extensions
        xml_pattern1 = os.path.join(path, '*.XML')
        xml_pattern2 = os.path.join(path, '*.xml')
        
        xml_files = glob.glob(xml_pattern1) + glob.glob(xml_pattern2)
        print(f'Found {len(xml_files)} XML files')
        
        if not xml_files:
            print('No XML files found in the directory!')
            print(f'Checked patterns: {xml_pattern1} and {xml_pattern2}')
            return

        for xml_file in xml_files:
            record_count += 1
            try:
                # Get the file name
                filename = os.path.basename(xml_file)
                print("Converting {} ....".format(filename))
                pattern = 'GB2312'
                subst = 'UTF-8'

                fh, abs_path = mkstemp()
                with open(abs_path, 'w', encoding='utf-8') as new_file:
                    with open(xml_file, 'r', encoding='gb2312') as old_file:
                        for line in old_file:
                            new_file.write(line.replace(pattern, subst))
                close(fh)
                # Remove original file
                remove(xml_file)
                # Move new file
                move(abs_path, xml_file)

            except Exception as e:
                print('Error when want to convert! : %s' % filename)
                failed_record_count += 1
                if halt_on_error:
                    print(str(e))
                    break
                else:
                    continue

        print('===============================')
        print('Products converted : %s ' % record_count)
        print('Products failed to convert : %s ' % failed_record_count)
