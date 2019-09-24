from openalpr import Alpr
import sys
from locale import setlocale
setlocale(0, "C")
alpr = Alpr('eu', '/usr/share/openalpr/config/openalpr.defaults.conf',
            '/usr/share/openalpr/runtime_data')



if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("lt")


results = alpr.recognize_file('/root/Projects/Final_Park_6_05/Pentagon/cars/2019-05-07 14:24:40_5.jpg')
max = 0
i = 0
for plate in results['results']:
    i += 1
    print("Plate #%d" % i)
    print("   %12s %12s" % ("Plate", "Confidence"))
    for candidate in plate['candidates']:
        prefix = "-"
        if candidate['matches_template']:
            prefix = "*"

        print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))


# Call when completely done to release memory
alpr.unload()