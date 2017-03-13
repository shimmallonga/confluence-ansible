#!/usr/bin/python

from ansible.module_utils.basic import *
import requests
import base64
import simplejson


def conf_create(data):

    username = data['username']
    password = data['password']
    title = data['title']
    ancestor = data['ancestor']
    api_url = data['url']


    url = "{}{}" . format(api_url, '/rest/api/content')

    stringToEncode = username + ":" + password
    encodedString = base64.b64encode(stringToEncode)
    headers = {
        'content-type': "application/json",
        'authorization': "Basic " + encodedString,
        'cache-control': "no-cache",
    }
    querystring = {"os_username":username}
    payload = "{\n    \"type\":\"page\",\n    " + "\"title\":\""+ title +"\",\n "+ "   \"space\":{\"key\":\"SPACE\"}\n    \"ancestors\":[{\"id\":"+ ancestor +"}],\n    \"body\":{\"storage\":{\"value\":\"<h1>" + title +"\"representation\":\"storage\"}}\n}"

    result=requests.request("POST",url,data=payload,headers=headers, params=querystring)
    if result.status_code == 200:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()
    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta




def conf_get(data):


    username = data['username']
    password = data['password']

    # still a work in progress



def main():

    fields = {
        "username": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str"},
        "ancestor": {"required": True, "type": "str"},
        "title": {"required": True, "type": "str"},
        "action": {
            "default": "create",
            "choices": ['create', 'get'],
            "type": 'str'
        },
    }

    choice_map = {
        "create": conf_create,
        "get": conf_get,
    }


    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['action'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()
