# Manual steps for next deployment


## Keycloak profile setup

### Realm settings -> User profile

Add following JSON into the JSON editor:

```json
{
  "attributes": [
    {
      "name": "username",
      "displayName": "${username}",
      "validations": {
        "length": {
          "min": 3,
          "max": 255
        },
        "username-prohibited-characters": {},
        "up-username-not-idn-homograph": {}
      },
      "permissions": {
        "view": [
          "admin",
          "user"
        ],
        "edit": [
          "admin",
          "user"
        ]
      },
      "multivalued": false
    },
    {
      "name": "email",
      "displayName": "${email}",
      "validations": {
        "email": {},
        "length": {
          "max": 255
        }
      },
      "required": {
        "roles": [
          "user"
        ]
      },
      "permissions": {
        "view": [
          "admin",
          "user"
        ],
        "edit": [
          "admin",
          "user"
        ]
      },
      "multivalued": false
    },
    {
      "name": "salutation",
      "displayName": "Salutation",
      "validations": {
        "options": {
          "options": [
            "Mrs.",
            "Mr.",
            "neutral"
          ]
        }
      },
      "annotations": {
        "inputType": "select"
      },
      "required": {
        "roles": [
          "admin",
          "user"
        ]
      },
      "permissions": {
        "view": [
          "admin",
          "user"
        ],
        "edit": [
          "admin",
          "user"
        ]
      },
      "multivalued": false
    },
    {
      "name": "firstName",
      "displayName": "${firstName}",
      "validations": {
        "length": {
          "max": 255
        },
        "person-name-prohibited-characters": {}
      },
      "annotations": {},
      "required": {
        "roles": [
          "admin",
          "user"
        ]
      },
      "permissions": {
        "view": [
          "admin",
          "user"
        ],
        "edit": [
          "admin",
          "user"
        ]
      },
      "multivalued": false
    },
    {
      "name": "title",
      "displayName": "Title",
      "validations": {
        "options": {
          "options": [
            "Dr.",
            "Prof.",
            "Prof. Dr.",
            "PD Dr."
          ]
        }
      },
      "annotations": {
        "inputType": "select"
      },
      "permissions": {
        "view": [
          "admin",
          "user"
        ],
        "edit": [
          "admin",
          "user"
        ]
      },
      "multivalued": false
    },
    {
      "name": "lastName",
      "displayName": "${lastName}",
      "validations": {
        "length": {
          "max": 255
        },
        "person-name-prohibited-characters": {}
      },
      "annotations": {},
      "required": {
        "roles": [
          "admin",
          "user"
        ]
      },
      "permissions": {
        "view": [
          "admin",
          "user"
        ],
        "edit": [
          "admin",
          "user"
        ]
      },
      "multivalued": false
    }
  ],
  "groups": [
    {
      "name": "user-metadata",
      "displayHeader": "User metadata",
      "displayDescription": "Attributes, which refer to user metadata"
    }
  ]
}
```

### Clients -> mysagw -> Client scopes -> mysagw-dedicated

Add mappers for `salutation` and `title`.
