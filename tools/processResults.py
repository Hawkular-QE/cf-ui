import sys
import lxml.html


# The purpose of this script is to remove nodes and node attributes
# from the junit .xml result file so that it can then be exported
# to Prolarion via the CI Jenkins Polarion Exporter (V1.3.x).

if len(sys.argv) != 2:
    print "Usage: {} <results.xml>".format(sys.argv[0])
    exit(-1)

in_file = sys.argv[1]
out_file = 'results_export_to_polarion.xml'

root = lxml.etree.parse(in_file)

# Remove nodes
system_err = root.findall('testcase/system-err')
for node in system_err:
    parent = node.getparent()
    parent.remove(node)

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
root.write(out_file)