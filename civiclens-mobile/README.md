# CivicLens Mobile

React Native Expo app that wraps the CivicLens web frontend in a native mobile shell.

## Features

- Fullscreen WebView pointing to the live Vercel site
- Safe area handling (notch, status bar)
- Loading screen with CivicLens branding
- Error screen with retry button
- Android back button navigation
- Native PDF report downloads via share sheet

## How to Run

```bash
cd civiclens-mobile
npm install
npx expo start
# Scan QR code with Expo Go app on your phone
# Phone and PC must be on the same Wi-Fi
```

## Build APK

```bash
npm install -g eas-cli
eas login
eas build -p android --profile preview
# Download the .apk from the link Expo gives you
```

No need to rebuild for web/backend changes — the app loads from Vercel so updates show up automatically. Only rebuild if you change the mobile wrapper code itself.

## Project Structure

```
civiclens-mobile/
├── app/
│   ├── _layout.tsx    Root layout
│   └── index.tsx      WebView + loading/error UI + PDF handling
├── app.json           App config
├── eas.json           Build profiles
└── package.json
```

