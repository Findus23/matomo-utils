from enum import Enum


# from PRIORITY_CHOICES in weblate/weblate/trans/util.py
class Priority(Enum):
    very_high = 60
    high = 80
    medium = 100
    low = 120
    very_low = 140


priorities = {
    "matomo-base": Priority.very_high,
    "plugin-actions": Priority.high,
    "plugin-annotations": Priority.high,
    "plugin-api": Priority.high,
    "plugin-coreadminhome": Priority.very_high,
    "plugin-corehome": Priority.very_high,
    "plugin-corepluginsadmin": Priority.high,
    "plugin-coreupdater": Priority.high,
    "plugin-dashboard": Priority.very_high,
    "plugin-deviceplugins": Priority.high,
    "plugin-devicesdetection": Priority.high,
    "plugin-eccommerce": Priority.high,
    "plugin-events": Priority.high,
    "plugin-feedback": Priority.high,
    "plugin-goals": Priority.high,
    "plugin-imagegraph": Priority.high,
    "plugin-insights": Priority.high,
    "plugin-installation": Priority.very_high,
    "plugin-languagesmanager": Priority.high,
    "plugin-live": Priority.high,
    "plugin-login": Priority.high,
    "plugin-marketplace": Priority.high,
    "plugin-overlay": Priority.high,
    "plugin-privacymanager": Priority.high,
    "plugin-provider": Priority.high,
    "plugin-referrers": Priority.high,
    "plugin-resolution": Priority.high,
    "plugin-scheduledreports": Priority.high,
    "plugin-segmenteditor": Priority.high,
    "plugin-seo": Priority.high,
    "plugin-sitesmanager": Priority.high,
    "plugin-transitions": Priority.high,
    "plugin-twofactorauth": Priority.high,
    "plugin-usercountry": Priority.high,
    "plugin-usercountrymap": Priority.high,
    "plugin-userid": Priority.high,
    "plugin-userlanguage": Priority.high,
    "plugin-usersmanager": Priority.high,
    "plugin-visitfrequency": Priority.high,
    "plugin-visitorinterest": Priority.high,
    "plugin-visitssummary": Priority.high,
    "plugin-visittime": Priority.high,
    "plugin-websitemeasurable": Priority.high,
    "plugin-widgetize": Priority.high,
    "plugin-securityinfo": Priority.low,
    "ommunityplugin-diagnosticsextended": Priority.low,

}
