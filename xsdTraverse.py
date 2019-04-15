# traverse xsd schema to output a nested xpath structure
# By Bingyin Hu, 04/14/2019
from lxml import etree

class xsdTraverse():
    def __init__(self, xsd):
        self.tree = etree.parse(xsd)
        self.header = self.tree.getroot().tag
        self.eheader = self.header.replace('schema', 'element') # element header
        self.findroot()
        self.xsd2dict()
        # self.xsd2dicttest("DataSourceType")
        self.leaf = []
        self.getLeaf(self.dictform)

    # find root
    def findroot(self):
        self.root = self.tree.find(".//*[@type='Root']")

    # recurrsive call to make the dictform
    def xsd2dict(self):
        # rootName = self.root.attrib['name']
        self.dictform = self.xsd2dictHelper(self.root.get('name'), 'Root')

    # recurrsion helper
    # 1) find the complexType with @name == mytype
    # 2) loop through its element
    # 3) make the recurrsive call with the type of elements if not xsd built-in
    def xsd2dictHelper(self, myname, mytype):
        # base case
        # print("%s, %s" %(myname, mytype))
        if mytype is None or mytype.find('xsd:') == 0:
            return myname
        # general case
        currentLv = []
        branches = self.tree.findall(".//*[@name='%s']" %(mytype))
        for branch in branches:
            if branch.tag != self.eheader:
                break
        for ele in branch.iter(self.eheader):
            currentLv.append(self.xsd2dictHelper(ele.get('name'), ele.get('type')))
        return {myname: currentLv}

    # a function to print out the hierachical structure of the dictform
    def printTraversal(self, dictform, level=0):
        # either input a dict or a str
        if isinstance(dictform, dict):
            for key in dictform:
                print level*'---' + key
                for ele in dictform[key]: # dictform[key] is a list
                    self.printTraversal(ele, level+1)
        elif isinstance(dictform, str):
            print level*'---' + dictform

    # a function to collect the xpath of leaf nodes
    def getLeaf(self, dictform, xpath=''):
        # either input a dict or a str
        if isinstance(dictform, dict):
            for key in dictform:
                for ele in dictform[key]: # dictform[key] is a list
                    if xpath == '':
                        self.getLeaf(ele, key)
                    else:
                        self.getLeaf(ele, xpath + '/' + key)
        elif isinstance(dictform, str):
            self.leaf.append(xpath + '/' + dictform)

    # a funtion that outputs the collected xpath of leaf nodes to csv
    def outputLeaf(self):
        with open('leaf.csv','wb') as f:
            for lf in self.leaf:
                f.write(lf + '\n')
        print("XPath of leaf nodes is written in leaf.csv")

    def xsd2dicttest(self, testtype):
        # rootName = self.root.attrib['name']
        self.dictform = self.xsd2dictHelper(self.tree.find(".//*[@type='%s']" %(testtype)).get('name'), testtype)


if __name__ == '__main__':
    xsdt = xsdTraverse('D:/Dropbox/DIBBS/nanomine-schema/xml/PNC_schema_081218.xsd')
    # xsdt.printTraversal(xsdt.dictform)
    xsdt.outputLeaf()