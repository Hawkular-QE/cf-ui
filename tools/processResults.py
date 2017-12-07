#!/usr/bin/python
import sys
import lxml.html


# The purpose of this script is to remove nodes and node attributes
# from the junit .xml result file so that it can then be exported
# to Prolarion via the CI Jenkins Polarion Exporter (V1.3.x).

OUT_FILE = 'results_export_to_polarion.xml'

if len(sys.argv) < 2:
    print "Usage: {} results.xml <output.xml>".format(sys.argv[0])
    exit(-1)

in_file = sys.argv[1]

if len(sys.argv) > 2:
    out_file = sys.argv[2]
else:
    out_file = OUT_FILE

try:
    root = lxml.etree.parse(in_file)
except Exception, e:
    raise Exception(e)

# Remove nodes
system_err = root.findall('testcase/system-err')
for node in system_err:
    parent = node.getparent()
    parent.remove(node)

#Remove failure texts
failures = root.findall('testcase/failure')
for node in failures:
    node.text = ''
    node.set('type', 'failure')

#Remove error texts
errors = root.findall('testcase/error')
for node in errors:
    node.text = ''
    node.set('type', 'error')

#Remove skipped testcases
skips = root.findall('testcase/skipped')
for node in skips:
    node.getparent().getparent().remove(node.getparent())

#Fix the polarion project name
suite = root.getroot()
suite.set('name', 'JBossON4')

# Remove Node Attributes
for e in root.iter():
    # print e.tag, e.attrib
    try:
        del e.attrib['skips']
    except:
        pass

    try:
        del e.attrib['line']
    except:
        pass

    try:
        del e.attrib['file']
    except:
        pass

print "Writing to output file: {}".format(out_file)

try:
    root.write(out_file)
except Exception, e:
    raise Exception(e)
