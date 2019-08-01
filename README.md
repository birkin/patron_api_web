### Overview

This is a python [flask](http://flask.pocoo.org) web-wrapper around a [patron-api library](https://github.com/birkin/patron_api).

Info from that libary's readme...

For a few purposes, we access data from our [iii-millennium](http://iii.com/products/millennium) patron-api.

The response that comes back is html and the data elements are simply strings. JSON would be much more useful.

This web-service offers that patron-api string output as nice json hash elements.

The service is used internally, so no demo link is provided. But to give an example, instead of raw patron-api output like:

```
<HTML><BODY>
...
PATRN NAME[pn]=Demolast, Demofirst<BR>
P BARCODE[pb]=1 2222 33333 4444<BR>
...
</BODY></HTML>
```

...it instead returns:

```
{
    "patrn_name": {
        "label": "PATRN NAME",
        "code": "pn",
        "value": "Demolast, Demofirst" },
    "p_barcode": {
        "label": "P BARCODE",
        "code": "pb",
        "value": "1 2222 33333 4444",
        "converted_value": "12222333334444" }
}
```

---
