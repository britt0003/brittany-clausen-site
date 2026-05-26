/**
 * Cloudflare Worker — brevo-subscribe (also creates Monday.com Lead)
 *
 * Environment secrets required:
 *   BREVO_API_KEY     — Brevo / Sendinblue API key
 *   MONDAY_API_TOKEN  — Monday.com API token (Admin → API → Generate Token)
 *
 * What it does on each newsletter signup:
 *   1. Adds contact to Brevo list #2 (EQ Edge Newsletter)
 *   2. Creates a Lead contact in Monday.com Contacts board
 *      — Type: "Lead"  |  Comments: "EQ Edge Newsletter"
 */

const MONDAY_BOARD   = 18399391551;
const MONDAY_GROUP   = 'group_mm0gc68'; // Active Contacts
const MONDAY_API_URL = 'https://api.monday.com/v2';

const CORS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost({ request, env }) {
  try {
    const { email, firstName, lastName } = await request.json();

    if (!email) {
      return new Response(JSON.stringify({ error: 'Email required' }), {
        status: 400,
        headers: { ...CORS, 'Content-Type': 'application/json' },
      });
    }

    // ── 1. Add to Brevo ──────────────────────────────────────────────────────
    const brevoRes = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        'accept':       'application/json',
        'content-type': 'application/json',
        'api-key':      env.BREVO_API_KEY,
      },
      body: JSON.stringify({
        email,
        attributes: { FIRSTNAME: firstName || '', LASTNAME: lastName || '' },
        listIds: [2],
        updateEnabled: true,
      }),
    });

    const brevoOk = brevoRes.ok || brevoRes.status === 204;
    if (!brevoOk) {
      const err = await brevoRes.json().catch(() => ({}));
      const isDupe = brevoRes.status === 400 && err.code === 'duplicate_parameter';
      if (!isDupe) {
        return new Response(JSON.stringify({ error: 'Subscription failed' }), {
          status: 500,
          headers: { ...CORS, 'Content-Type': 'application/json' },
        });
      }
    }

    // ── 2. Create Lead in Monday.com (fire-and-forget, don't block signup) ──
    createMondayContact({ firstName, lastName, email, env }).catch(() => {});

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error' }), {
      status: 500,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, { headers: CORS });
}

// ── Monday.com helper ─────────────────────────────────────────────────────────

async function createMondayContact({ firstName, lastName, email, env }) {
  if (!env.MONDAY_API_TOKEN) return; // token not configured yet — skip silently

  const fullName = [firstName, lastName].filter(Boolean).join(' ') || email;

  const columnValues = {
    contact_email: { email, text: email },
    status:        { label_id: 6 },          // "Lead"
    long_text4:    { text: 'EQ Edge Newsletter' },
  };

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
      ) { id }
    }
  `;

  await fetch(MONDAY_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type':  'application/json',
      'Authorization': env.MONDAY_API_TOKEN,
      'API-Version':   '2024-01',
    },
    body: JSON.stringify({
      query: mutation,
      variables: {
        boardId:      String(MONDAY_BOARD),
        groupId:      MONDAY_GROUP,
        itemName:     fullName,
        columnValues: JSON.stringify(columnValues),
      },
    }),
  });
}
