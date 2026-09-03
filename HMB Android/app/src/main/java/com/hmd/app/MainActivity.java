package com.hmbnuts.app;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // PORTRAIT ONLY
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        // JavaScript
        settings.setJavaScriptEnabled(true);

        // Streamlit storage
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        // Web pages
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        /*
         * IMPORTANT:
         * Do NOT use:
         *
         * setUseWideViewPort(true)
         * setLoadWithOverviewMode(true)
         *
         * because they can make the Streamlit page behave like
         * a desktop-width page on a portrait phone.
         */

        settings.setUseWideViewPort(false);
        settings.setLoadWithOverviewMode(false);

        // Disable user zoom
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        // Normal WebView rendering
        settings.setDefaultTextEncodingName("UTF-8");
        settings.setTextZoom(100);

        webView.setInitialScale(100);

        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());

        // HMB Nuts and Seeds
        webView.loadUrl(
                "https://baluaiproject1.streamlit.app/"
        );
    }

    @Override
    public void onBackPressed() {

        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {

        if (webView != null) {
            webView.stopLoading();
            webView.destroy();
        }

        super.onDestroy();
    }
}
