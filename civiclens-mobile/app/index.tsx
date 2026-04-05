import { useRef, useState } from 'react';
import {
  StyleSheet,
  View,
  ActivityIndicator,
  Text,
  TouchableOpacity,
  BackHandler,
  Platform,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { WebView } from 'react-native-webview';
import { useEffect } from 'react';
import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';

const WEBAPP_URL = 'https://civic-lens-ai-bay.vercel.app';
const API_BASE = 'https://civiclens-backend-j5q2.onrender.com';

// Injected JS: Override the handleExportPdf function so it sends a message
// to React Native instead of trying to create a blob download link
const INJECTED_JS = `
(function() {
  // Intercept dynamically created <a> elements with download attribute
  // The frontend creates: <a href="blob:..." download="amendment-X-report.pdf">
  var origClick = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function() {
    if (this.hasAttribute('download') && this.href && this.href.startsWith('blob:')) {
      // Extract amendment ID from the download filename
      var downloadAttr = this.getAttribute('download') || '';
      var match = downloadAttr.match(/amendment-(\\d+)/);
      var amendmentId = match ? match[1] : null;
      var token = localStorage.getItem('token') || '';
      
      if (amendmentId) {
        window.ReactNativeWebView.postMessage(JSON.stringify({
          type: 'pdf_download',
          amendmentId: amendmentId,
          token: token
        }));
        return; // Don't actually click the blob link
      }
    }
    return origClick.apply(this, arguments);
  };
})();
true;
`;

export default function Index() {
  const webViewRef = useRef<WebView>(null);
  const [canGoBack, setCanGoBack] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [downloading, setDownloading] = useState(false);

  // Handle Android hardware back button
  useEffect(() => {
    if (Platform.OS !== 'android') return;

    const onBackPress = () => {
      if (canGoBack && webViewRef.current) {
        webViewRef.current.goBack();
        return true;
      }
      return false;
    };

    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      onBackPress
    );
    return () => subscription.remove();
  }, [canGoBack]);

  // Native PDF download handler
  const handlePdfDownload = async (amendmentId: string, token: string) => {
    if (downloading) return;
    setDownloading(true);

    try {
      const url = `${API_BASE}/api/amendments/${amendmentId}/report/pdf`;
      const filename = `civiclens-amendment-${amendmentId}-report.pdf`;
      const fileUri = `${FileSystem.cacheDirectory}${filename}`;

      const downloadResult = await FileSystem.downloadAsync(url, fileUri, {
        headers: {
          Authorization: token ? `Bearer ${token}` : '',
          Accept: 'application/pdf',
        },
      });

      if (downloadResult.status === 200) {
        const canShare = await Sharing.isAvailableAsync();
        if (canShare) {
          await Sharing.shareAsync(downloadResult.uri, {
            mimeType: 'application/pdf',
            dialogTitle: 'Save CivicLens Report',
            UTI: 'com.adobe.pdf',
          });
        } else {
          Alert.alert('Downloaded', 'Report saved successfully.');
        }
      } else {
        Alert.alert('Download Failed', 'Could not download the report.');
      }
    } catch (err) {
      console.error('PDF download error:', err);
      Alert.alert('Download Error', 'Something went wrong. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  // Handle messages from the WebView
  const handleMessage = (event: any) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'pdf_download' && data.amendmentId) {
        handlePdfDownload(data.amendmentId, data.token);
      }
    } catch (e) {
      // ignore non-JSON messages
    }
  };

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

      {downloading && (
        <View style={styles.downloadBanner}>
          <ActivityIndicator size="small" color="#0a0f1a" />
          <Text style={styles.downloadText}>Downloading report...</Text>
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
        onShouldStartLoadWithRequest={(request) => {
          if (request.url.startsWith('blob:')) {
            return false;
          }
          return true;
        }}
        injectedJavaScript={INJECTED_JS}
        onMessage={handleMessage}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={false}
        allowsBackForwardNavigationGestures={true}
        allowsInlineMediaPlayback={true}
        mediaPlaybackRequiresUserAction={false}
        sharedCookiesEnabled={true}
        thirdPartyCookiesEnabled={true}
        cacheEnabled={true}
        setSupportMultipleWindows={false}
        overScrollMode="never"
        textZoom={100}
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
  downloadBanner: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 20,
    backgroundColor: '#c8ee44',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 8,
  },
  downloadText: {
    color: '#0a0f1a',
    fontSize: 13,
    fontWeight: '600',
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
