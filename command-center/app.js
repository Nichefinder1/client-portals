// app.js — NicheFinders Command Center

let Graph;          // 3d-force-graph instance
let allNodes = [];  // full dataset
let allEdges = [];  // full dataset
let currentLevel = 'agency';   // 'agency' | client id
let selectedNode = null;

const PORTAL_URLS = {
  'fox-valley-plumbing':          'https://nichefinder1.github.io/client-portals/fox-valley-plumbing/',
  'all-south-lightning-protection': 'https://nichefinder1.github.io/client-portals/all-south-lightning/',
};

// ── Bootstrap ──────────────────────────────────────────────────────────────
async function init() {
  const res = await fetch('data.json?v=' + Date.now());
  const data = await res.json();
  allNodes = data.nodes;
  allEdges = data.edges;

  renderMeta(data.meta);
  renderClientList(data.nodes, data.meta);
  renderUrgent(data.nodes);
  buildGraph();
}

// ── Meta / Panel ───────────────────────────────────────────────────────────
function renderMeta(meta) {
  document.getElementById('mrr-value').textContent =
    '$' + meta.mrr.toLocaleString();
  document.getElementById('hud-clients').textContent =
    meta.active_clients + ' CLIENTS';
  document.getElementById('hud-mrr').textContent =
    '$' + (meta.mrr / 1000).toFixed(0) + 'K MRR';
  document.getElementById('hud-urgent').textContent =
    meta.urgent_count + ' URGENT';
}

function renderClientList(nodes) {
  const list = document.getElementById('client-list');
  list.innerHTML = '';
  nodes
    .filter(n => n.type === 'client')
    .forEach(n => {
      const li = document.createElement('li');
      li.dataset.id = n.id;
      li.innerHTML = `
        <span class="client-dot" style="background:${n.color};box-shadow:0 0 5px ${n.color}"></span>
        <span class="client-name">${n.label}</span>
        <span class="client-value">$${(n.monthly_value/1000).toFixed(0)}K</span>
      `;
      li.addEventListener('click', () => flyIntoClient(n.id));
      list.appendChild(li);
    });
}

function renderUrgent(nodes) {
  const list = document.getElementById('urgent-list');
  list.innerHTML = '';
  nodes
    .filter(n => n.urgent && n.next_action)
    .slice(0, 5)
    .forEach(n => {
      const li = document.createElement('li');
      li.textContent = `${n.label}: ${n.next_action.slice(0, 40)}`;
      list.appendChild(li);
    });
}

function showNodeDetail(node) {
  selectedNode = node;
  const detail = document.getElementById('node-detail');
  detail.classList.add('visible');

  const color = node.color || '#ffffff';
  document.getElementById('node-name').textContent = node.label;
  document.getElementById('node-name').style.color = color;

  const rows = document.getElementById('detail-rows');
  rows.innerHTML = '';

  const fields = [
    ['Type',        node.type],
    ['Status',      node.status],
    ['Health',      node.health],
    ['MRR',         node.monthly_value > 0 ? '$' + node.monthly_value.toLocaleString() + '/mo' : '—'],
    ['Next Action', node.next_action || '—'],
  ];
  for (const [key, val] of fields) {
    const row = document.createElement('div');
    row.className = 'detail-row';
    row.innerHTML = `<span class="key">${key}</span><span class="val">${val}</span>`;
    rows.appendChild(row);
  }

  const portalLink = document.getElementById('portal-link');
  const url = PORTAL_URLS[node.id];
  if (url && node.type === 'client') {
    portalLink.href = url;
    portalLink.style.display = 'inline-block';
    portalLink.textContent = '↗ OPEN CLIENT PORTAL';
  } else {
    portalLink.style.display = 'none';
  }
}

// ── Graph ───────────────────────────────────────────────────────────────────
function buildGraph() {
  const container = document.getElementById('graph-container');
  const w = container.offsetWidth  || Math.floor(window.innerWidth * 0.6);
  const h = container.offsetHeight || (window.innerHeight - 36);

  Graph = ForceGraph3D()(container)
    .width(w)
    .height(h)
    .backgroundColor('#020b18')
    .showNavInfo(false)
    .nodeLabel(n => n.label)
    .d3AlphaDecay(0.02)
    .d3VelocityDecay(0.3)
    .nodeThreeObjectExtend(true)
    .nodeThreeObject(n => {
      if (n.type === 'service' || n.type === 'project') return null;
      const size = nodeSizeByType(n.type);
      const sprite = new SpriteText(n.label);
      sprite.color = n.type === 'agency' ? '#7c3aed' : (n.color || '#ffffff');
      sprite.textHeight = n.type === 'agency' ? 5 : n.type === 'client' ? 4 : 2.5;
      sprite.fontFace = 'Arial';
      sprite.fontWeight = 'bold';
      sprite.position.y = size + 4;
      n.__labelSprite = sprite;
      return sprite;
    })
    .nodeColor(n => n.type === 'agency' ? '#7c3aed' : (n.color || '#ffffff'))
    .nodeOpacity(0.95)
    .nodeResolution(32)
    .nodeVal(n => nodeSizeByType(n.type))
    .linkColor(() => 'rgba(0,180,255,0.25)')
    .linkWidth(0.5)
    .linkOpacity(1)
    .onNodeClick(handleNodeClick)
    .onNodeHover(handleNodeHover);

  // Strong repulsion + collision so nodes never overlap
  const chargeForce = Graph.d3Force('charge');
  if (chargeForce && typeof chargeForce.strength === 'function') {
    chargeForce.strength(-800).distanceMax(600);
  }
  const linkForce = Graph.d3Force('link');
  if (linkForce && typeof linkForce.distance === 'function') {
    linkForce.distance(n => n.source?.type === 'agency' ? 100 : 60);
  }

  window.addEventListener('resize', () => {
    const nw = container.offsetWidth;
    const nh = container.offsetHeight;
    Graph.width(nw).height(nh);
  });

  // Star field goes behind the graph — z-index:0 so the WebGL canvas (z-index:1) is on top
  addStarField(container);

  // The ForceGraph3D canvas was appended first — select it and raise it above the star canvas
  const graphCanvas = container.querySelector('canvas');
  if (graphCanvas) {
    graphCanvas.style.position = 'absolute';
    graphCanvas.style.top = '0';
    graphCanvas.style.left = '0';
    graphCanvas.style.zIndex = '1';
  }

  // Give the library one frame to finish internal scene setup before feeding data
  setTimeout(() => renderAgencyGraph(), 0);
}

function nodeSizeByType(type) {
  return { agency: 20, client: 8, prospect: 3, project: 2, service: 2 }[type] || 2;
}

function renderAgencyGraph() {
  currentLevel = 'agency';
  document.getElementById('breadcrumb').classList.remove('visible');

  // Prospects removed from graph — shown in Pipeline panel instead
  const nodes = allNodes.filter(n => n.level <= 1 && n.type !== 'prospect');
  const edges = allEdges.filter(e =>
    nodes.find(n => n.id === e.source) && nodes.find(n => n.id === e.target)
  );

  const clonedNodes = structuredClone(nodes);
  // Pin agency hub to center so prospects never overlap it
  const hub = clonedNodes.find(n => n.type === 'agency');
  if (hub) { hub.fx = 0; hub.fy = 0; hub.fz = 0; }
  Graph.graphData({ nodes: clonedNodes, links: structuredClone(edges) });
  // Kick the renderer in case the animation loop stalled on first load
  if (typeof Graph.refresh === 'function') Graph.refresh();
  setTimeout(() => Graph.zoomToFit(400, 40), 1000);
}

function flyIntoClient(clientId) {
  currentLevel = clientId;
  const client = allNodes.find(n => n.id === clientId);
  if (!client) return;

  showNodeDetail(client);

  // Show breadcrumb
  const bc = document.getElementById('breadcrumb');
  bc.textContent = `◀ AGENCY  /  ${client.label.toUpperCase()}`;
  bc.classList.add('visible');

  // Build sub-graph: client hub + their level-2 children
  const clientNode = structuredClone(client);
  clientNode.level = 0; // promote to hub

  const children = allNodes
    .filter(n => n.parentId === clientId)
    .map(n => structuredClone(n));

  const subEdges = allEdges
    .filter(e => e.source === clientId)
    .map(e => structuredClone(e));

  Graph.graphData({
    nodes: [clientNode, ...children],
    links: subEdges,
  });

  // Re-center camera
  setTimeout(() => {
    Graph.zoomToFit(800, 80);
  }, 600);
}

function handleNodeClick(node) {
  if (currentLevel === 'agency') {
    if (node.type === 'client') {
      flyIntoClient(node.id);
    } else {
      showNodeDetail(node);
    }
  } else {
    showNodeDetail(node);
  }
}

let _lastHovered = null;
function handleNodeHover(node) {
  document.getElementById('graph-container').style.cursor = node ? 'pointer' : 'default';
  if (_lastHovered && _lastHovered.__labelSprite) {
    _lastHovered.__labelSprite.textHeight = _lastHovered.type === 'agency' ? 5 : _lastHovered.type === 'client' ? 4 : 2.5;
  }
  _lastHovered = node;
  if (node && node.__labelSprite) {
    node.__labelSprite.textHeight = node.type === 'agency' ? 7 : node.type === 'client' ? 6 : 4;
  }
}

// ── Star Field ──────────────────────────────────────────────────────────────
function addStarField(container) {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none;z-index:0';
  canvas.width  = container.offsetWidth  || window.innerWidth * 0.6;
  canvas.height = container.offsetHeight || window.innerHeight;
  container.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  const stars = Array.from({ length: 180 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 1.2 + 0.2,
    o: Math.random() * 0.35 + 0.05,
  }));

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const s of stars) {
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255,255,255,${s.o})`;
    ctx.fill();
  }
}

// ── Breadcrumb back ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('breadcrumb').addEventListener('click', () => {
    document.getElementById('node-detail').classList.remove('visible');
    renderAgencyGraph();
  });

  // Force layout to paint before graph init so offsetWidth/Height are non-zero
  requestAnimationFrame(() => requestAnimationFrame(() => init()));
});
