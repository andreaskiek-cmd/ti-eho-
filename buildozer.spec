[app]

title = ΤΙ ΕΧΩ
package.name = tieho
package.domain = org.tieho

source.dir = .
source.include_exts = py,db,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.archs = arm64-v8a

android.api = 35
android.minapi = 23

android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
