const SITE_ID = '602a70e6-590b-43c8-bf85-6c822b237f39';
const IDENTITY_URL = (process.env.URL || 'https://membersportal.icaregives.org') + '/.netlify/identity';

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
  const token = process.env.NETLIFY_API_TOKEN;
  if (!token) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server misconfigured' }) };
  }

  const user = await verifyToken(event.headers.authorization);
  if (!user) {
    return { statusCode: 401, body: JSON.stringify({ error: 'Unauthorized' }) };
  }

  try {
    // Get form ID for governance-doc-upload
    const formsRes = await fetch(
      `https://api.netlify.com/api/v1/sites/${SITE_ID}/forms`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    if (!formsRes.ok) throw new Error('Failed to fetch forms');
    const forms = await formsRes.json();
    const uploadForm = forms.find(f => f.name === 'governance-doc-upload');
    if (!uploadForm) {
      return { statusCode: 200, body: JSON.stringify({ submissions: [] }) };
    }

    // Paginate through all submissions
    const allSubmissions = [];
    let page = 1;
    const perPage = 100;

    while (true) {
      const subsRes = await fetch(
        `https://api.netlify.com/api/v1/forms/${uploadForm.id}/submissions?per_page=${perPage}&page=${page}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (!subsRes.ok) throw new Error('Failed to fetch submissions');
      const batch = await subsRes.json();
      allSubmissions.push(...batch);
      if (batch.length < perPage) break;
      page++;
    }

    const docs = allSubmissions.map(sub => ({
      id: sub.id,
      docType: sub.data?.['doc-type'] || '',
      docName: sub.data?.['doc-name'] || '',
      uploadedBy: sub.data?.['uploaded-by'] || '',
      uploadDate: sub.data?.['upload-date'] || sub.created_at,
      fileUrl: sub.data?.file?.url || null,
      fileName: sub.data?.file?.filename || null,
      fileSize: sub.data?.file?.size || 0
    }));

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ submissions: docs })
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server error' }) };
  }
};
