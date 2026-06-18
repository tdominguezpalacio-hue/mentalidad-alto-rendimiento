from __future__ import annotations

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))
PDF_PATH = Path("Mentalidad_2025.pdf")
CONTACT_PHONE = "+573142961072"
CONTACT_EMAIL = "afgr840108@gmail.com"


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Mentalidad de Alto Rendimiento</title>
  <meta name="description" content="Pagina promocional inspirada en el portafolio Mentalidad 2025 de Andres Gonzalez." />
  <style>
    :root {
      --black: #050505;
      --ink: #0d0d0d;
      --panel: #141414;
      --white: #f7f7f2;
      --soft: #e1e1dc;
      --muted: #9a9a95;
      --line: rgba(247,247,242,.15);
      --red: #b6121b;
      --red-soft: rgba(182,18,27,.2);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--black);
      color: var(--white);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      overflow-x: hidden;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
      background-size: 72px 72px;
      mask-image: linear-gradient(90deg, black, transparent 82%);
      z-index: -3;
    }

    body::after {
      content: "";
      position: fixed;
      inset: -20%;
      pointer-events: none;
      background: linear-gradient(120deg, transparent 34%, rgba(255,255,255,.055) 48%, transparent 62%);
      animation: scan 9s ease-in-out infinite;
      z-index: -2;
    }

    .curve-layer {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: -1;
      overflow: hidden;
    }

    .curve-layer svg {
      position: absolute;
      opacity: .14;
      animation: drift 18s ease-in-out infinite;
    }

    .curve-layer svg:nth-child(1) { top: -8%; left: -6%; width: 58vw; }
    .curve-layer svg:nth-child(2) { bottom: -12%; right: -8%; width: 52vw; animation-delay: -6s; }
    .curve-layer svg:nth-child(3) { top: 38%; right: -14%; width: 40vw; animation-delay: -12s; opacity: .09; }

    .orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      pointer-events: none;
      z-index: 0;
      animation: orbFloat 12s ease-in-out infinite;
    }

    .orb-red { width: 320px; height: 320px; background: var(--red-soft); top: 12%; right: 8%; }
    .orb-gray { width: 280px; height: 280px; background: rgba(154,154,149,.12); bottom: 18%; left: 4%; animation-delay: -4s; }

    @keyframes scan {
      0%, 100% { transform: translateX(-22%); opacity: .28; }
      50% { transform: translateX(22%); opacity: .8; }
    }

    @keyframes drift {
      0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg); }
      50% { transform: translate3d(18px, -24px, 0) rotate(2deg); }
    }

    @keyframes orbFloat {
      0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
      50% { transform: translate3d(0, -28px, 0) scale(1.08); }
    }

    .progress {
      position: fixed;
      top: 0;
      left: 0;
      width: 0;
      height: 3px;
      background: var(--red);
      z-index: 30;
    }

    nav {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      min-height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 clamp(18px, 4vw, 54px);
      background: rgba(5,5,5,.76);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(18px);
      z-index: 20;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 900;
      text-transform: uppercase;
    }

    .brand-mark {
      width: 32px;
      height: 32px;
      border: 2px solid var(--white);
      transform: rotate(45deg);
      position: relative;
      animation: markPulse 2.8s ease-in-out infinite;
    }

    .brand-mark::after {
      content: "";
      position: absolute;
      inset: 8px;
      background: var(--white);
    }

    @keyframes markPulse {
      50% { border-color: var(--red); box-shadow: 0 0 28px var(--red-soft); }
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    a, button { font: inherit; }

    .nav-links a,
    .button {
      min-height: 42px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 10px 16px;
      border: 1px solid transparent;
      text-decoration: none;
      color: var(--white);
      font-size: 14px;
      font-weight: 750;
      transition: transform .25s ease, background .25s ease, border-color .25s ease;
    }

    .nav-links a:hover,
    .button.secondary:hover {
      transform: translateY(-2px);
      border-color: var(--line);
      background: rgba(255,255,255,.06);
    }

    .button.primary,
    .nav-links a.primary {
      color: var(--black);
      background: var(--white);
      border-color: var(--white);
      cursor: pointer;
    }

    .button.primary:hover,
    .nav-links a.primary:hover {
      transform: translateY(-3px);
      background: var(--soft);
    }

    main { padding-top: 72px; }

    section {
      padding: clamp(72px, 9vw, 126px) clamp(18px, 4vw, 54px);
      position: relative;
    }

    .hero {
      min-height: calc(100vh - 72px);
      display: grid;
      grid-template-columns: minmax(0, .9fr) minmax(340px, 1.1fr);
      align-items: center;
      gap: clamp(32px, 6vw, 86px);
      overflow: hidden;
    }

    .hero::after {
      content: "";
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      width: min(52vw, 720px);
      background:
        linear-gradient(90deg, var(--black), rgba(5,5,5,.5) 36%, rgba(5,5,5,.1)),
        url("/asset/2/0") center / cover;
      filter: grayscale(1) contrast(1.06);
      opacity: .48;
      mask-image: linear-gradient(90deg, transparent, black 28%, black);
      z-index: -1;
    }

    .hero > * {
      position: relative;
      z-index: 1;
    }

    .quote {
      color: var(--muted);
      text-transform: uppercase;
      font-weight: 850;
      font-size: clamp(11px, 1.2vw, 14px);
      letter-spacing: .22em;
      line-height: 1.9;
      max-width: 720px;
      margin: 0 0 36px;
    }

    .eyebrow {
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .18em;
      font-size: 12px;
      font-weight: 900;
      margin-bottom: 18px;
    }

    h1, h2, h3, p { margin-top: 0; }

    h1 {
      font-size: clamp(48px, 8vw, 116px);
      line-height: .86;
      text-transform: uppercase;
      max-width: 760px;
      margin-bottom: 26px;
    }

    h1 .thin {
      display: block;
      color: var(--muted);
      font-weight: 500;
    }

    h1 .accent,
    h2 .accent {
      display: inline-block;
      color: var(--white);
      position: relative;
    }

    h1 .accent::after,
    h2 .accent::after {
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      bottom: .04em;
      height: .08em;
      background: var(--red);
      z-index: -1;
    }

    .lead {
      color: var(--soft);
      font-size: clamp(18px, 2vw, 24px);
      line-height: 1.5;
      max-width: 760px;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 32px;
    }

    .hero-visual {
      min-height: 650px;
      position: relative;
    }

    .portrait-card {
      position: absolute;
      inset: 0 12% 0 12%;
      border: 1px solid var(--line);
      background: var(--panel);
      overflow: hidden;
      box-shadow: 0 40px 120px rgba(0,0,0,.55);
      transform: rotate(-1.5deg);
      animation: floatCard 6s ease-in-out infinite;
    }

    .portrait-card img,
    .photo-tile img,
    .profile-photo img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      filter: grayscale(1) contrast(1.12);
      transition: filter .45s ease, transform .55s ease;
    }

    .portrait-card:hover img,
    .photo-tile:hover img,
    .profile-photo:hover img {
      filter: grayscale(.25) contrast(1.08);
      transform: scale(1.035);
    }

    .portrait-label {
      position: absolute;
      left: 22px;
      right: 22px;
      bottom: 22px;
      padding: 18px;
      border: 1px solid var(--line);
      background: rgba(5,5,5,.76);
      backdrop-filter: blur(16px);
    }

    .portrait-label strong {
      display: block;
      text-transform: uppercase;
      font-size: 22px;
      margin-bottom: 6px;
    }

    .portrait-label span {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }

    .mini-photo {
      position: absolute;
      width: min(210px, 34%);
      aspect-ratio: 1 / 1.16;
      right: 0;
      top: 9%;
      border: 1px solid var(--line);
      overflow: hidden;
      background: var(--ink);
      animation: floatCard 5s ease-in-out infinite reverse;
    }

    .mini-photo img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      filter: grayscale(1) contrast(1.1);
    }

    @keyframes floatCard {
      50% { transform: translateY(-14px) rotate(.6deg); }
    }

    .marquee {
      padding-top: 24px;
      padding-bottom: 24px;
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      overflow: hidden;
    }

    .marquee-track {
      width: max-content;
      display: flex;
      gap: 42px;
      color: var(--muted);
      text-transform: uppercase;
      font-size: clamp(24px, 4vw, 52px);
      font-weight: 950;
      animation: move 20s linear infinite;
    }

    .marquee-track span:nth-child(3n) { color: var(--white); }
    @keyframes move { to { transform: translateX(-50%); } }

    .split {
      display: grid;
      grid-template-columns: minmax(320px, .9fr) minmax(0, 1.1fr);
      gap: clamp(32px, 6vw, 88px);
      align-items: center;
    }

    .section-head {
      max-width: 820px;
      margin-bottom: 46px;
    }

    h2 {
      font-size: clamp(38px, 6vw, 78px);
      line-height: .94;
      text-transform: uppercase;
      margin-bottom: 22px;
    }

    .profile-photo {
      min-height: 620px;
      border: 1px solid var(--line);
      overflow: hidden;
      background: var(--panel);
      position: relative;
    }

    .bio {
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      padding: 28px 0;
      margin: 28px 0;
    }

    .bio p {
      color: var(--soft);
      font-size: clamp(18px, 2vw, 24px);
      line-height: 1.55;
      margin-bottom: 0;
    }

    .club-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      border: 1px solid var(--line);
    }

    .club {
      min-height: 92px;
      display: grid;
      place-items: center;
      padding: 16px;
      border-right: 1px solid var(--line);
      text-align: center;
      color: var(--muted);
      text-transform: uppercase;
      font-size: 13px;
      font-weight: 900;
    }

    .club:last-child { border-right: 0; }

    .pillars {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }

    .pillars-12 {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }

    .pricing-wrap {
      border: 1px solid var(--line);
      background: rgba(255,255,255,.03);
      overflow: hidden;
    }

    .pricing-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    .pricing-table th,
    .pricing-table td {
      padding: 18px 22px;
      border-bottom: 1px solid var(--line);
      text-align: left;
    }

    .pricing-table th {
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .14em;
      font-size: 11px;
      font-weight: 900;
      background: rgba(255,255,255,.04);
    }

    .pricing-table td:last-child,
    .pricing-table th:last-child { text-align: right; }

    .pricing-table tr:last-child td { border-bottom: 0; }

    .pricing-table .highlight {
      color: var(--white);
      font-weight: 900;
      font-size: clamp(20px, 2.4vw, 28px);
    }

    .pricing-note {
      padding: 22px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.65;
      border-top: 1px solid var(--line);
    }

    .contact-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 32px;
    }

    .contact-card {
      border: 1px solid var(--line);
      padding: 28px;
      background: rgba(255,255,255,.035);
      text-decoration: none;
      color: var(--white);
      transition: transform .3s ease, border-color .3s ease, background .3s ease;
      display: block;
    }

    .contact-card:hover {
      transform: translateY(-6px);
      border-color: rgba(255,255,255,.32);
      background: rgba(255,255,255,.06);
    }

    .contact-card span {
      display: block;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .16em;
      font-size: 11px;
      font-weight: 900;
      margin-bottom: 10px;
    }

    .contact-card strong {
      font-size: clamp(18px, 2.2vw, 26px);
      font-weight: 850;
    }

    .reveal:nth-child(2) { transition-delay: .08s; }
    .reveal:nth-child(3) { transition-delay: .16s; }
    .reveal:nth-child(4) { transition-delay: .24s; }

    .pillar,
    .week,
    .plan-card {
      border: 1px solid var(--line);
      background: rgba(255,255,255,.035);
      padding: 22px;
      min-height: 270px;
      position: relative;
      overflow: hidden;
      transition: transform .32s ease, background .32s ease, border-color .32s ease;
    }

    .pillar:hover,
    .week:hover,
    .plan-card:hover {
      transform: translateY(-9px);
      border-color: rgba(255,255,255,.34);
      background: rgba(255,255,255,.065);
    }

    .num {
      color: var(--muted);
      font-size: 14px;
      font-weight: 950;
      letter-spacing: .18em;
      margin-bottom: 54px;
    }

    .pillar h3,
    .week h3,
    .plan-card h3 {
      text-transform: uppercase;
      font-size: 21px;
      line-height: 1.1;
      margin-bottom: 14px;
    }

    .pillar p,
    .week p,
    .plan-card p {
      color: var(--muted);
      line-height: 1.58;
      margin-bottom: 0;
    }

    .pillar::after,
    .week::after,
    .plan-card::after {
      content: "";
      position: absolute;
      left: 22px;
      right: 22px;
      bottom: 22px;
      height: 2px;
      background: var(--red);
      transform: scaleX(.2);
      transform-origin: left;
      transition: transform .35s ease;
    }

    .pillar:hover::after,
    .week:hover::after,
    .plan-card:hover::after {
      transform: scaleX(1);
    }

    .gallery {
      display: grid;
      grid-template-columns: 1.1fr .9fr 1fr;
      gap: 14px;
      min-height: 560px;
    }

    .photo-tile {
      min-height: 280px;
      border: 1px solid var(--line);
      background: var(--panel);
      overflow: hidden;
      position: relative;
    }

    .photo-tile.tall { grid-row: span 2; }

    .photo-caption {
      position: absolute;
      left: 16px;
      right: 16px;
      bottom: 16px;
      padding: 12px;
      background: rgba(5,5,5,.74);
      border: 1px solid var(--line);
      color: var(--soft);
      font-size: 13px;
      text-transform: uppercase;
      font-weight: 850;
    }

    .weeks {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .plan-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .plan-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: var(--level, 50%);
      background: var(--red);
      transition: height .35s ease;
    }

    .final {
      min-height: 78vh;
      display: grid;
      place-items: center;
      text-align: center;
    }

    .final-inner { max-width: 920px; }

    footer {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      padding: 28px clamp(18px, 4vw, 54px);
      color: var(--muted);
      border-top: 1px solid var(--line);
      font-size: 13px;
      text-transform: uppercase;
      font-weight: 850;
    }

    .reveal {
      opacity: 0;
      transform: translateY(34px);
      transition: opacity .75s ease, transform .75s ease;
    }

    .reveal.visible {
      opacity: 1;
      transform: translateY(0);
    }

    @media (max-width: 1020px) {
      .hero,
      .split,
      .hero-visual,
      .profile-photo {
        min-height: 540px;
      }

      .pillars,
      .pillars-12,
      .weeks,
      .plan-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .gallery { grid-template-columns: 1fr 1fr; }
      .nav-links a:not(.primary) { display: none; }
    }

    @media (max-width: 680px) {
      section { padding-top: 72px; padding-bottom: 72px; }
      .hero-visual { min-height: 460px; }
      .portrait-card { inset: 0; }
      .mini-photo { display: none; }
      .pillars,
      .pillars-12,
      .weeks,
      .plan-grid,
      .club-strip,
      .gallery,
      .contact-grid {
        grid-template-columns: 1fr;
      }
      .photo-tile.tall { grid-row: span 1; }
      .club { border-right: 0; border-bottom: 1px solid var(--line); }
      .club:last-child { border-bottom: 0; }
      h1 { font-size: clamp(46px, 15vw, 72px); }
    }
  </style>
</head>
<body>
  <div class="curve-layer" aria-hidden="true">
    <svg viewBox="0 0 800 600" fill="none"><path d="M0 420C120 360 220 520 360 480C520 440 620 280 800 320V600H0V420Z" fill="#b6121b"/><path d="M0 180C160 240 280 80 440 140C580 200 680 360 800 300V0H0V180Z" fill="#f7f7f2"/></svg>
    <svg viewBox="0 0 800 600" fill="none"><path d="M800 120C680 200 560 40 400 100C240 160 120 320 0 260V600H800V120Z" fill="#9a9a95"/><path d="M800 480C640 420 520 560 360 500C200 440 80 300 0 360V0H800V480Z" fill="#b6121b" opacity=".6"/></svg>
    <svg viewBox="0 0 600 400" fill="none"><path d="M0 200Q150 80 300 200T600 200V400H0V200Z" fill="#f7f7f2" opacity=".5"/></svg>
  </div>
  <div class="progress" id="progress"></div>
  <nav>
    <div class="brand"><span class="brand-mark"></span><span>Mentalidad</span></div>
    <div class="nav-links">
      <a href="#persona">Andrés</a>
      <a href="#metodo">Método</a>
      <a href="#programa">12 semanas</a>
      <a href="#precios">Precios</a>
      <a class="primary" href="#contacto">Unirme</a>
    </div>
  </nav>

  <main>
    <section class="hero">
      <div class="orb orb-red" aria-hidden="true"></div>
      <div class="reveal">
        <p class="quote">"No importa cuán talentoso seas, sin la mentalidad adecuada perseguirás el éxito, pero nunca lo alcanzarás"</p>
        <div class="eyebrow">Desarrolla una</div>
        <h1>Mentalidad <span class="thin">de alto</span> <span class="accent">rendimiento</span></h1>
        <p class="lead">Programa promocional de Andrés González: disciplina, resiliencia y hábitos reales para deportistas y personas que quieren elevar su rendimiento bajo presión.</p>
        <div class="actions">
          <a class="button primary" href="#programa">Ver programa</a>
          <a class="button secondary" href="#persona">Conocer a Andrés</a>
        </div>
      </div>

      <div class="hero-visual reveal">
        <div class="portrait-card">
          <img src="/asset/2/0" alt="Imagen deportiva del portafolio Mentalidad 2025" />
          <div class="portrait-label">
            <strong>Andrés González</strong>
            <span>Futbolista profesional por 12 años. Disciplina, presión competitiva y mentalidad aplicada al día a día.</span>
          </div>
        </div>
        <div class="mini-photo">
          <img src="/asset/1/4" alt="Detalle visual del documento Mentalidad 2025" />
        </div>
      </div>
    </section>

    <section class="marquee">
      <div class="marquee-track">
        <span>Un día a la vez</span><span>Te nutres o te envenenas</span><span>Nadie lo hará por ti</span><span>Qué tanto lo quieres</span>
        <span>Un día a la vez</span><span>Te nutres o te envenenas</span><span>Nadie lo hará por ti</span><span>Qué tanto lo quieres</span>
      </div>
    </section>

    <section class="split" id="persona">
      <div class="profile-photo reveal">
        <div class="orb orb-gray" aria-hidden="true"></div>
        <img src="/asset/3/0" alt="Andrés González en material del portafolio" />
      </div>
      <div class="reveal">
        <div class="eyebrow">Acerca de mí</div>
        <h2>Andrés <span class="accent">González</span></h2>
        <div class="bio">
          <p>Futbolista profesional durante 12 años en clubes como América de Cali, Colo Colo de Chile, Independiente Santa Fe, Junior de Barranquilla y la Selección Colombia. Una carrera marcada por triunfos y aprendizajes, pero sobre todo, una reconocida mentalidad de disciplina y resiliencia.</p>
        </div>
        <p class="lead">He conjugado mis experiencias de vida y deportivas para transmitir a mis deportistas los valores, ejercicios y métodos que permitieron entrenar mi mentalidad y enfrentar el estrés y la presión de la alta competencia.</p>
        <div class="club-strip">
          <div class="club">América de Cali</div>
          <div class="club">Colo Colo</div>
          <div class="club">Selección Colombia</div>
        </div>
      </div>
    </section>

    <section id="metodo">
      <div class="section-head reveal">
        <div class="eyebrow">De qué se trata</div>
        <h2>Valores, ejercicios y métodos para entrenar la mente.</h2>
        <p class="lead">La propuesta toma experiencias de vida y deporte para convertirlas en acciones simples que se pueden practicar dentro y fuera de la competencia.</p>
      </div>
      <div class="pillars">
        <article class="pillar reveal"><div class="num">01</div><h3>Un día a la vez</h3><p>Aprende a enfocarte en el paso necesario. Menos ansiedad por el resultado y más presencia en la acción.</p></article>
        <article class="pillar reveal"><div class="num">02</div><h3>Te nutres o te envenenas</h3><p>Tienes el poder y la responsabilidad de elegir tus hábitos, conversaciones, descanso y contenido.</p></article>
        <article class="pillar reveal"><div class="num">03</div><h3>Nadie lo hará por ti</h3><p>Elimina responsables externos y toma control de lo que sí puedes ejecutar hoy.</p></article>
        <article class="pillar reveal"><div class="num">04</div><h3>Qué tanto lo quieres</h3><p>Del dicho al hecho con decisiones medibles, incómodas y sostenidas.</p></article>
      </div>
      <div class="pillars-12" style="margin-top:14px">
        <article class="pillar reveal"><div class="num">05</div><h3>Conviértete en tu mejor versión</h3><p>La tarea es diaria. No esperes el momento perfecto para empezar.</p></article>
        <article class="pillar reveal"><div class="num">06</div><h3>La mariposa no vuelve a ser oruga</h3><p>Vuela, no hay vuelta atrás. El cambio exige compromiso total.</p></article>
        <article class="pillar reveal"><div class="num">07</div><h3>Mantente firme</h3><p>Cuida las pequeñas cosas. La consistencia construye confianza bajo presión.</p></article>
        <article class="pillar reveal"><div class="num">08</div><h3>La siguiente cima</h3><p>Una nueva meta, una más alta. El progreso nunca termina.</p></article>
        <article class="pillar reveal"><div class="num">09</div><h3>Sin cargas innecesarias</h3><p>Tu sueño es importante solo para ti. Suelta lo que no te empuja adelante.</p></article>
        <article class="pillar reveal"><div class="num">10</div><h3>La meta</h3><p>No olvides tu por qué. El motivo sostiene el esfuerzo diario.</p></article>
        <article class="pillar reveal"><div class="num">11</div><h3>El máximo rendimiento</h3><p>Una vida, una oportunidad. Compite con la versión que puedes ser.</p></article>
        <article class="pillar reveal"><div class="num">12</div><h3>Eres luz</h3><p>La responsabilidad de iluminar el camino. Tu ejemplo inspira a quienes te rodean.</p></article>
      </div>
    </section>

    <section>
      <div class="section-head reveal">
        <div class="eyebrow">Imágenes del portafolio</div>
        <h2>Una identidad visual <span class="accent">más fuerte.</span></h2>
        <p class="lead">El documento se convierte en una experiencia web con movimiento, fotografía, bloques editoriales y llamados a la acción.</p>
      </div>
      <div class="gallery">
        <div class="photo-tile tall reveal"><img src="/asset/1/0" alt="Imagen del documento Mentalidad 2025" /><div class="photo-caption">Disciplina</div></div>
        <div class="photo-tile reveal"><img src="/asset/1/2" alt="Imagen deportiva del portafolio" /><div class="photo-caption">Alta competencia</div></div>
        <div class="photo-tile tall reveal"><img src="/asset/4/0" alt="Imagen del plan de trabajo" /><div class="photo-caption">12 semanas</div></div>
        <div class="photo-tile reveal"><img src="/asset/3/2" alt="Detalle visual del portafolio" /><div class="photo-caption">Resiliencia</div></div>
      </div>
    </section>

    <section id="programa">
      <div class="section-head reveal">
        <div class="eyebrow">Cómo lo haremos</div>
        <h2>Plan de trabajo de <span class="accent">doce semanas.</span></h2>
        <p class="lead">Dos sesiones semanales, presenciales o virtuales, para identificar metas, aclarar el camino, fortalecer habilidades y detectar oportunidades de mejora.</p>
      </div>
      <div class="weeks">
        <article class="week reveal"><div class="num">W01-W04</div><h3>Claridad</h3><p>Diagnóstico, metas, hábitos iniciales y una agenda realista para empezar sin fricción.</p></article>
        <article class="week reveal"><div class="num">W05-W08</div><h3>Presión</h3><p>Ejercicios para manejar estrés, competencia interna, disciplina y toma de decisiones.</p></article>
        <article class="week reveal"><div class="num">W09-W12</div><h3>Identidad</h3><p>Consolidación de rutinas, seguimiento de progreso y plan para sostener el rendimiento.</p></article>
      </div>
    </section>

    <section id="app">
      <div class="section-head reveal">
        <div class="eyebrow">Mentorías</div>
        <h2>Acompañamiento teórico-práctico.</h2>
        <p class="lead">Sesiones basadas en potenciar las fortalezas del deportista y nivelar aquellas en que tiene mayor oportunidad de mejora.</p>
      </div>
      <div class="plan-grid reveal">
        <article class="plan-card" style="--level:78%">
          <div class="num">2 sesiones semanales</div>
          <h3>Presencial o virtual</h3>
          <p>Espacios de asesoría para revisar metas, bloqueos, hábitos y decisiones que afectan el rendimiento.</p>
        </article>
        <article class="plan-card" style="--level:64%">
          <div class="num">Ruta individual</div>
          <h3>Claridad de objetivos</h3>
          <p>Identificación del camino, habilidades actuales y oportunidades de mejora dentro y fuera de la competencia.</p>
        </article>
        <article class="plan-card" style="--level:88%">
          <div class="num">Seguimiento</div>
          <h3>Acción medible</h3>
          <p>Retos, reflexiones y compromisos semanales para convertir la mentalidad en comportamiento visible.</p>
        </article>
      </div>
    </section>

    <section id="precios">
      <div class="section-head reveal">
        <div class="eyebrow">Inversión</div>
        <h2>Mentorías con <span class="accent">impacto real.</span></h2>
        <p class="lead">Paquetes diseñados para acompañar el proceso completo de transformación mental en doce semanas.</p>
      </div>
      <div class="pricing-wrap reveal">
        <table class="pricing-table">
          <thead>
            <tr>
              <th>Plan</th>
              <th>Sesiones</th>
              <th>Valor por sesión</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Mentorías</td>
              <td>8 por mes</td>
              <td>USD 120</td>
              <td class="highlight">USD 960</td>
            </tr>
            <tr>
              <td>Plan completo</td>
              <td>24 sesiones</td>
              <td>—</td>
              <td class="highlight">USD 1,880</td>
            </tr>
          </tbody>
        </table>
        <p class="pricing-note">Paquete mínimo a invertir por 8 sesiones. La inversión de 24 sesiones requiere un único pago al iniciar el plan. Los asesorados en Cali pueden realizar sesiones presenciales y entrenamiento físico incluido en el valor.</p>
      </div>
    </section>

    <section class="final" id="contacto">
      <div class="final-inner reveal">
        <div class="eyebrow">Portafolio promocional</div>
        <h2>Desarrolla una mentalidad de alto rendimiento.</h2>
        <p class="lead">Una propuesta para ampliar audiencias hacia un estilo de vida más sano, con mejor desempeño atlético y una mentalidad preparada para la presión.</p>
        <div class="actions" style="justify-content:center">
          <button class="button primary" id="commitButton">Activar reto de hoy</button>
        </div>
        <p id="commitMessage" class="lead" style="margin:22px auto 0; color:var(--muted)"></p>
        <div class="contact-grid">
          <a class="contact-card" href="https://wa.me/573142961072" target="_blank" rel="noopener">
            <span>WhatsApp</span>
            <strong>+57 314 296 1072</strong>
          </a>
          <a class="contact-card" href="mailto:afgr840108@gmail.com">
            <span>Email</span>
            <strong>afgr840108@gmail.com</strong>
          </a>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <span>Andrés González / Mentalidad 2025</span>
    <span>Blanco · Negro · Rojo · Gris</span>
    <span>+57 314 296 1072</span>
  </footer>

  <script>
    const progress = document.getElementById("progress");
    const reveals = document.querySelectorAll(".reveal");

    function updateProgress() {
      const scrollTop = window.scrollY;
      const height = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = `${Math.max(0, Math.min(100, (scrollTop / height) * 100))}%`;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("visible");
      });
    }, { threshold: .14, rootMargin: "0px 0px -40px 0px" });

    reveals.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i * 0.04, 0.32)}s`;
      observer.observe(el);
    });

    window.addEventListener("scroll", updateProgress, { passive: true });
    updateProgress();

    document.querySelectorAll(".hero-visual, .profile-photo").forEach((el) => {
      window.addEventListener("scroll", () => {
        const y = window.scrollY;
        el.style.transform = `translate3d(0, ${y * 0.025}px, 0)`;
      }, { passive: true });
    });

    document.getElementById("commitButton").addEventListener("click", () => {
      const messages = [
        "Reto activado: 20 minutos de movimiento consciente y una meta escrita antes de entrenar.",
        "Reto activado: cumple una acción incómoda hoy sin culpar al entorno.",
        "Reto activado: elige una cosa que te nutre y elimina una que te envenena.",
        "Reto activado: escribe tu por qué y repítelo antes de dormir.",
        "Reto activado: cuida una pequeña cosa que sueles postergar."
      ];
      const msg = messages[Math.floor(Math.random() * messages.length)];
      const target = document.getElementById("commitMessage");
      target.textContent = msg;
      target.style.color = "var(--soft)";
    });
  </script>
</body>
</html>"""


def image_response(page_index: int, image_index: int) -> tuple[bytes, str]:
    if not PDF_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el PDF: {PDF_PATH}")

    reader = PdfReader(str(PDF_PATH))
    if page_index < 0 or page_index >= len(reader.pages):
        raise IndexError("Página fuera de rango")

    images = list(getattr(reader.pages[page_index], "images", []) or [])
    if image_index < 0 or image_index >= len(images):
        raise IndexError("Imagen fuera de rango")

    pil_image = images[image_index].image
    if pil_image.mode not in {"RGB", "L"}:
        pil_image = pil_image.convert("RGB")

    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG", quality=88, optimize=True)
    return buffer.getvalue(), "image/jpeg"


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path in {"/", "/index.html"}:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
            return

        if path.startswith("/asset/"):
            try:
                _, _, page, index = path.split("/", 3)
                data, mime = image_response(int(page) - 1, int(index))
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Cache-Control", "public, max-age=3600")
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Imagen no encontrada".encode("utf-8"))
                return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Pagina no encontrada".encode("utf-8"))

    def log_message(self, format, *args):
        return


def run() -> None:
    if not PDF_PATH.is_file():
        print(f"Advertencia: no se encontró el PDF en {PDF_PATH}")
        print("La página cargará, pero las imágenes del portafolio no estarán disponibles.")

    server = ThreadingHTTPServer((HOST, PORT), AppHandler)
    print(f"Página lista en http://{HOST}:{PORT}")
    print(f"PDF: {PDF_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    run()
