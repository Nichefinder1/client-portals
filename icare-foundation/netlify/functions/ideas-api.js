const BASE = process.env.AIRTABLE_BASE_ID || 'appkKo8Ap1u5ijogd';
const TABLE = 'iCare Board Ideas';
const AT_URL = `https://api.airtable.com/v0/${BASE}/${encodeURIComponent(TABLE)}`;
const IDENTITY_URL = (process.env.URL || 'https://membersportal.icaregives.org') + '/.netlify/identity';

const ALLOWED_FIELDS = new Set(['Title', 'Category', 'Description', 'Submitted By', 'Date', 'Status', 'Upvotes']);
const RECORD_ID_RE = /^rec[A-Za-z0-9]{14}$/;

async function verifyToken(authHeader) {
  if (!authHeader || !authHeader.startsWith('Bearer ')) return null;
  const token = authHeader.slice(7);
  try {
    const res = await fetch(`${IDENTITY_URL}/user`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

exports.handler = async function(event) {
  const pat = process.env.AIRTABLE_PAT;
  if (!pat) return { statusCode: 500, body: JSON.stringify({ error: 'Server error' }) };

  const atHeaders = { 'Authorization': `Bearer ${pat}`, 'Content-Type': 'application/json' };

  try {
    // GET — public read allowed (non-sensitive board ideas)
    if (event.httpMethod === 'GET') {
      const res = await fetch(`${AT_URL}?sort[0][field]=Upvotes&sort[0][direction]=desc`, { headers: atHeaders });
      if (!res.ok) return { statusCode: 502, body: JSON.stringify({ error: 'Failed to load ideas' }) };
      const data = await res.json();
      return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) };
    }

    // POST + PATCH — require valid board member token
    const user = await verifyToken(event.headers.authorization);
    if (!user) return { statusCode: 401, body: JSON.stringify({ error: 'Unauthorized' }) };

    if (event.httpMethod === 'PATCH') {
      let body;
      try { body = JSON.parse(event.body); } catch { return { statusCode: 400, body: JSON.stringify({ error: 'Invalid request' }) }; }

      const { recordId } = body;
      if (!recordId || !RECORD_ID_RE.test(recordId)) {
        return { statusCode: 400, body: JSON.stringify({ error: 'Invalid record' }) };
      }

      // Fetch current value server-side — never trust client-sent upvote count
      const getRes = await fetch(`${AT_URL}/${recordId}`, { headers: atHeaders });
      if (!getRes.ok) return { statusCode: 502, body: JSON.stringify({ error: 'Failed to fetch record' }) };
      const current = await getRes.json();
      const currentVotes = current.fields?.Upvotes || 0;

      const patchRes = await fetch(`${AT_URL}/${recordId}`, {
        method: 'PATCH', headers: atHeaders,
        body: JSON.stringify({ fields: { Upvotes: currentVotes + 1 } })
      });
      if (!patchRes.ok) return { statusCode: 502, body: JSON.stringify({ error: 'Failed to update votes' }) };
      const data = await patchRes.json();
      return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) };
    }

    if (event.httpMethod === 'POST') {
      let fields;
      try { fields = JSON.parse(event.body).fields; } catch { return { statusCode: 400, body: JSON.stringify({ error: 'Invalid request' }) }; }
      if (!fields) return { statusCode: 400, body: JSON.stringify({ error: 'Missing fields' }) };

      // Whitelist — only allow known safe fields
      const sanitized = {};
      for (const key of Object.keys(fields)) {
        if (ALLOWED_FIELDS.has(key)) sanitized[key] = fields[key];
      }
      if (!sanitized.Title) return { statusCode: 400, body: JSON.stringify({ error: 'Title is required' }) };

      const res = await fetch(AT_URL, { method: 'POST', headers: atHeaders, body: JSON.stringify({ fields: sanitized }) });
      if (!res.ok) return { statusCode: 502, body: JSON.stringify({ error: 'Failed to submit idea' }) };
      const data = await res.json();
      return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) };
    }

    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  } catch {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server error' }) };
  }
};
