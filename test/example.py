#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import logging
from rosco_client import *

API_KEY = "1"

logging.basicConfig(format='[%(levelname)8s] %(name)s: %(message)s')
logging.getLogger().setLevel(logging.WARNING)

def main():
    # Initialize ROSCO object
    rosco = ROSCO(API_KEY)

    ## Get object properties
    # With SHA256 hash
    obj_1 = rosco.get_object("5BD558B9F7F6680F9D4ECE6F656B08938A4949458EA532A6F2C1D0A747EFA02E")

    # With SHA1 hash
    obj_2 = rosco.get_object("4DD03EE95B486E1B129DCAE5BEFBE3CAA8953EB1")

    # With MD5 hash
    obj_3 = rosco.get_object("02904AF19414464F19104111012BCFE8")

    print obj_1 == obj_2 and obj_2 == obj_3 and obj_1 == obj_3 #True
    print obj_1


    ## Get connected objects
    # With SHA256 hash
    conn_obj_1 = rosco.get_connected_object("5BD558B9F7F6680F9D4ECE6F656B08938A4949458EA532A6F2C1D0A747EFA02E")

    # With SHA1 hash
    conn_obj_2 = rosco.get_connected_object("4DD03EE95B486E1B129DCAE5BEFBE3CAA8953EB1")

    # With MD5 hash
    conn_obj_3 = rosco.get_connected_object("02904AF19414464F19104111012BCFE8")

    print conn_obj_1 == conn_obj_2 and conn_obj_2 == conn_obj_3 and conn_obj_1 == conn_obj_3 #True
    print conn_obj_1


    ## Search
    # Certificate search
    c = CertSearch()
    c.add_filter(c.Filters.issuer_common_name, prefix='Microsoft Root Certificate Authority')
    certs = rosco.search(c)

    print "Number of searched certificates:", len(certs)
    for cert in certs:
        print cert.subject_common_name

    # PE search
    p = PESearch()
    p.add_filter(
        p.Filters.timestamp,
        start=ROSCO.date_to_string(datetime(2012, 11, 6)),
        stop=ROSCO.date_to_string(datetime(2012, 12, 6))
    )
    pes = rosco.search(p)

    print "Number of searched PE's:", len(pes)
    for pe in pes:
        print pe.linker_version

    # APK search
    a = APKSearch()
    a.add_filter(a.Filters.permissions, substring='br.com')
    apks = rosco.search(a)

    print "Number of searched APK's:", len(apks)
    for apk in apks:
        print apk.package_name

    # Get the verified PE's, JAR'a, APK's by certificate
    begin_object = rosco.get_object("958CF204EB1A52020F2FFB3B024CDE738B726C750A04669CF907837C3F4B72A7")
    objects = rosco.get_verified_objects(begin_object, (PE, JAR, APK))
    for object in objects:
        print object.sha256

    # Get the root certificate for an object
    begin_object = rosco.get_object("5BD558B9F7F6680F9D4ECE6F656B08938A4949458EA532A6F2C1D0A747EFA02E")
    certs = rosco.get_verifier_certs(begin_object)
    for cert in certs:
        print cert.issuer_common_name
        print cert.sha256


    ## File upload
    rosco.upload("upload.exe")

if __name__ == "__main__":
    main()
