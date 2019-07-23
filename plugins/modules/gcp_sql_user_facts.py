#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_sql_user_facts
description:
- Gather facts for GCP User
short_description: Gather facts for GCP User
version_added: 2.8
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  instance:
    description:
    - The name of the Cloud SQL instance. This does not include the project ID.
    - 'This field represents a link to a Instance resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''name'' and value of
      your resource''s name Alternatively, you can add `register: name-of-resource`
      to a gcp_sql_instance task and then set this instance field to "{{ name-of-resource
      }}"'
    required: true
    type: dict
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name: " a user facts"
  gcp_sql_user_facts:
    instance: "{{ instance }}"
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
'''

RETURN = '''
resources:
  description: List of resources
  returned: always
  type: complex
  contains:
    host:
      description:
      - The host name from which the user can connect. For insert operations, host
        defaults to an empty string. For update operations, host is specified as part
        of the request URL. The host name cannot be updated after insertion.
      returned: success
      type: str
    name:
      description:
      - The name of the user in the Cloud SQL instance.
      returned: success
      type: str
    instance:
      description:
      - The name of the Cloud SQL instance. This does not include the project ID.
      returned: success
      type: dict
    password:
      description:
      - The password for the user.
      returned: success
      type: str
'''

################################################################################
# Imports
################################################################################
from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json

################################################################################
# Main
################################################################################


def main():
    module = GcpModule(argument_spec=dict(instance=dict(required=True, type='dict')))

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/sqlservice.admin']

    items = fetch_list(module, collection(module))
    if items.get('items'):
        items = items.get('items')
    else:
        items = []
    return_value = {'resources': items}
    module.exit_json(**return_value)


def collection(module):
    res = {'project': module.params['project'], 'instance': replace_resource_dict(module.params['instance'], 'name')}
    return "https://www.googleapis.com/sql/v1beta4/projects/{project}/instances/{instance}/users".format(**res)


def fetch_list(module, link):
    auth = GcpSession(module, 'sql')
    response = auth.get(link)
    return return_if_object(module, response)


def return_if_object(module, response):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


if __name__ == "__main__":
    main()
