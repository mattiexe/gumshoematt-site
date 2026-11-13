// Receives a suggestion from the site, checks Cloudflare Turnstile, mails it to the site owner via Resend.
// Needs Vercel env vars: TURNSTILE_SECRET, RESEND_API_KEY, SUGGESTION_TO. Without them it answers 503.
module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ error: 'Method not allowed' }); }
  const { TURNSTILE_SECRET, RESEND_API_KEY, SUGGESTION_TO } = process.env;
  if (!TURNSTILE_SECRET || !RESEND_API_KEY || !SUGGESTION_TO) return res.status(503).json({ error: 'The suggestion box is not open yet. Try again soon.' });
  const b = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
  const name = clean(b.name, 80), email = clean(b.email, 120), text = clean(b.suggestion, 2000);
  if (b.website) return res.status(200).json({ ok: true }); // honeypot: pretend it worked
  if (!name || !text || !/^\S+@\S+\.\S+$/.test(email)) return res.status(400).json({ error: 'Fill in your name, a valid email and your suggestion.' });
  if (!b.token) return res.status(400).json({ error: 'Please complete the captcha first.' });
  try {
    const v = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ secret: TURNSTILE_SECRET, response: String(b.token) }),
    }).then((r) => r.json());
    if (!v.success) return res.status(400).json({ error: 'Captcha failed. Try again.' });
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST', headers: { Authorization: 'Bearer ' + RESEND_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: 'Gumshoematt site <onboarding@resend.dev>', to: [SUGGESTION_TO], reply_to: email, subject: 'Game suggestion from ' + name, text: 'From: ' + name + ' <' + email + '>\n\n' + text }),
    });
    if (!r.ok) return res.status(502).json({ error: 'Could not send right now. Try again later.' });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ error: 'Something went wrong. Try again later.' });
  }
};
function safeParse(s) { try { return JSON.parse(s); } catch (e) { return {}; } }
function clean(v, max) { return String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max); }
