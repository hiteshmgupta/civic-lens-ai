import { useRef, useState, useCallback } from 'react';
import {
  StyleSheet,
  View,
  ActivityIndicator,
  Text,
  TouchableOpacity,
  BackHandler,
  Platform,
  Alert,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { WebView, WebViewNavigation } from 'react-native-webview';
import { useEffect } from 'react';

const WEBAPP_URL = 'https://civic-lens-ai-bay.vercel.app';

// Injected JS: intercept blob URL creation for downloads and open in external browser instead
const INJECTED_JS = `
(function() {
  // Override the click-to-download pattern used for blob URLs
  var origCreateObjectURL = URL.createObjectURL;
  URL.createObjectURL = function(blob) {
    var url = origCreateObjectURL.call(URL, blob);
    // Store blob URLs so we can identify them
    window.__blobUrls = window.__blobUrls || [];
    window.__blobUrls.push(url);
    return url;
  };

  // Intercept link clicks that target blob URLs
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a');
    if (link && link.href && link.href.startsWith('blob:')) {
      e.preventDefault();
      e.stopPropagation();
      window.ReactNativeWebView.postMessage(JSON.stringify({
        type: 'blob_download',
        message: 'PDF downloads are not supported in the mobile app. Please use the website to download reports.'
      }));
    }
  }, true);
})();
true;
`;

export default function Index() {
  const webViewRef = useRef<WebView>(null);
  const [canGoBack, setCanGoBack] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  // Handle Android hardware back button
  useEffect(() => {
    if (Platform.OS !== 'android') return;

    const onBackPress = () => {
      if (canGoBack && webViewRef.current) {
        webViewRef.current.goBack();
        return true; // prevent default (exit app)
      }
      return false; // allow default (exit app)
    };

    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      onBackPress
    );
    return () => subscription.remove();
  }, [canGoBack]);

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorEmoji}>📡</Text>
          <Text style={styles.errorTitle}>Connection Error</Text>
          <Text style={styles.errorMessage}>
            Could not connect to CivicLens.{'\n'}Please check your internet
            connection.
          </Text>
          <TouchableOpacity
            style={styles.retryButton}
            onPress={() => {
              setError(false);
              setLoading(true);
            }}
            activeOpacity={0.8}
          >
            <Text style={styles.retryText}>Try Again</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      {loading && (
        <View style={styles.loadingOverlay}>
          <View style={styles.loadingCard}>
            <View style={styles.logoContainer}>
              <Text style={styles.logoText}>CL</Text>
            </View>
            <Text style={styles.loadingTitle}>CivicLens</Text>
            <ActivityIndicator size="small" color="#c8ee44" style={{ marginTop: 16 }} />
            <Text style={styles.loadingSubtitle}>Loading platform...</Text>
          </View>
        </View>
      )}
      <WebView
        ref={webViewRef}
        source={{ uri: WEBAPP_URL }}
        style={styles.webview}
        onLoadEnd={() => setLoading(false)}
        onError={() => {
          setLoading(false);
          setError(true);
        }}
        onHttpError={(syntheticEvent) => {
          const { nativeEvent } = syntheticEvent;
          if (nativeEvent.statusCode >= 500) {
            setError(true);
          }
        }}
        onNavigationStateChange={(navState) => {
          setCanGoBack(navState.canGoBack);
        }}
        // Block blob: URL navigation (WebView can't handle these)
        onShouldStartLoadWithRequest={(request) => {
          if (request.url.startsWith('blob:')) {
            return false; // silently block
          }
          // Allow all other URLs
          return true;
        }}
        // Inject JS to intercept blob download links
        injectedJavaScript={INJECTED_JS}
        // Handle messages from injected JS
        onMessage={(event) => {
          try {
            const data = JSON.parse(event.nativeEvent.data);
            if (data.type === 'blob_download') {
              Alert.alert(
                'Download Not Available',
                'PDF report downloads are not available in the mobile app. Please visit the website in a browser to download reports.',
                [
                  { text: 'OK' },
                  {
                    text: 'Open in Browser',
                    onPress: () => Linking.openURL(WEBAPP_URL),
                  },
                ]
              );
            }
          } catch (e) {
            // ignore non-JSON messages
          }
        }}
        // Performance & UX settings
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={false}
        allowsBackForwardNavigationGestures={true}
        allowsInlineMediaPlayback={true}
        mediaPlaybackRequiresUserAction={false}
        sharedCookiesEnabled={true}
        thirdPartyCookiesEnabled={true}
        cacheEnabled={true}
        // Prevent opening external browser
        setSupportMultipleWindows={false}
        // Android-specific
        overScrollMode="never"
        textZoom={100}
        // Pull to refresh
        pullToRefreshEnabled={true}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0f1a',
  },
  webview: {
    flex: 1,
    backgroundColor: '#0a0f1a',
  },
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    zIndex: 10,
    backgroundColor: '#0a0f1a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingCard: {
    alignItems: 'center',
  },
  logoContainer: {
    width: 56,
    height: 56,
    borderRadius: 16,
    backgroundColor: '#c8ee44',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  logoText: {
    color: '#0a0f1a',
    fontSize: 20,
    fontWeight: '800',
  },
  loadingTitle: {
    color: '#f1f5f9',
    fontSize: 22,
    fontWeight: '700',
  },
  loadingSubtitle: {
    color: '#64748b',
    fontSize: 13,
    marginTop: 8,
  },
  errorContainer: {
    flex: 1,
    backgroundColor: '#0a0f1a',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 32,
  },
  errorEmoji: {
    fontSize: 48,
    marginBottom: 16,
  },
  errorTitle: {
    color: '#f1f5f9',
    fontSize: 22,
    fontWeight: '700',
    marginBottom: 8,
  },
  errorMessage: {
    color: '#94a3b8',
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 24,
  },
  retryButton: {
    backgroundColor: '#c8ee44',
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 14,
  },
  retryText: {
    color: '#0a0f1a',
    fontSize: 15,
    fontWeight: '700',
  },
});
