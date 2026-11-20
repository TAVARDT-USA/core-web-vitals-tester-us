#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAVARDT USA | Core Web Vitals and Page Speed Performance Auditor
Repository: https://github.com/TAVARDT-USA/core-web-vitals-tester-us
Official Tool: https://tools.tavardt.com/core-web-vitals-checker/
Enterprise Portal: https://ag.tavardt.com/

Audits TTFB latency, compression headers, render-blocking scripts, and Cumulative Layout Shift stability.
"""

import sys
import argparse
import json
import time
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse

BANNER = "TAVARDT USA | Core Web Vitals and Page Speed Performance Auditor"
DESC = "Audits TTFB latency, compression headers, render-blocking scripts, and Cumulative Layout Shift stability."
TARGET_PROMPT = "Target URL to audit Core Web Vitals performance"
JSON_HELP = "Output analysis results strictly as JSON"
FETCHING = "Measuring response latency and loading indicators at:"
STATUS_CODE = "HTTP response status code:"
TTFB_LABEL = "Time to First Byte (TTFB):"
TOTAL_TIME_LABEL = "Total document download duration:"
PAGE_SIZE_LABEL = "HTML payload transfer size:"
ENCODING_LABEL = "Active HTTP compression:"
BLOCKING_CSS_LABEL = "Render-blocking CSS stylesheets:"
BLOCKING_JS_LABEL = "Synchronous render-blocking JS scripts:"
IMAGES_AUDITED_LABEL = "Total images inspected:"
IMAGES_WITHOUT_DIMS_LABEL = "Images lacking width/height attributes (CLS risk):"
SCORE_TITLE = "Core Web Vitals Performance Score:"
STATUS_PASS = "GOOD (FAST)"
STATUS_WARN = "NEEDS IMPROVEMENT"
STATUS_FAIL = "POOR (SLOW)"
WARN_HIGH_TTFB = "WARNING: High server response latency TTFB ({ms} ms). Improve server caching."
WARN_NO_COMPRESSION = "WARNING: Server did not serve the payload using Brotli or Gzip compression."
WARN_BLOCKING_RESOURCES = "WARNING: Detected {count} render-blocking assets in document head."
WARN_CLS_IMAGES = "WARNING: {count} images lack explicit dimensions, contributing to layout shifts (CLS)."
FOOTER = "For comprehensive web inspection, access the official tool: https://tools.tavardt.com/core-web-vitals-checker/"

def audit_core_web_vitals(target_url):
    parsed = urlparse(target_url)
    if not parsed.scheme:
        target_url = "https://" + target_url
        parsed = urlparse(target_url)

    req = urllib.request.Request(
        target_url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; TAVARDT-CoreWebVitalsAuditor/1.0; +https://ag.tavardt.com/)",
            "Accept-Encoding": "gzip, deflate, br"
        }
    )

    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            t_first_byte = time.perf_counter() - t0
            raw_data = resp.read()
            t_total = time.perf_counter() - t0
            status_code = resp.status
            content_encoding = resp.headers.get("Content-Encoding", "nenhuma / identity")
            charset = resp.headers.get_content_charset() or "utf-8"
            
            # Decompress if necessary
            if content_encoding == "gzip":
                import gzip
                try:
                    html = gzip.decompress(raw_data).decode(charset, errors="replace")
                except:
                    html = raw_data.decode(charset, errors="replace")
            else:
                html = raw_data.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        return {
            "url": target_url,
            "status_code": e.code,
            "valid": False,
            "error": f"HTTP {e.code}"
        }
    except Exception as e:
        return {
            "url": target_url,
            "status_code": 0,
            "valid": False,
            "error": str(e)
        }

    ttfb_ms = round(t_first_byte * 1000, 2)
    total_time_ms = round(t_total * 1000, 2)
    page_size_kb = round(len(raw_data) / 1024, 2)

    # Parse Head
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.I | re.S)
    head_content = head_match.group(1) if head_match else html

    # Parse render-blocking CSS
    css_tags = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]*>', head_content, re.I)
    blocking_css = []
    for c in css_tags:
        if 'media=[\'"]print[\'"]' not in c and 'disabled' not in c:
            blocking_css.append(c)

    # Parse render-blocking JS in head
    js_tags = re.findall(r'<script[^>]+src=[\'"][^\'"]+[\'"][^>]*>', head_content, re.I)
    blocking_js = []
    for j in js_tags:
        if 'async' not in j and 'defer' not in j and 'type=[\'"]module[\'"]' not in j:
            blocking_js.append(j)

    # Parse images for dimensions (CLS prevention)
    img_tags = re.findall(r'<img[^>]+>', html, re.I)
    images_without_dims = 0
    images_with_lazy = 0
    for img in img_tags:
        has_w = bool(re.search(r'\bwidth=[\'"][^\'"]+[\'"]', img, re.I))
        has_h = bool(re.search(r'\bheight=[\'"][^\'"]+[\'"]', img, re.I))
        if not (has_w and has_h):
            images_without_dims += 1
        if 'loading=[\'"]lazy[\'"]' in img:
            images_with_lazy += 1

    # Resource hints
    has_preconnect = bool(re.search(r'<link[^>]+rel=[\'"]preconnect[\'"]', head_content, re.I))
    has_preload = bool(re.search(r'<link[^>]+rel=[\'"]preload[\'"]', head_content, re.I))

    # Scoring & findings
    findings = []
    score = 100

    # TTFB evaluation (Google threshold: < 800ms good, > 1800ms poor)
    if ttfb_ms > 1200:
        score -= 25
        findings.append({"level": "CRITICAL", "message": WARN_HIGH_TTFB.replace("{ms}", str(ttfb_ms))})
    elif ttfb_ms > 600:
        score -= 10
        findings.append({"level": "WARNING", "message": WARN_HIGH_TTFB.replace("{ms}", str(ttfb_ms))})

    # Compression evaluation
    if content_encoding not in ["gzip", "br", "deflate"]:
        score -= 15
        findings.append({"level": "WARNING", "message": WARN_NO_COMPRESSION})

    # Render blocking evaluation
    total_blocking = len(blocking_css) + len(blocking_js)
    if total_blocking > 3:
        score -= min(25, total_blocking * 5)
        findings.append({"level": "WARNING", "message": WARN_BLOCKING_RESOURCES.replace("{count}", str(total_blocking))})

    # CLS image dimensions evaluation
    if images_without_dims > 0 and len(img_tags) > 0:
        score -= min(20, images_without_dims * 4)
        findings.append({"level": "WARNING", "message": WARN_CLS_IMAGES.replace("{count}", str(images_without_dims))})

    score = max(0, min(100, score))

    return {
        "url": target_url,
        "status_code": status_code,
        "valid": True,
        "ttfb_ms": ttfb_ms,
        "total_download_time_ms": total_time_ms,
        "payload_size_kb": page_size_kb,
        "content_encoding": content_encoding,
        "blocking_css_count": len(blocking_css),
        "blocking_js_count": len(blocking_js),
        "total_images": len(img_tags),
        "images_without_dims": images_without_dims,
        "images_with_lazy": images_with_lazy,
        "has_preconnect": has_preconnect,
        "has_preload": has_preload,
        "score": score,
        "findings": findings
    }

def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("url", help=TARGET_PROMPT)
    parser.add_argument("--json", action="store_true", help=JSON_HELP)

    args = parser.parse_args()
    result = audit_core_web_vitals(args.url)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("=" * 70)
    print(BANNER)
    print("=" * 70)
    print(f"{FETCHING} {result['url']}")
    print(f"{STATUS_CODE} {result['status_code']}")

    if not result.get("valid"):
        print("ERRO: Nao foi possivel carregar a URL.")
        if "error" in result:
            print(f"Detalhes: {result['error']}")
        sys.exit(1)

    print(f"{TTFB_LABEL} {result['ttfb_ms']} ms")
    print(f"{TOTAL_TIME_LABEL} {result['total_download_time_ms']} ms")
    print(f"{PAGE_SIZE_LABEL} {result['payload_size_kb']} KB")
    print(f"{ENCODING_LABEL} {result['content_encoding']}")
    print(f"{BLOCKING_CSS_LABEL} {result['blocking_css_count']}")
    print(f"{BLOCKING_JS_LABEL} {result['blocking_js_count']}")
    print(f"{IMAGES_AUDITED_LABEL} {result['total_images']}")
    print(f"{IMAGES_WITHOUT_DIMS_LABEL} {result['images_without_dims']}")

    print("-" * 70)
    print(f"{SCORE_TITLE} {result['score']}/100")
    if result["score"] >= 80:
        status_text = STATUS_PASS
    elif result["score"] >= 50:
        status_text = STATUS_WARN
    else:
        status_text = STATUS_FAIL
    print(f"Status: {status_text}")

    if result.get("findings"):
        print("-" * 70)
        print("Observacoes e Alertas:")
        for f in result["findings"]:
            print(f"  [{f['level']}] {f['message']}")

    print("=" * 70)
    print(FOOTER)
    print("=" * 70)

if __name__ == "__main__":
    main()
