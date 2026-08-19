# How to fix each finding

## missing-doc
Add footer links to: privacy policy, terms, cookie policy, accessibility
statement, refund/returns (if you sell), contact or imprint.

```html
<footer>
  <a href="/privacy">Privacy Policy</a>
  <a href="/terms">Terms of Service</a>
  <a href="/cookies">Cookie Policy</a>
  <a href="/accessibility">Accessibility</a>
</footer>
```

Shopify: **Settings → Policies** generates these and exposes them at
`/policies/privacy-policy` etc. Link them from the theme footer — generating
them is not enough, they have to be reachable.

## tracker-no-consent / cookie-no-consent
Load analytics and ad pixels only after consent. With Google Consent Mode v2:

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    ad_storage: 'denied',
    analytics_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });
</script>
```

Then update to `granted` from your consent banner's callback. If your banner is
client-injected, this scan cannot see it — verify manually with devtools:
load in a private window, check Application → Cookies before interacting.

## img-alt
```html
<img src="hero.jpg" alt="Walnut dining table set for six">   <!-- informative -->
<img src="swirl.svg" alt="">                                  <!-- decorative -->
```
Decorative images need `alt=""`, not a missing attribute. Never write
`alt="image"` or `alt="photo"` — present but meaningless still fails.

## html-lang
```html
<html lang="en">
```

## input-label
```html
<label for="email">Email address</label>
<input id="email" type="email" name="email">
```
Or, when no visible label fits:
```html
<input type="search" aria-label="Search products">
```
Placeholder text is not a label.

## empty-control
```html
<button aria-label="Close dialog"><svg …></svg></button>
```
Icon-only controls need an accessible name.

## no-h1
One `<h1>` per page, describing that page. Not the site name on every page.

## target-blank
```html
<a href="https://example.com" target="_blank" rel="noopener noreferrer">…</a>
```

## no-https / no-hsts
Enable TLS, redirect all http traffic to https, then add:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```
Do not add HSTS until https works everywhere — it is hard to undo.
