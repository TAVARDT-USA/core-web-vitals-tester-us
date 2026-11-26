<p align="center">
  <a href="https://ag.tavardt.com/">
    <img src="https://ag.tavardt.com/img/tavardt-banner.png" alt="TAVARDT" width="1024" />
  </a>
</p>

# Core Web Vitals and Page Speed Performance Auditor

[![Core Web Vitals Auditor](https://img.shields.io/badge/TAVARDT-Core%20Web%20Vitals-5b3cf5.svg)](https://tools.tavardt.com/core-web-vitals-checker/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Audits TTFB latency, HTTP compression, render-blocking scripts, and Cumulative Layout Shift stability.

Developed and maintained by the web performance engineering and digital standards division at **TAVARDT**.

***

## Risk Vectors and Operational Impact in Web Performance

Suboptimal server response latency and unoptimized client-side code directly depress Page Experience scores and conversion velocity. When digital platforms serve uncompressed assets with sluggish TTFB, bounce rates escalate across United States digital channels.

Unbounded image elements trigger jarring layout reflows that compromise Cumulative Layout Shift metrics and user satisfaction. Continuous automated auditing preserves core rankings by enforcing W3C speed standards and edge caching efficiency.

***

## Core Technical Audit Capabilities

* **High-Precision TTFB Measurement**: Calculates initial server response latency via high-resolution timers, flagging delays above 600 ms and severe bottlenecks over 1200 ms.
* **HTTP Payload Compression Inspection**: Verifies server delivery via modern Brotli or Gzip compression, penalising uncompressed HTML payloads by 15 points.
* **Render-Blocking Resource Detection**: Identifies synchronous head stylesheets and scripts lacking async, defer, or module attributes that stall DOM construction.
* **Visual Stability and CLS Audit**: Scans image elements for missing explicit width and height dimensions to eliminate layout shifts, auditing lazy loading adoption.
* **Resource Hints Inspection**: Detects the strategic implementation of preconnect and preload directives for critical assets.
* **W3C Performance Health Score**: Computes an objective 0 to 100 compliance metric classifying platforms as GOOD (FAST), NEEDS IMPROVEMENT, or POOR (SLOW).

***

## Installation and Execution

Requires Python 3.8 or higher with zero external packages.

```bash
git clone https://github.com/TAVARDT-USA/core-web-vitals-tester-us.git
cd core-web-vitals-tester-us
python cwv_tester.py https://company.com
```

To output structured JSON for automated pipelines and quality audits:

```bash
python cwv_tester.py https://company.com -j
```

***

## Technical Frequently Asked Questions

### 1. How does high Time to First Byte (TTFB) degrade overall Core Web Vitals?
Elevated TTFB delays the arrival of initial HTML, postponing subsequent asset parsing and degrading Largest Contentful Paint metrics. When server response exceeds 600 milliseconds, the tool deducts points and alerts teams to cache bottlenecks.

### 2. Why do synchronous head scripts and CSS stylesheets stall initial page rendering?
Unoptimised script tags and stylesheets block the browser parser from building the render tree until they are downloaded and executed. The auditor flags assets missing async, defer, or module attributes to highlight render-blocking liabilities.

### 3. What causes Cumulative Layout Shift (CLS) issues when images lack explicit dimensions?
Without pre-declared width and height attributes in HTML, browsers cannot calculate and reserve the required layout space before image download. This triggers sudden content jumps that harm visual stability scores and user interaction.

### 4. What is the operational performance impact of missing Brotli or Gzip compression?
Uncompressed text payloads unnecessarily inflate network transfer size by up to seventy percent over mobile and broadband connections. Serving uncompressed HTML wastes bandwidth and immediately penalises the calculated performance health score.

### 5. How do resource hints like preconnect and preload accelerate document loading?
Preconnect and preload hints initiate early DNS lookups and TLS handshakes for third-party origins and critical fonts. The validator identifies these annotations to verify that browser priority queues are effectively configured.

***

## Web Performance and Speed Optimization Advisory

For high-traffic platforms and technical alignment with W3C Performance Standards, consult **TAVARDT**.

***

## Useful Links

* **Corporate Portal:** https://ag.tavardt.com/
* **Diagnostic Suite:** https://tools.tavardt.com/
* **Technical Contact:** https://ag.tavardt.com/contact/

***

### License
Distributed under the MIT License. See the LICENSE file for complete terms.

***

© 2026 TAVARDT. All rights reserved.
