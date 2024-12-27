* pdfimpose-web 1.1.0 (2024-12-27)

    * Add Python3.13 support.

    -- Louis Paternault <spalax@gresille.org>

* pdfimpose-web 1.0.1 (2024-06-24)

    * Bug fixes

        * pdfautonup option 'repeat=auto' did not work (closes #1).
        * App would fail and go back to main page without any explaination about the error (closes #2).
        * App would not run if database was not initialized, or if no configuration was present.
        * App would crash instead of reporting an error if the source file was to big.
        * Repeat limit was ignored (on server side).

    -- Louis Paternault <spalax@gresille.org>

* pdfimpose-web 1.0.0 (2024-03-05)

    * First published version.

    -- Louis Paternault <spalax@gresille.org>
