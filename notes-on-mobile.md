
# Android
## Retrieve APK
### Download the APK from the smartphone
### Verify if device is connected
```adb devices```

### View list of installed packages
```adb shell pm list packages```

### Get path of apk
```adb shell pm path com.example.example```

### Get apk 
```adb pull /data/app/com.example.example.path.ecc.ecc```

### Website with APKs
Might be available here:
https://apkpure.com
https://apkmonk.com
https://apkfollow.com

External refs:
https://manifestsecurity.com/android-application-security/

### Using Frida on Android without root
https://koz.io/using-frida-on-android-without-root/
