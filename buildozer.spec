[app]

title = Space Shooter
package.name = spaceshooter
package.domain = org.yourname

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

# Εικονίδιο εφαρμογής (αν έχεις)
# icon.filename = icon.png

# Splash Screen (αν έχεις)
# presplash.filename = presplash.png

android.api = 35
android.minapi = 23
android.sdk = 35
android.ndk = 25b
android.accept_sdk_license = True

android.permissions = INTERNET

android.allow_backup = True

android.archs = arm64-v8a

[buildozer]

log_level = 2

warn_on_root = 1
