# Google-Play-SSL-Pinning-Bypass

## Bypass Cronet Google Play SSL pinning on Android with Frida.

This repository includes multiple scripts, particularly ***gms_ssl_pinning.js*** and ***gps_ssl_pinning.js***.

Both scripts are linked to and used for Android HTTP(S) communication, sometimes relying on Cronet


We can *very roughly* summarize the use of these services as follows:



### gps (Google Play Services) → com.android.vending
Used for Google Play (e.g., Play Store browsing) services traffic generation and other Play Integrity communication, including:

- [PI] Attestation Request (DroidGuard result ↔ Google backend)


### gms (Google Mobile Services) → com.google.android.gms
Used for VM/bytecode requests for both SafetyNet and Play Integrity, and involved in basic SafetyNet communication:

- [PI] VM & Bytecode Request

- [SN] VM & Bytecode Request

- [SN] Attestation Request (DroidGuard result <-> Google backend)

You will also find a mitm script to capture safetynet/play integrity traffic.
This will help in reversing the DroidGuard VM and what not keep it up to date.


TODO: Finish Reversing DroidGuard
TODO:  Add a Python <-> Java bridge to avoid recompiling the app everytime and trace custom bytecode 








> *The deeper we explore Google's services, the more fascinating the journey gets 😊*
