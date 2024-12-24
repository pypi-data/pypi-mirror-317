"""
core application classes and widgets for GUIApp-conform Kivy apps
=================================================================

this ae portion is implementing the Kivy-framework-specific parts for apps with multilingual context-sensitive help,
user onboarding, tours, walkthroughs and tutorials.

by extending and joining the app classes :class:`~ae.gui_app.MainAppBase`, :class:`~ae.gui_help.HelpAppBase` and
:class:`~kivy.app.App`, it is providing additional :ref:`config-variables`, some useful constants, behaviors and
widgets for your multi-platform apps.

this portion is composed of the following modules:

    * :mod:`~ae.kivy.i18n`: internationalization (i18n) function :func:`~ae.kivy.i18n.get_txt` for python and kv code
    * :mod:`~ae.kivy.behaviors`: widget behavior classes
    * :mod:`~ae.kivy.widgets`: generic widget classes and some useful constants
    * :mod:`~ae.kivy.tours`: app tour widget classes
    * :mod:`~ae.kivy.apps`: providing the two application classes (:class:`~ae.kivy.apps.FrameworkApp` and
      :class:`~ae.kivy.apps.KivyMainApp`)


unit tests
----------

unit tests are currently still incomplete and need at least V 2.0 of OpenGL and the
`Kivy framework <https://kivy.org>`__ installed.

.. note::
    unit tests are currently not passing at the gitlab CI because is failing to set up
    a properly running OpenGL graphics/window system on the python image that all ae portions are using.

"""


__version__ = '0.3.114'
