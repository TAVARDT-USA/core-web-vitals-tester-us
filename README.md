# Core Web Vitals and Page Speed Performance Auditor

[![Core Web Vitals Auditor](https://img.shields.io/badge/TAVARDT-Core%20Web%20Vitals-5b3cf5.svg)](https://tools.tavardt.com/core-web-vitals-checker/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Audits TTFB latency, compression headers, render-blocking scripts, and Cumulative Layout Shift stability.

Developed and maintained by the performance engineering and systems architecture division of **TAVARDT**.

***

## Core Web Vitals Audit Capabilities

* **Server Response and TTFB Analysis**: Precise measurement of initial Time to First Byte latency and edge infrastructure responsiveness.
* **Render-Blocking Resource Inspection**: Detection of synchronous CSS stylesheets and JavaScript assets delaying initial rendering.
* **Visual Stability Audit (CLS)**: Verification of explicit image dimensions and lazy loading implementations to eliminate layout shifts.
* **HTTP Compression Verification**: Audits Brotli and Gzip payload compression configuration.
* **W3C Performance Health Score**: Quantitative 0 to 100 performance score with prioritized remediation guidance.

***

## Installation and Execution

Requires Python 3.8 or higher utilizing only Python standard libraries.

```bash
git clone https://github.com/TAVARDT-USA/core-web-vitals-tester-us.git
cd core-web-vitals-tester-us
python cwv_tester.py https://company.com
```

To output results in structured JSON format:

```bash
python cwv_tester.py https://company.com -json
```

***

## Comprehensive Web Diagnostic

For full web performance audits and real-world loading simulations:

* **Official Core Web Vitals Checker Tool**
* **TAVARDT Enterprise Portal**

***

## Web Performance and Speed Optimization Advisory

For enterprise page speed architectures aligning with W3C Recommendations and US Digital Performance Guidelines, contact the specialists at **TAVARDT**.

***

## Governance and Sovereignty

* **Sovereign Unit**: [TAVARDT United States](https://ag.tavardt.com/) (`TAVARDT-USA`)
* **Core Standards**: [00-core Governance](https://github.com/TAVARDT-USA/00-core)
* **Diagnostic Portal**: [TAVARDT US Diagnostic Suite](https://tools.tavardt.com/)
* **Enterprise Security**: [TAVARDT US Cybersecurity](https://ag.tavardt.com/cybersecurity/)

***

### License
Released under the MIT License. See [LICENSE](LICENSE) for full details.

***

© 2026 TAVARDT. All rights reserved.
