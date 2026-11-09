(function () {
  // Online: folders change the background on hover/focus
  var folders = document.querySelector('.folders');
  if (folders) {
    var bgs = document.querySelectorAll('.files-hero .bg');
    var title = document.getElementById('fh-title'), eyebrow = document.getElementById('fh-eyebrow'), score = document.getElementById('fh-score');
    var items = folders.querySelectorAll('.folder');
    function set(i) {
      items.forEach(function (f) { f.classList.toggle('on', +f.dataset.i === i); });
      bgs.forEach(function (b) { b.classList.toggle('on', +b.dataset.i === i); });
      folders.classList.toggle('active', i >= 0);
      if (i < 0) { title.textContent = 'The best on file.'; eyebrow.textContent = 'FILE B · ON SCREEN'; score.textContent = ''; return; }
      var f = items[i];
      title.textContent = f.dataset.name; eyebrow.textContent = 'CASE No. ' + String(i + 1).padStart(3, '0'); score.textContent = 'My score: ' + f.dataset.score;
    }
    items.forEach(function (f) {
      f.addEventListener('mouseenter', function () { set(+f.dataset.i); });
      f.addEventListener('focus', function () { set(+f.dataset.i); });
    });
    document.querySelector('.files-hero').addEventListener('mouseleave', function () { set(-1); });
  }

  // Archive: filter + sort
  document.querySelectorAll('.archive').forEach(function (arc) {
    var grid = arc.querySelector('[data-grid]');
    if (!grid) return;
    var filter = 'All', sort = (arc.querySelector('.sort.on') || {}).dataset ? arc.querySelector('.sort.on').dataset.sort : 'name';
    var cards = Array.prototype.slice.call(grid.children);
    function apply() {
      cards.forEach(function (c) { c.hidden = !(filter === 'All' || c.dataset.kind === filter); });
      var sorted = cards.slice().sort(function (a, b) {
        if (sort === 'name') return a.dataset.name.localeCompare(b.dataset.name);
        return (+b.dataset.score) - (+a.dataset.score);
      });
      sorted.forEach(function (c) { grid.appendChild(c); });
    }
    arc.querySelectorAll('.chip').forEach(function (b) {
      b.addEventListener('click', function () {
        filter = b.dataset.filter;
        arc.querySelectorAll('.chip').forEach(function (x) { x.classList.toggle('on', x === b); });
        apply();
      });
    });
    arc.querySelectorAll('.sort').forEach(function (b) {
      b.addEventListener('click', function () {
        sort = b.dataset.sort;
        arc.querySelectorAll('.sort').forEach(function (x) { x.classList.toggle('on', x === b); });
        apply();
      });
    });
    apply();
  });

  // Offline: ring-bound flip stack
  var stack = document.getElementById('stack');
  if (stack) {
    var cardsF = stack.querySelectorAll('.flipcard'), n = cardsF.length, idx = 0;
    var pos = document.getElementById('stack-pos'), next = document.getElementById('next');
    function render() {
      cardsF.forEach(function (c, i) {
        var k = i - idx;
        c.classList.toggle('cur', k === 0);
        if (k < 0) { c.style.transform = 'rotateX(172deg)'; c.style.opacity = 0; }
        else { var d = Math.min(k, 3); c.style.transform = 'translateY(' + d * 18 + 'px) scale(' + (1 - d * 0.035) + ')'; c.style.opacity = k > 3 ? 0 : 1; }
      });
      stack.classList.toggle('done', idx >= n);
      pos.textContent = 'File ' + Math.min(idx + 1, n) + ' of ' + n;
      next.textContent = idx >= n - 1 ? 'Last card' : 'Flip →';
    }
    next.addEventListener('click', function () { idx = Math.min(idx + 1, n); render(); });
    document.getElementById('prev').addEventListener('click', function () { idx = Math.max(idx - 1, 0); render(); });
    document.getElementById('restart').addEventListener('click', function () { idx = 0; render(); });
    render();
  }
})();
(function () {
  var host = document.getElementById('gm-page');
  if (!host || !window.GM) return;
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function sc(s) { return s === null ? 'Not scored yet' : String(s).replace('.', ',') + '/10'; }
  var slug = new URLSearchParams(location.search).get('g');
  var isBox = location.pathname.indexOf('box') > -1;
  var list = isBox ? GM.b : GM.g;
  var idx = -1; list.forEach(function (x, i) { if (x[0] === slug) idx = i; });
  if (idx < 0) { host.innerHTML = '<section class="wrap pagehead"><h1>Case not found.</h1><p class="lede"><a href="/">Back to the files</a></p></section>'; return; }
  var no = String(idx + 1).padStart(3, '0'), h = '';
  if (!isBox) {
    var g = list[idx], name = g[1], app = g[2], s = g[3], rec = g[4], base = GM.cdn + app + '/';
    document.title = name + ': review | Gumshoematt';
    var verdict = { 'Recommended': 'RECOMMENDED', 'Not for me': 'NOT FOR ME', 'On file': 'ON FILE' }[rec];
    var rel = list.filter(function (x) { return x[0] !== g[0] && x[3] !== null; }).sort(function (a, b) { var t = s === null ? 8 : s; return Math.abs(a[3] - t) - Math.abs(b[3] - t); }).slice(0, 3);
    h = '<div class="wrap crumbs"><a href="/online.html">← Online games</a><span> / Case No. ' + no + '</span></div>' +
      '<section class="wrap gtop"><div class="gbanner"><img src="' + base + g[6] + '" alt="' + esc(name) + '"><span class="tape">CASE No. ' + no + ' · ON SCREEN<b class="tape-score"> · ' + sc(s) + '</b></span></div>' +
      '<div class="ghead"><span class="eyebrow">' + esc(g[7].toUpperCase()) + ' · ' + esc(g[8]) + '</span><h1>' + esc(name) + '</h1>' +
      '<div class="scorecard kraft"><span class="lbl">GUMSHOE SCORE</span><span class="num">' + (s === null ? '?' : String(s).replace('.', ',')) + '<small>/10</small></span><span class="verdict">' + verdict + '</span></div></div></section>' +
      '<section class="wrap gbody"><div class="take"><span class="eyebrow">MY TAKE</span><p>' + esc(g[5]) + '</p><span class="sig">Matthias</span></div>' +
      '<div class="facts"><div><span>DEVELOPER</span>' + esc(g[7]) + '</div><div><span>RELEASED</span>' + esc(g[8]) + '</div><div><span>MY VERDICT</span>' + esc(rec) + '</div></div>' +
      '<div><span class="eyebrow">EVIDENCE</span><div class="evidence">' + g[9].map(function (u, k) { return '<a href="' + base + u + '" target="_blank" rel="noopener"><img src="' + base + u + '" alt="' + esc(name) + ' screenshot ' + (k + 1) + '" loading="lazy"></a>'; }).join('') + '</div></div>' +
      '<div class="btns"><a class="btn solid light" href="https://store.steampowered.com/app/' + app + '/">Get it on Steam' + (g[10] ? ' · ' + g[10] : '') + ' →</a><a class="btn ghost" href="https://store.steampowered.com/curator/46277857/">Follow my Steam curator page</a></div>' + (g[10] ? '<p class="pricenote">Steam price in Belgium, checked ' + GM.checked + '. Sales change it.</p>' : '') + '</section>' +
      '<section class="band"><div class="wrap archive"><h2 class="mid">Related cases</h2><div class="grid">' + rel.map(function (x) { return '<a class="card newsprint" href="/game.html?g=' + x[0] + '"><img src="' + GM.cdn + x[2] + '/' + x[6] + '" alt="' + esc(x[1]) + '" loading="lazy" class="ban"><span class="row"><span class="name">' + esc(x[1]) + '</span><span class="score">' + sc(x[3]) + '</span></span></a>'; }).join('') + '</div></div></section>';
  } else {
    var o = list[idx];
    document.title = o[1] + ' | Gumshoematt';
    h = '<div class="wrap crumbs"><a href="/offline.html">← Offline games</a><span> / ' + esc(o[7]) + '</span></div>' +
      '<section class="wrap gtop"><div class="gbox kraft"><img src="' + o[6] + '" alt="' + esc(o[1]) + '"><span class="tape">' + esc(o[2].toUpperCase()) + '</span></div>' +
      '<div class="ghead"><span class="eyebrow">ON THE TABLE · ' + esc(o[7].toUpperCase()) + '</span><h1>' + esc(o[1]) + '</h1><div class="scorecard kraft"><span class="lbl">GUMSHOE SCORE</span><span class="num pend">Not scored yet</span></div></div></section>' +
      '<section class="wrap gbody"><div class="take"><span class="eyebrow">MY TAKE</span><p>' + esc(o[5]) + '</p><span class="sig">Matthias</span></div>' +
      '<div class="facts"><div><span>TYPE</span>' + esc(o[2]) + '</div><div><span>PLAYERS</span>' + esc(o[3]) + '</div><div><span>TIME</span>' + esc(o[4]) + '</div></div>' +
      '<div class="btns"><a class="btn ghost" href="https://www.instagram.com/gumshoematt/">See the post on Instagram</a></div></section>' +
      '<section class="band"><div class="wrap archive"><h2 class="mid">More on the table</h2><div class="grid">' + list.filter(function (x) { return x[0] !== o[0]; }).map(function (x) { return '<a class="card newsprint" href="/box.html?g=' + x[0] + '"><span class="boxwrap"><img src="' + x[6] + '" alt="' + esc(x[1]) + '" loading="lazy"></span><span class="tag">' + esc(x[2].toUpperCase()) + '</span><span class="name">' + esc(x[1]) + '</span><span class="row"><span class="score small">Not scored yet</span><span class="more">Open file →</span></span></a>'; }).join('') + '</div></div></section>';
  }
  host.innerHTML = h;
})();
