#! /usr/bin/python3
import os
import sys
import argparse
from androguard.core.bytecodes import apk
from androguard.core import androconf
from androguard.core.bytecodes.axml import ARSCParser
from lxml import etree
import lxml.etree


def get_firebase(fpath):
    """Returns the Firebase URL from the given APK file.
    Parameters:
        - fpath (str): The file path of the APK file.
    Returns:
        - str: The Firebase URL found in the APK file, if any.
    Processing Logic:
        - Parses the APK file using the apk.APK() function.
        - Retrieves the Android resources using the get_android_resources() function.
        - Checks if the retrieved resources are not empty.
        - Extracts the public resources from the first package using the get_public_resources() function.
        - Converts the extracted resources into an XML tree using the fromstring() function.
        - Iterates through the XML tree and checks for elements with type 'string'.
        - Retrieves the resolved resource configurations using the get_resolved_res_configs() function.
        - Checks if the retrieved value ends with 'firebaseio.com'.
        - Returns the Firebase URL if found, otherwise returns None."""
    
    a = apk.APK(fpath)
    arscobj = a.get_android_resources()
    if not arscobj:
        return None
    xmltree = arscobj.get_public_resources(arscobj.get_packages_names()[0])
    x = etree.fromstring(xmltree, parser=lxml.etree.XMLParser(resolve_entities=False))
    for elt in x:
        if elt.get('type') == 'string':
            val = arscobj.get_resolved_res_configs(int(elt.get('id')[2:], 16))[0][1]
            if val.endswith('firebaseio.com'):
                return val
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH", help="Path of a folder")
    args = parser.parse_args()


    if os.path.isdir(args.PATH):
        for f in os.listdir(args.PATH):
            fpath = os.path.join(args.PATH, f)
            if os.path.isfile(fpath):
                if androconf.is_android(fpath) == 'APK':
                    r = get_firebase(fpath)
                    if r:
                        print("{} : {}".format(fpath, r))
    elif os.path.isfile(args.PATH):
        if androconf.is_android(args.PATH) == 'APK':
            r = get_firebase(args.PATH)
            if r:
                print(r)
    else:
        print("Please give an APK file or a folder")
