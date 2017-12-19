Endpoints
=========

Search
------

This endpoint returns search results from the CIPO patent database for a given query. The response includes ``count``, and a couple key details to identify each patent found.

Always check ``limit_exceeded`` first because CIPO limits search results to 1,000 per query. The list of patents in the response is incomplete if ``limit_exceeded`` is ``True``.
The suggested workaround is to use ``date-field``, ``date-start``, and ``date-end`` to narrow the search scope. Repeated queries with consecutive date ranges may then be used to build the complete list of results.

The patents are listed in the same order as retrieved from CIPO. While none of the parameters below are always required, at least one parameter must be provided for each query.

Endpoint
    GET https://api.patentology.org/v1/search

Query Parameters
^^^^^^^^^^^^^^^^

=============== ==================================================================================================================================================
Parameter	    Description
=============== ==================================================================================================================================================
keyword	        Term in any of the following fields: title, abstract, claims, inventor, owner, applicant, ipc, cpc, pct, ipn.
title	        Word or phrase in title.
abstract	    Word or phrase in abstract.
claims	        Word or phrase in claims.
inventor	    Word or phrase in name(s) of inventor(s).
owner	        Word or phrase in name(s) of owner(s).
applicant	    Word or phrase in name(s) of applicant(s).
ipc	            Search by classification(s) or a portion of a classification corresponding to the International Patent Classification (IPC).
cpc	            Search by classification(s) or a portion of a classification corresponding to the Canadian Patent Classification (IPC).
pct	            Search by PCT Filing Number assigned by the World Intellectual Property Organization (WIPO).
ipn	            Search by the International Publication Number assigned by the World Intellectual Property Organization (WIPO).
country	        Inventor country code. See Appendix for allowed values.
status	        Status of patent document. See Appendix for allowed values.
type	        Type of patent document filing. See Appendix for allowed values.
language	    Language of filing. See Appendix for allowed values.
licence-filter	Only find patents with licence availability. See Appendix for allowed values.
date-field	    Date field to search for, if any. See Appendix for allowed values.
date-start	    Starting date of range. Must be formatted as “yyyy-mm-dd”. Required if date-field is anything else than either ‘Date search not active’ or empty.
date-end	    Ending date of range. Must be formatted as “yyyy-mm-dd”. Required if date-field is anything else than either ‘Date search not active’ or empty.
=============== ==================================================================================================================================================



Example Request::

    import requests
    
    payload = {'keyword': 'gesture', 'country': 'CA', 'date-field': 'issue', 'date-start': '2017-01-01', 'date-end': '2017-01-31'}
    r = requests.get('https://api.patentology.org/v1/search', params=payload)

Exampe Response:

.. code-block:: json

    {
        "count": "2", 
        "limit_exceeded": "False",
        "patents": [
            {
                "link": "http://www.ic.gc.ca/opic-cipo/cpd/eng/patent/2748881/summary.html",
                "number": "2748881",
                "title": "GESTURE RECOGNITION METHOD AND INTERACTIVE INPUT SYSTEM EMPLOYING THE SAME"
            },
            {
                "link": "http://www.ic.gc.ca/opic-cipo/cpd/eng/patent/2896381/summary.html",
                "number": "2896381",
                "title": "INTELLIGENT POSITIONING SYSTEM AND METHODS THEREFORE"
            }
        ]
    }

Info
----

This endpoint returns patent-specific information from the CIPO patent database. The response includes the boolean ``found``, and bibliographic data, abstract, claims, and representative drawing. 

For patents with abstracts in English and French, both versions are returned as a list.
The Canadian Patent Classification, ``cpc``, is returned only for older patents.

Processing of data gathered from CIPO is kept to a minimum and mostly returned as is, therefore common issues like extra whitespace and unrecognizable non-ASCII characters are to be expected.

Endpoint
    GET https://api.patentology.org/v1/info

Query Parameters
^^^^^^^^^^^^^^^^
=========== ================
Parameter	Description
=========== ================
id          Patent number.
=========== ================

Example Request::

    import requests
    
    payload = {'id': '2894056'}
    r = requests.get('https://api.patentology.org/v1/info', params=payload)

Exampe Response:

.. code-block:: json

    {
        "application": "CA 2894056",
        "titles": {
            "fr": "APPAREIL ELECTRONIQUE PORTABLE, PROCEDE ET INTERFACE UTILISATEUR GRAPHIQUE ...",
            "en": "PORTABLE ELECTRONIC DEVICE, METHOD AND GRAPHICAL USER ITNERFACE FOR DISPLAYING ..."
        },
        "bibliographic-data": {
            "ipc": [
                "G06F 3/0488 (2013.01)",
                "G06F 3/0481 (2013.01)",
                "G06F 3/0484 (2013.01)"
            ],
            "owners": [
                "APPLE INC. (United States of America)"
            ],
            "filing-date": "2007-09-05",
            "language": "English",
            "pub-date": "2008-03-13",
            "issued": "",
            "agent": "RICHES, MCKENZIE & HERBERT LLP",
            "licence": "N/A",
            "inventors": [
                "ORDING, BAS (United States of America)",
                "FORSTALL, SCOTT (United States of America)",
                "CHRISTIE, GREG (United States of America)",
                "LEMAY, STEPHEN O. (United States of America)",
                "CHAUDHRI, IMRAN (United States of America)",
                "WILLIAMSON, RICHARD (United States of America)",
                "BLUMENBERG, CHRIS (United States of America)",
                "VAN OS, MARCEL (United States of America)"
            ],
            "applicants": [
                "APPLE INC. (United States of America)"
            ]
        },
        "claims": "Note: Claims are shown in the official language in which they were submitted. The embodiments ...",
        "found": "True",
        "abstracts": [
            "A computer-implemented method, for use in conjunction with a portable electronic device ..."
        ],
        "drawing": "http://www.ic.gc.ca/opic-cipo/cpd/page/2894056_20150028_page1_scale25_rotate0_objectnameA1001001A17B25A11931J94872.gif"
    }