# sefaga
secure socket instant messaging

## Depandencies

```
pip install rsa
```

## client

### tree
```
CLIENT
│   gui.py
│   ctools.py
│   POOcom.py
│
│   token.json
│
└───keys
        clt_public.pem
        psw_public.pem
        srv_private.pem
```

### token.json
```json
{
    "name": "token"
}
```

## server

```
SERVER
│   server.py
│   stools.py
│
│   users.json
│
└───keys
        clt_private.pem
        psw_private.pem
        srv_public.pem
```