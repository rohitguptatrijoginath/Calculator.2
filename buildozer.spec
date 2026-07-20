[app]
title = Advanced Calculator X
package.name = advancedcalculatorx
package.domain = com.offlineapps
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0

# ✅ Stability Requirements
requirements = python3,kivy==2.3.0,hostpython3,pillow

orientation = portrait
fullscreen = 0

# ✅ Modern Android Settings
android.api = 33
android.minapi = 21
android.ndk = 25c
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ✅ GitHub fixes
android.accept_sdk_license = True
android.skip_update = False
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
