# Teamulate

Static marketing site for Teamulate. No build step. No public price list. Multi-client login is not built.

| Page | File |
| --- | --- |
| Home | `index.html` |
| How it works | `how-it-works.html` |
| AI Team | `marketing.html` |
| Workflows | `workflows.html` |
| Research hub | `research.html` |
| About | `about.html` |
| Demo stepper | `demo.html` |
| Public demo dashboard | `demo-dashboard.html` |
| Product dashboard (noindex) | `dashboard.html` |
| Campaigns / Content / Leads / SEO / Social / Reports / Settings | matching `.html` files |
| Design partner | `design-partner.html` |
| Thank you | `thank-you.html` |
| Login (noindex, Tenant 0 preview) | `login.html` |
| Pricing (noindex, no numbers) | `pricing.html` |

Product dashboard pages share `css/app.css` + `js/app.js`. Sample figures are demo data only and carry a persistent banner. `robots.txt` allows marketing pages and the public demo dashboard, and disallows shop slugs plus the internal app pages. Canonical host: `https://teamulate.ca`.

## Preview locally

```bash
python3 -m http.server 8080
```

Official logo: `assets/teamulate-logo.png`. Mark: `assets/teamulate-mark.png`.

## Contact

contact@teamulate.ca · Chris Momchilov · Barrie, Ontario
