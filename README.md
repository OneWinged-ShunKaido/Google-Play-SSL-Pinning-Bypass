# Google-Play-SSL-Pinning-Bypass

Bypass Cronet Google Play SSL pinning on Android with Frida

This Repo includes multiple scripts, especially **gms**_ssl_pinning.js & **gps**_ssl_pinning.js

Both are linked & used for Android http(s) communication and sometimes relies on Cronet. The deeper we dive into Google's services, the more exciting the journey becomes 😊
Thus we can *very roughly* sum up the use of these services as follows:


**gps** -> **com.android.vending**
**gms** -> **com.google.android.gms**



gps is used for Google Play (e.g. Play Store browsing) services traffic generation and whatnot Play Integrity communication: 
[PI] Attestation Request (DroidGuard result <-> Google backend)

gms is used for VM/bytecode request for both SafetyNet and Play Integrity. Also involved in basic SN communication:

[SN] VM & ByteCode Request
[SN] Attestation Request (DroidGuard result <-> Google backend)
[PI] VM & ByteCode Request



