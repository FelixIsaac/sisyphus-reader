// Cloudflare Pages Functions endpoint for zero-login state sync
export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const token = (url.searchParams.get("token") || "").trim().toLowerCase();

  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
    "Cache-Control": "no-store, no-cache, must-revalidate",
  };

  if (!token || token.length < 4 || token.length > 64) {
    return new Response(
      JSON.stringify({ ok: false, error: "Invalid sync token" }),
      { status: 400, headers: corsHeaders }
    );
  }

  if (!env.SISYPHUS_SYNC) {
    return new Response(
      JSON.stringify({ ok: false, error: "KV store not bound" }),
      { status: 500, headers: corsHeaders }
    );
  }

  try {
    const raw = await env.SISYPHUS_SYNC.get(`sync:${token}`, { type: "json" });
    return new Response(
      JSON.stringify({ ok: true, token, data: raw || null }),
      { status: 200, headers: corsHeaders }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: err.message }),
      { status: 500, headers: corsHeaders }
    );
  }
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  };

  if (!env.SISYPHUS_SYNC) {
    return new Response(
      JSON.stringify({ ok: false, error: "KV store not bound" }),
      { status: 500, headers: corsHeaders }
    );
  }

  try {
    const body = await request.json();
    const token = (body.token || "").trim().toLowerCase();

    if (!token || token.length < 4 || token.length > 64) {
      return new Response(
        JSON.stringify({ ok: false, error: "Invalid sync token" }),
        { status: 400, headers: corsHeaders }
      );
    }

    const incoming = body.data || {};
    
    // Fetch existing data to perform merge (Set Union for readCards)
    let existing = await env.SISYPHUS_SYNC.get(`sync:${token}`, { type: "json" });
    if (!existing || typeof existing !== "object") {
      existing = {
        readCards: {},
        currentSecId: "",
        sessionSeconds: 0,
        avgWpm: 240,
        updatedAt: 0,
      };
    }

    // Merge readCards (Union, respecting resets and unmarks)
    let mergedReadCards = incoming.reset ? {} : { ...(existing.readCards || {}) };
    if (!incoming.reset && incoming.readCards && typeof incoming.readCards === "object") {
      for (const [k, v] of Object.entries(incoming.readCards)) {
        if (!mergedReadCards[k] || (v.time && v.time > (mergedReadCards[k].time || 0))) {
          mergedReadCards[k] = v;
        }
      }
    }
    if (!incoming.reset && incoming.unmarkedCards && typeof incoming.unmarkedCards === "object") {
      for (const k of Object.keys(incoming.unmarkedCards)) {
        delete mergedReadCards[k];
      }
    }

    // Merge location and session time based on most recent updatedAt
    const incomingTime = incoming.updatedAt || Date.now();
    const existingTime = existing.updatedAt || 0;
    const isNewer = incomingTime >= existingTime;

    const merged = {
      readCards: mergedReadCards,
      unmarkedCards: incoming.reset ? {} : { ...(existing.unmarkedCards || {}), ...(incoming.unmarkedCards || {}) },
      currentSecId: isNewer ? (incoming.currentSecId || existing.currentSecId || "") : existing.currentSecId,
      sessionSeconds: incoming.reset ? 0 : Math.max(existing.sessionSeconds || 0, incoming.sessionSeconds || 0),
      avgWpm: isNewer ? (incoming.avgWpm || existing.avgWpm || 240) : (existing.avgWpm || 240),
      updatedAt: Date.now(),
    };

    // Store in KV with 1 year TTL (31536000 seconds)
    await env.SISYPHUS_SYNC.put(`sync:${token}`, JSON.stringify(merged), {
      expirationTtl: 31536000,
    });

    return new Response(
      JSON.stringify({ ok: true, token, data: merged }),
      { status: 200, headers: corsHeaders }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: err.message }),
      { status: 500, headers: corsHeaders }
    );
  }
}
