# CivicLens Mobile

React Native Expo app that wraps the [CivicLens web platform](https://civic-lens-ai-bay.vercel.app) in a native mobile experience.

## What It Does

- Fullscreen WebView pointing to the CivicLens Vercel frontend
- SafeAreaView prevents overlap with device notch / status bar
- Branded loading screen with CivicLens logo
- Error screen with retry on network failure
- Android hardware back button navigates within the app
- Pull-to-refresh support
- Cookies & localStorage preserved for auth persistence
- **Native PDF report downloads** — downloads reports directly on your phone via the share sheet

## Prerequisites

| Tool | Version | Download Link | How to Verify |
|---|---|---|---|
| **Node.js** | 18+ (LTS) | [nodejs.org](https://nodejs.org/) | `node --version` |
| **npm** | 9+ | Comes with Node.js | `npm --version` |

## Versions Used

| Package | Version |
|---|---|
| Expo SDK | 54.0.33 |
| React Native | 0.81.5 |
| React | 19.1.0 |
| react-native-webview | 13.15.0 |
| react-native-safe-area-context | 5.6.0 |
| expo-file-system | 19.0.21 |
| expo-sharing | 14.0.8 |
| Expo Router | 6.0.23 |
| expo-status-bar | 3.0.9 |
| TypeScript | 5.9.2 |

## Development Setup

```bash
# 1. Install dependencies
npm install

# 2. Start Expo dev server
npx expo start
```

Then scan the QR code with **Expo Go** app:
- **Android:** Download [Expo Go from Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent), open and scan QR
- **iOS:** Download [Expo Go from App Store](https://apps.apple.com/app/expo-go/id982107779), scan QR with Camera app

> Your phone and PC must be on the **same Wi-Fi network**.

## Build Standalone APK (Runs Without PC)

This builds the app on Expo's cloud servers — **no Android Studio or local tools needed**.

```bash
# 1. Install EAS CLI globally (one-time)
npm install -g eas-cli

# 2. Login to Expo (create a free account at https://expo.dev if you don't have one)
eas login

# 3. Build APK (~10-15 minutes, runs on Expo's cloud)
eas build -p android --profile preview

# 4. When done, you get a download link for the .apk file
# Download it and install on your Android phone
# (Enable "Install from unknown sources" in Android settings if prompted)
```

> **Do I need to rebuild after every code change?**
> - **Web frontend changes (CSS, React, etc.):** ❌ No rebuild needed. The app loads the Vercel URL — changes deploy automatically.
> - **Backend/AI changes:** ❌ No rebuild needed. Hosted on Render.
> - **Mobile app code (`civiclens-mobile/`):** ✅ Yes, only if you change the native wrapper code.

### Build for iOS

```bash
eas build -p ios --profile preview
```

Requires an Apple Developer account ($99/year). Install the resulting `.ipa` via TestFlight.

### Build for Play Store

```bash
eas build -p android --profile production
```

Generates an `.aab` (Android App Bundle) optimized for Google Play Store submission.

## Project Structure

```
civiclens-mobile/
├── app/
│   ├── _layout.tsx    # Root layout — no header, dark status bar
│   └── index.tsx      # WebView + SafeAreaView + PDF download + loading/error UI
├── app.json           # App config (name, splash, icons, package IDs)
├── eas.json           # EAS Build profiles (development, preview/APK, production/AAB)
├── package.json       # Dependencies and scripts
└── tsconfig.json      # TypeScript configuration
```

## EAS Build Profiles (`eas.json`)

| Profile | Output | Use Case |
|---|---|---|
| `development` | Dev client | Development with custom native code |
| `preview` | `.apk` | Sideloading / testing on real devices |
| `production` | `.aab` | Google Play Store submission |
