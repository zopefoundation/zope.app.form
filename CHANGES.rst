=======
CHANGES
=======

6.2 (unreleased)
================

- Update tests to run with ``multipart >= 1.1+``.


6.1 (2024-10-21)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7.

- Update tests to run with ``multipart >= 1``.


6.0 (2023-02-24)
================

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Add support for Python 3.8, 3.9, 3.10, 3.11.

- Adapt to changes in ``zope.configuration >= 4.4``.


5.1.0 (2018-10-22)
==================

- Add support for Python 3.7.


5.0.0 (2017-04-27)
==================

- Add support for PyPy, Python 3.4, 3.5 and 3.6.

4.0.2 (2010-01-22)
==================

- Seems like 4.0.1 was released already. Brown bag.

4.0.1 (2010-01-08)
==================

- Import 'escape' for backwards compatibility as packages turn out to be
  importing this too, even though it's actually from the Python standard
  library.

- Widget documentation is now on PyPI too.

4.0 (2010-01-08)
================

- The widget implementations have been moved to zope.formlib. This
  makes this package depend on zope.formlib. The dependency of zope.formlib
  on this package has been broken.

3.12.1 (2009-12-22)
===================

- Added missing zope.datetime dependency.

3.12.0 (2009-12-22)
===================

- Use zope.browserpage in favor of zope.app.pagetemplate.

3.11.1 (2009-12-22)
===================

- Prefer zope.testing.doctest over doctestunit and adjust test output to newer
  zope.schema release.

3.11.0 (2009-12-18)
===================

- Use zope.component.testing in favor of zope.app.testing where possible.

- Define dummy standard_macros for test purposes. This reduces the test
  dependencies by zope.app.basicskin and zope.browserresource.

- Removed the zope.app.container and zope.app.publisher testing dependencies.

- Refactored code to remove zope.app.component dependency.

- Made the tests independent of zope.app.locales.

- Reduce zope.app test dependencies by avoiding zope.app.securitypolicy and
  zope.app.zcmlfiles.

3.10.0 (2009-12-17)
===================

- Avoid the ``zope.app.basicskin`` dependency, by defining our own FormMacros.

3.9.0 (2009-10-08)
==================

- Internationalized 'Invalid value' used with ConversionError
- Added dependency on transaction and test dependency on zope.app.component.
- Moved dependencies on ZODB3 and zope.location to the test extra.
- Reduced the dependency on zope.app.publisher to a dependency on
  zope.browsermenu plus a test dependency on zope.browserpage.

3.8.1 (2009-07-23)
==================

- Fix unittest failure due to translation update.

3.8.0 (2009-05-24)
==================

- Use standard properties instead of `zope.cachedescriptors`.

- Require `zope.browser` 1.1 instead of `zope.app.container` for IAdding.

3.7.3 (2009-05-11)
==================

- Fixed invalid markup.

3.7.2 (2009-03-12)
==================

- Fixed bug where OrderedMultiSelectWidget did not respect the widgets
  size attribute.

- Fixed bug in SequenceWidget where it crashed while trying to iterate
  a missing_value (None in most of cases) on _getRenderedValue.

- Adapt to removal of deprecated interfaces from zope.component.interfaces.
  The IView was moved to zope.publisher and we use our custom IWidgetFactory
  interface instead of removed zope.component.interfaces.IViewFactory.

- Fix tests to work on Python 2.6.

3.7.1 (2009-01-31)
==================

- Adapt to the upcoming zope.schema release 3.5.1 which will also silence the
  spurious `set` failures.

3.7.0 (2008-12-11)
==================

- use zope.browser.interfaces.ITerms instead of zope.app.form.browser.interfaces

- Depending on zope.schema>=3.5a1 which uses the builtin ``set`` instead of the
  ``sets`` module.


3.6.4 (2008-11-26)
==================

- The URIDisplayWidget doesn't render an anchor for empty/None values.


3.6.3 (2008-10-15)
==================

- Get rid of deprecated usage of LayerField from
  zope.app.component.back35, replaced by
  zope.configuration.fields.GlobalInterface.

3.6.2 (2008-09-08)
==================


- Fixed restructured text in doc tests to unbreak the PyPI page.

(3.6.1 skipped due to a typo)


3.6.0 (2008-08-22)
==================

- Dropdown widgets display an item for the missing value even if the field is
  required when no value is selected. See zope/app/form/browser/README.txt on
  how to switch this off for BBB.

- Source select widgets for required fields are now required as well. They
  used not to be required on the assumption that some value would be selected
  by the browser, which had always been wrong except for dropdown widgets.


3.5.0 (2008-06-05)
==================

- Translate the title on SequenceWidget's "Add <title>" button.

- No longer uses zapi.


3.4.2 (2008-02-07)
==================

- Made display widgets for sources translate message IDs correctly.


3.4.1 (2007-10-31)
==================

- Resolve ``ZopeSecurityPolicy`` deprecation warning.


3.4.0 (2007-10-24)
==================

- ``zope.app.form`` now supports Python2.5

- Initial release independent of the main Zope tree.


Before 3.4
==========

This package was part of the Zope 3 distribution and did not have its own
CHANGES.txt. For earlier changes please refer to either our subversion log or
the CHANGES.txt of earlier Zope 3 releases.
