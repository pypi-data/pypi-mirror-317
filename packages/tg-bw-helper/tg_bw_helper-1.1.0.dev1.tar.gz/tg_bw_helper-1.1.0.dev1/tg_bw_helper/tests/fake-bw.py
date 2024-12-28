#!/usr/bin/env python
import sys


item1 = (
    '{"object":"item","id":"11111111-1111-1111-1111-111111111111",'
    '"organizationId":"11111111-1111-1111-1111-111111111111",'
    '"folderId":null,"type":2,"reprompt":0,"name":"Ansible Vault",'
    '"notes":"Use wisely","favorite":false,"fields":['
    '{"name":"Main ansible","value":"pa$$word","type":1},'
    '{"name":"Legacy ansible","value":"$ecure","type":1}],'
    '"secureNote":{"type":0},"collectionIds":["11111111-1111-1111-1111-111111111111"],'
    '"revisionDate":"2021-08-19T06:01:06.133Z","passwordHistory":[]}'
)

item2 = (
    '{"object":"item","id":"11111111-1111-1111-1111-111111111111",'
    '"organizationId":"11111111-1111-1111-1111-111111111111",'
    '"folderId":null,"type":1,"reprompt":0,"name":"Main ansible",'
    '"notes":null,"favorite":false,"login":{'
    '"username":"","password":"pass","totp":null,"passwordRevisionDate":null},'
    '"collectionIds": ["11111111-1111-1111-1111-111111111111"],'
    '"revisionDate": "2020-08-18T15:26:26.666Z"}'
)

item_bad = (
    '{"object":"item","id":"11111111-1111-1111-1111-111111111111",'
    '"organizationId":"11111111-1111-1111-1111-111111111111",'
    '"folderId":null,"type":2,"reprompt":0,"name":"Ansible Vault",'
    '"notes":"Use wisely","favorite":false,"fields":[{}],'
    '"secureNote":{"type":0},"collectionIds":["11111111-1111-1111-1111-111111111111"]}'
)

if "list" in sys.argv:
    if "item1" in sys.argv:
        print(f"[{item1}]")
    elif "item2" in sys.argv:
        print(f"[{item2}]")
    elif "item3" in sys.argv:
        print("[]")
    elif "item4" in sys.argv:
        print("There was a horrible error, and this is no valid json.")
    elif "item_bad" in sys.argv:
        print(f"[{item_bad}]")
    elif "item" in sys.argv:
        print(f"[{item1},{item2}]")
elif "unlock" in sys.argv:
    print("SESSION_TOKEN")
