# Google-Play-SSL-Pinning-Bypass

## Bypass Cronet Google Play SSL pinning on Android with Frida.

This repository includes multiple scripts, particularly ***gms_ssl_pinning.js*** and ***gps_ssl_pinning.js***.

Both scripts are linked to and used for Android HTTP(S) communication, sometimes relying on Cronet. The deeper we dive into Google's services, the more exciting the journey becomes 😊. We can very roughly summarize the use of these services as follows:



### gps (Google Play Services) → com.android.vending
Used for Google Play (e.g., Play Store browsing) services traffic generation and other Play Integrity communication, including:

[PI] Attestation Request (DroidGuard result ↔ Google backend)


### gms (Google Mobile Services)gms → com.google.android.gms
Used for VM/bytecode requests for both SafetyNet and Play Integrity, and involved in basic SafetyNet communication:

[SN] VM & Bytecode Request
[SN] Attestation Request (DroidGuard result ↔ Google backend)
[SN] VM & Bytecode Request
