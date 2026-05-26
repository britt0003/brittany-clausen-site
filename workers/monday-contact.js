/**
 * Cloudflare Worker — monday-contact
 * Creates a new Contact item in Monday.com CRM (Contacts board: 18399391551)
 * when someone downloads the media kit from brittanyclausen.com/media-kit
 *
 * DEPLOY STEPS:
 *   1. In Cloudflare Dashboard → Workers & Pages → Create Worker
 *   2. Name it "monday-contact"
 *   3. Paste this code
 *   4. Settings → Variables → Add environment variable:
 *        MONDAY_API_TOKEN = <your Monday.com API token>
 *      (Get token: Monday.com → Avatar → Admin → API → Generate Token)
 *   5. Save and deploy
 *   6. Copy the worker URL (e.g. https://monday-contact.brittany-60b.workers.dev)
 *      and set it as WORKER_URL in media-kit.html
 */

const BOARD_ID = 18399391551;
const GROUP_ID = 'group_mm0gc68'; // "Active Contacts"
const MONDAY_API = 'https://api.monday.com/v2';

const CORS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default {
  async fetch(request, env) {
    // Preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS });
    }

    if (request.method !== 'POST') {
      return json({ error: 'Method not allowed' }, 405);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: 'Invalid JSON' }, 400);
    }

    const { firstName, lastName, email, company, phone, title, interest } = body;

    if (!email || !firstName || !lastName) {
      return json({ error: 'firstName, lastName and email are required' }, 400);
    }

    const fullName = `${firstName} ${lastName}`.trim();

    // Build column values for Monday.com
    // Column IDs from Contacts board:
    //   contact_email   → Email
    //   contact_phone   → Phone
    //   text_mm0g8x28   → Title/Position
    //   status          → Type (label_id 6 = "Lead")
    //   long_text4      → Comments (we store company + interest here)
    const notes = [
      company   ? `Organization: ${company}` : '',
      interest  ? `Interest: ${interest}`     : '',
      'Source: Media Kit Download — brittanyclausen.com',
    ].filter(Boolean).join('\n');

    const columnValues = {
      contact_email:  { email, text: email },
      status:         { label_id: 6 }, // "Lead"
      text_mm0g8x28:  title || '',
      long_text4:     { text: notes },
    };

    // Add phone only if provided (Monday.com phone needs countryShortName)
    if (phone) {
      columnValues.contact_phone = { phone, countryShortName: 'US' };
    }

    const mutation = `
      mutation CreateContact(
        $boardId: ID!,
        $groupId: String!,
        $itemName: String!,
        $columnValues: JSON!
      ) {
        create_item(
          board_id: $boardId,
          group_id: $groupId,
          item_name: $itemName,
          column_values: $columnValues
        ) {
          id
          name
        }
      }
    `;

    try {
      const res = await fetch(MONDAY_API, {
        method: 'POST',
        headers: {
          'Content-Type':  'application/json',
          'Authorization': env.MONDAY_API_TOKEN,
          'API-Version':   '2024-01',
        },
        body: JSON.stringify({
          query: mutation,
          variables: {
            boardId:      String(BOARD_ID),
            groupId:      GROUP_ID,
            itemName:     fullName,
            columnValues: JSON.stringify(columnValues),
          },
        }),
      });

      const data = await res.json();

      if (data.errors) {
        console.error('Monday.com errors:', JSON.stringify(data.errors));
        return json({ success: false, error: data.errors[0]?.message }, 500);
      }

      return json({ success: true, id: data.data?.create_item?.id });

    } catch (err) {
      console.error('Fetch error:', err.message);
      return json({ success: false, error: 'Internal error' }, 500);
    }
  },
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
}
