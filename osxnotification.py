import Foundation
import objc
import AppKit
import sys

NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
NSUserNotification = objc.lookUpClass('NSUserNotification')

def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    notification.setHasActionButton_(True)
    notification.setActionButtonTitle_('Action!!')
    notification.setHasReplyButton_(True)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
