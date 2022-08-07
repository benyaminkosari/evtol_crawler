

EVTOL Crawler
===============
This is a crawler for gathering data from https://evtol.news/aircraft. The data then can be either
analyzed by filtering or just simply saved as csv.

Installing
============

.. code-block:: bash

    pip install evtol-crawler

Usage
============

Download all vtols:

.. code-block:: bash

    >>> from evtol.download import Download
    >>> download = Download()
    >>> download.all()

Save downloaded vtols as csv:

.. code-block:: bash

    >>> from evtol.save_to_csv import SaveToCsv
    >>> handler = SaveToCsv()
    >>> handler.save('myvtols', handler.limited_by_params)
