[app]

# (str) Title of your application
title = Dental Detection

# (str) Package name
package.name = dentaldetection

# (str) Package domain (needed for android/ios packaging)
package.domain = org.dental

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,tflite

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.10.6,kivy==2.2.0,opencv-python,numpy,tensorflow-lite-support

# (list) Permissions
# (See https://python-for-android.readthedocs.io/en/latest/buildoptions/#build-options-1 for all the supported syntaxes and properties)
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (list) features (adds uses-feature -tags to manifest)
android.features = android.hardware.camera,android.hardware.camera.autofocus

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = False

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
android.extra_manifest_xml = %(source.dir)s/android_manifest.xml

# (str) Extra xml to write directly inside the <manifest><application> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
android.extra_manifest_application_xml = %(source.dir)s/android_manifest_application.xml

# (list) Pattern to whitelist for the whole project
android.whitelist =

# (str) Path to a custom whitelist file
android.whitelist_src =

# (str) Path to a custom blacklist file
android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
android.add_jars =

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src =

# (list) Android AAR archives to add
android.add_aars =

# (list) Gradle dependencies to add
android.gradle_dependencies =

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
android.add_compile_options =

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes
android.gradle_repositories =

# (str) python-for-android branch to use, defaults to master
p4a.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
android.manifest.intent_filters =

# (str) launchMode to set for the main activity
android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/armeabi-v7a
android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/arm64-v8a
android.add_libs_arm64_v8a =

# (list) Android additional libraries to copy into libs/x86
android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/x86_64
android.add_libs_x86_64 =

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
android.logcat_pid_only = False

# (str) Android additional adb arguments
android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
