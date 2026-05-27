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

android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b

android.permissions = INTERNET

android.allow_backup = True

android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2

warn_on_root = 1