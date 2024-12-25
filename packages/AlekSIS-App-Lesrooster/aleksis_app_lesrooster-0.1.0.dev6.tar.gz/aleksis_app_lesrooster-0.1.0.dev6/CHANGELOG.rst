Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`0.1.0.dev6`_ - 2024-12-24
--------------------------

Added
~~~~~

* Lesson bundles for simple planning of connected courses (e. g. for language tracks).

`0.1.0.dev5`_ - 2024-10-17
--------------------------

Upgrade notice
~~~~~~~~~~~~~~

This app's functionality was mainly covered by AlekSIS-App-Chronos
in the past. Lesrooster contains a migration path for migrating
3.x versions of AlekSIS-App-Chronos and AlekSIS-App-Alsijil.
If you want to migrate from these versions, please be sure that the
apps are installed. Then run migrations as usual. Please be aware
that depending on the amount of data the migration might take a while.
On really large installations, several hours are to be expected.
In case you run into memory issues, please contact us for support.

Added
~~~~~

* Management of validity ranges and lesson rasters (slots and breaks).
* Planning of courses per validity range/school term using interactive
  planning tool.
* Creation of timetables using digital magnetic board with assistance
  functions.


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html


.. _0.1.0.dev5: https://edugit.org/AlekSIS/onboarding/AlekSIS-App-Lesrooster/-/tags/0.1.0.dev5
.. _0.1.0.dev6: https://edugit.org/AlekSIS/onboarding/AlekSIS-App-Lesrooster/-/tags/0.1.0.dev6
