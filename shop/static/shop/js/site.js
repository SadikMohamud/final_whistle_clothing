const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursorRing');
const langToggle = document.getElementById('langToggle');
const themeToggle = document.getElementById('themeToggle');
let themeSwitchInput = null;
const root = document.documentElement;
const body = document.body;

const translations = {
  nl: {
    page_title: 'Final Whistle Clothing',
    brand_logo: 'Final<span>.</span>Whistle',
    campaign_mark: 'FW',
    col_mark_top: 'TOP',
    col_mark_bas: 'BAS',
    col_mark_acc: 'ACC',
    social_ig: 'IG',
    social_tt: 'TT',
    social_yt: 'YT',
    ticker_shipping: 'Gratis verzending vanaf €100',
    ticker_collection: 'Nieuwe Collectie SS26',
    ticker_delivery: 'Bestel voor 22:00, morgen in huis',
    ticker_streetwear: 'Authentiek Dutch Streetwear',
    ticker_drop: 'Limited Drop - Final Whistle Classics',
    nav_shop: 'Shop',
    nav_collections: 'Collecties',
    nav_drops: 'Drops',
    nav_search: 'Zoeken',
    nav_login: 'Log in',
    nav_logout: 'Logout',
    nav_bag: 'Tas',
    hero_eyebrow: 'SS26 - Nieuwe Collectie',
    hero_headline: 'Gebouwd Voor<br><em>De Straat</em><br>Gedragen Erbuiten',
    hero_stat_items: 'Unieke Items',
    hero_stat_season: 'Seizoen',
    cat_tshirts: 'T-Shirts',
    cat_hoodies: 'Hoodies',
    cat_tracksuits: 'Tracksuits',
    cat_jackets: 'Jackets',
    cat_shorts: 'Shorts',
    cat_caps: 'Caps',
    cat_accessories: 'Accessoires',
    cat_sale: 'Sale',
    cta_shop_now: 'Shop Nu',
    cta_view_collection: 'Bekijk Collectie',
    new_arrivals: 'Nieuwe <span>Binnenkomers</span>',
    view_all: 'Bekijk alles ->',
    product_image: 'Product Afbeelding',
    shopify_configure: 'Configureer Shopify API-gegevens',
    products_none: 'Geen producten geladen',
    products_env: 'Controleer .env instellingen',
    campaign_circle: 'Geboren Uit<br><em>Street Culture</em>',
    campaign_story: 'Ons Verhaal',
    campaign_heading: 'Street Meets<br>Stadium',
    campaign_body: 'Final Whistle Clothing is geboren vanuit een liefde voor moderne Nederlandse street culture. Van de stad tot de straat - onze kleding is gemaakt om elke dag te dragen.',
    campaign_stat_founded: 'Opgericht',
    campaign_stat_community: 'Community',
    campaign_stat_madein: 'Made in',
    campaign_cta: 'Ons Verhaal ->',
    shop_category: 'Shop Per <span>Categorie</span>',
    all_collections: 'Alle collecties ->',
    col_tops_name: 'Tops &<br>Sweaters',
    col_tops_desc: 'T-shirts, hoodies, longsleeves & meer',
    col_bottoms_name: 'Bottoms &<br>Shorts',
    col_bottoms_desc: 'Tracksuits, shorts & joggers',
    col_accessories_name: 'Caps &<br>Accessoires',
    col_accessories_desc: 'Headwear, tassen & essentials',
    collection_shop_now: 'Shop Nu ->',
    trust_shipping_title: 'Gratis Verzending',
    trust_shipping_desc: 'Op alle bestellingen boven €100 - snel en betrouwbaar bezorgd.',
    trust_order_title: 'Bestel voor 22:00',
    trust_order_desc: 'Volgende werkdag al in huis - standaard voor alle Nederlandse bestellingen.',
    trust_return_title: '30 Dagen Retour',
    trust_return_desc: 'Niet tevreden? Ruil of retourneer moeiteloos binnen 30 dagen.',
    trust_payment_title: 'Veilig Betalen',
    trust_payment_desc: 'iDEAL, Klarna, creditcard en meer - 100% veilig en versleuteld.',
    newsletter_heading: 'Blijf in<br><span>De Game</span>',
    newsletter_sub: 'Meld je aan voor vroeg toegang tot drops, exclusieve aanbiedingen & inside nieuws.',
    newsletter_placeholder: 'Jouw e-mailadres',
    newsletter_button: 'Aanmelden',
    footer_tagline: 'Dutch streetwear. Geboren vanuit liefde voor stijl - gedragen op straat.',
    footer_shop: 'Shop',
    footer_shop_new: 'Nieuw',
    footer_shop_tshirts: 'T-Shirts',
    footer_shop_hoodies: 'Hoodies',
    footer_shop_jackets: 'Jackets',
    footer_shop_sale: 'Sale',
    footer_info: 'Info',
    footer_info_about: 'Over Ons',
    footer_info_shipping: 'Verzending',
    footer_info_returns: 'Retourneren',
    footer_info_contact: 'Contact',
    footer_info_faq: 'FAQ',
    footer_follow: 'Volg Ons',
    footer_follow_instagram: 'Instagram',
    footer_follow_tiktok: 'TikTok',
    footer_follow_youtube: 'YouTube',
    footer_follow_newsletter: 'Newsletter',
    footer_copy: '© 2025 Final Whistle Clothing. Alle rechten voorbehouden.',
    auth_login_title: 'Inloggen',
    auth_login_sub: 'Log in om producten te bekijken en door te gaan naar Shopify checkout.',
    auth_email_label: 'E-mail',
    auth_password_label: 'Wachtwoord',
    auth_forgot_password: 'Wachtwoord vergeten?',
    auth_login_button: 'Inloggen',
    auth_signup_link: 'Aanmelden',
    auth_signup_title: 'Aanmelden',
    auth_signup_sub: 'Maak je account aan om te browsen en te bestellen met Shopify checkout.',
    auth_first_name_label: 'Voornaam',
    auth_last_name_label: 'Achternaam',
    auth_password_help: 'Moet minimaal 8 tekens hebben, 1 speciaal teken en 3 niet-opeenvolgende cijfers.',
    auth_confirm_password_label: 'Bevestig wachtwoord',
    auth_signup_button: 'Account aanmaken',
    auth_back_login: 'Terug naar inloggen',
    auth_or_continue: 'of',
    auth_google_button: 'Doorgaan met Google',
    auth_confirm_title: 'Bevestig E-mail',
    auth_confirm_sub: 'Je account is succesvol aangemaakt. Controleer je inbox en bevestig je e-mailadres voordat je inlogt.',
    auth_confirm_login_cta: 'Ga naar inloggen',
    auth_confirm_home_cta: 'Terug naar home',
    auth_login_page_title: 'Inloggen | Final Whistle Clothing',
    auth_signup_page_title: 'Aanmelden | Final Whistle Clothing',
    theme_dark: 'Donker',
    theme_light: 'Licht'
  },
  en: {
    page_title: 'Final Whistle Clothing',
    brand_logo: 'Final<span>.</span>Whistle',
    campaign_mark: 'FW',
    col_mark_top: 'TOP',
    col_mark_bas: 'BAS',
    col_mark_acc: 'ACC',
    social_ig: 'IG',
    social_tt: 'TT',
    social_yt: 'YT',
    ticker_shipping: 'Free shipping from €100',
    ticker_collection: 'New SS26 Collection',
    ticker_delivery: 'Order before 22:00, delivered tomorrow',
    ticker_streetwear: 'Authentic Dutch Streetwear',
    ticker_drop: 'Limited Drop - Final Whistle Classics',
    nav_shop: 'Shop',
    nav_collections: 'Collections',
    nav_drops: 'Drops',
    nav_search: 'Search',
    nav_login: 'Log in',
    nav_logout: 'Logout',
    nav_bag: 'Bag',
    hero_eyebrow: 'SS26 - New Collection',
    hero_headline: 'Built For<br><em>The Street</em><br>Worn Beyond',
    hero_stat_items: 'Unique Items',
    hero_stat_season: 'Season',
    cat_tshirts: 'T-Shirts',
    cat_hoodies: 'Hoodies',
    cat_tracksuits: 'Tracksuits',
    cat_jackets: 'Jackets',
    cat_shorts: 'Shorts',
    cat_caps: 'Caps',
    cat_accessories: 'Accessories',
    cat_sale: 'Sale',
    cta_shop_now: 'Shop Now',
    cta_view_collection: 'View Collection',
    new_arrivals: 'New <span>Arrivals</span>',
    view_all: 'View all ->',
    product_image: 'Product Image',
    shopify_configure: 'Configure Shopify API credentials',
    products_none: 'No products loaded',
    products_env: 'Check .env settings',
    campaign_circle: 'Born From<br><em>Street Culture</em>',
    campaign_story: 'Our Story',
    campaign_heading: 'Street Meets<br>Stadium',
    campaign_body: 'Final Whistle Clothing was born from a love for modern Dutch street culture. From the city to the street - our clothing is made for everyday wear.',
    campaign_stat_founded: 'Founded',
    campaign_stat_community: 'Community',
    campaign_stat_madein: 'Made in',
    campaign_cta: 'Our Story ->',
    shop_category: 'Shop By <span>Category</span>',
    all_collections: 'All collections ->',
    col_tops_name: 'Tops &<br>Sweaters',
    col_tops_desc: 'T-shirts, hoodies, long sleeves & more',
    col_bottoms_name: 'Bottoms &<br>Shorts',
    col_bottoms_desc: 'Tracksuits, shorts & joggers',
    col_accessories_name: 'Caps &<br>Accessories',
    col_accessories_desc: 'Headwear, bags & essentials',
    collection_shop_now: 'Shop Now ->',
    trust_shipping_title: 'Free Shipping',
    trust_shipping_desc: 'On all orders above €100 - delivered fast and reliably.',
    trust_order_title: 'Order Before 22:00',
    trust_order_desc: 'Delivered the next business day - standard for all Dutch orders.',
    trust_return_title: '30-Day Returns',
    trust_return_desc: 'Not satisfied? Exchange or return within 30 days with ease.',
    trust_payment_title: 'Secure Payments',
    trust_payment_desc: 'iDEAL, Klarna, credit card and more - 100% secure and encrypted.',
    newsletter_heading: 'Stay in<br><span>The Game</span>',
    newsletter_sub: 'Sign up for early access to drops, exclusive offers and insider news.',
    newsletter_placeholder: 'Your email address',
    newsletter_button: 'Subscribe',
    footer_tagline: 'Dutch streetwear. Born from love for style - worn on the streets.',
    footer_shop: 'Shop',
    footer_shop_new: 'New',
    footer_shop_tshirts: 'T-Shirts',
    footer_shop_hoodies: 'Hoodies',
    footer_shop_jackets: 'Jackets',
    footer_shop_sale: 'Sale',
    footer_info: 'Info',
    footer_info_about: 'About Us',
    footer_info_shipping: 'Shipping',
    footer_info_returns: 'Returns',
    footer_info_contact: 'Contact',
    footer_info_faq: 'FAQ',
    footer_follow: 'Follow Us',
    footer_follow_instagram: 'Instagram',
    footer_follow_tiktok: 'TikTok',
    footer_follow_youtube: 'YouTube',
    footer_follow_newsletter: 'Newsletter',
    footer_copy: '© 2025 Final Whistle Clothing. All rights reserved.',
    auth_login_title: 'Login',
    auth_login_sub: 'Sign in to browse products and continue to Shopify checkout.',
    auth_email_label: 'Email',
    auth_password_label: 'Password',
    auth_forgot_password: 'Forgot password?',
    auth_login_button: 'Login',
    auth_signup_link: 'Sign Up',
    auth_signup_title: 'Sign Up',
    auth_signup_sub: 'Create your account to browse and order with Shopify checkout.',
    auth_first_name_label: 'First Name',
    auth_last_name_label: 'Last Name',
    auth_password_help: 'Must be at least 8 characters, include 1 special character, and 3 numbers.',
    auth_confirm_password_label: 'Confirm Password',
    auth_signup_button: 'Create Account',
    auth_back_login: 'Back to Login',
    auth_or_continue: 'or',
    auth_google_button: 'Continue with Google',
    auth_confirm_title: 'Confirm Email',
    auth_confirm_sub: 'Your account was created successfully. Please check your inbox and confirm your email address before logging in.',
    auth_confirm_login_cta: 'Go to Login',
    auth_confirm_home_cta: 'Back Home',
    auth_login_page_title: 'Login | Final Whistle Clothing',
    auth_signup_page_title: 'Sign Up | Final Whistle Clothing',
    theme_dark: 'Dark',
    theme_light: 'Light'
  }
};

function applyLanguage(lang) {
  const safeLang = translations[lang] ? lang : 'en';
  root.setAttribute('lang', safeLang);
  root.setAttribute('data-lang', safeLang);

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    const value = translations[safeLang][key];
    if (value) {
      el.innerHTML = value;
    }
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const key = el.getAttribute('data-i18n-placeholder');
    const value = translations[safeLang][key];
    if (value) {
      el.setAttribute('placeholder', value);
    }
  });

  if (langToggle) {
    langToggle.textContent = safeLang.toUpperCase();
  }

  localStorage.setItem('fwcLang', safeLang);
  syncThemeToggleState();
}

function applyTheme(theme) {
  const safeTheme = theme === 'light' ? 'light' : 'dark';
  body.setAttribute('data-theme', safeTheme);
  localStorage.setItem('fwcTheme', safeTheme);
  syncThemeToggleState();
}

function syncThemeToggleState() {
  if (!themeSwitchInput) {
    return;
  }

  const theme = body.getAttribute('data-theme') || 'dark';
  themeSwitchInput.checked = theme !== 'light';
}

function renderThemeToggleSwitch() {
  if (!themeToggle || themeToggle.classList.contains('switch')) {
    return;
  }

  const currentTheme = localStorage.getItem('fwcTheme') || 'dark';
  const switchLabel = document.createElement('label');
  switchLabel.className = 'switch';
  switchLabel.setAttribute('aria-label', 'Toggle theme');
  switchLabel.innerHTML = `
    <input id="themeSwitch" type="checkbox" ${currentTheme === 'dark' ? 'checked' : ''} aria-label="Toggle theme">
    <div class="slider round">
      <div class="sun-moon">
        <svg id="moon-dot-1" class="moon-dot" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="moon-dot-2" class="moon-dot" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="moon-dot-3" class="moon-dot" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="light-ray-1" class="light-ray" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="light-ray-2" class="light-ray" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="light-ray-3" class="light-ray" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="cloud-1" class="cloud-dark" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="cloud-2" class="cloud-dark" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="cloud-3" class="cloud-dark" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="cloud-4" class="cloud-light" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="cloud-5" class="cloud-light" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
        <svg id="cloud-6" class="cloud-light" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50"></circle></svg>
      </div>
      <div class="stars">
        <svg id="star-1" class="star" viewBox="0 0 20 20"><path d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"></path></svg>
        <svg id="star-2" class="star" viewBox="0 0 20 20"><path d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"></path></svg>
        <svg id="star-3" class="star" viewBox="0 0 20 20"><path d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"></path></svg>
        <svg id="star-4" class="star" viewBox="0 0 20 20"><path d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"></path></svg>
      </div>
    </div>`;

  themeToggle.replaceWith(switchLabel);
  themeSwitchInput = switchLabel.querySelector('#themeSwitch');

  themeSwitchInput.addEventListener('change', () => {
    applyTheme(themeSwitchInput.checked ? 'dark' : 'light');
  });

  syncThemeToggleState();
}

if (langToggle) {
  langToggle.addEventListener('click', () => {
    const current = root.getAttribute('data-lang') || 'nl';
    applyLanguage(current === 'nl' ? 'en' : 'nl');
  });
}

if (themeToggle) {
  renderThemeToggleSwitch();
}

const initialTheme = localStorage.getItem('fwcTheme') || 'dark';
const initialLang = localStorage.getItem('fwcLang') || 'en';
applyTheme(initialTheme);
applyLanguage(initialLang);

function ensureGlobalBackButton() {
  // Don't show back button on homepage
  if (window.location.pathname === '/') {
    return;
  }

  if (document.querySelector('.global-back-btn')) {
    return;
  }

  // Always create and show the back button on all pages except homepage
  const backBtn = document.createElement('a');
  backBtn.className = 'global-back-btn';
  backBtn.href = '#';
  backBtn.innerHTML = '<span class="arrow">&larr;</span><span>Back</span>';
  backBtn.setAttribute('aria-label', 'Go back');

  // Inline style guarantees consistent rendering even if a page overrides link styles.
  backBtn.style.position = 'fixed';
  backBtn.style.top = '16px';
  backBtn.style.left = '16px';
  backBtn.style.zIndex = '1001';
  backBtn.style.display = 'inline-flex';
  backBtn.style.alignItems = 'center';
  backBtn.style.gap = '8px';
  backBtn.style.padding = '8px 12px';
  backBtn.style.borderRadius = '999px';
  backBtn.style.border = '1px solid var(--volt)';
  backBtn.style.color = 'var(--volt)';
  backBtn.style.background = 'rgba(8, 8, 8, 0.42)';
  backBtn.style.backdropFilter = 'blur(10px)';
  backBtn.style.fontFamily = 'var(--font-display)';
  backBtn.style.fontSize = '11px';
  backBtn.style.fontWeight = '700';
  backBtn.style.letterSpacing = '0.1em';
  backBtn.style.textTransform = 'uppercase';
  backBtn.style.textDecoration = 'none';
  backBtn.style.lineHeight = '1';
  backBtn.style.cursor = 'pointer';

  backBtn.addEventListener('click', (event) => {
    event.preventDefault();
    // If there's history, go back; otherwise go to home
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = '/';
    }
  });

  document.body.appendChild(backBtn);
}

ensureGlobalBackButton();

const canUseCustomCursor = Boolean(
  cursor &&
  ring &&
  window.matchMedia('(hover: hover) and (pointer: fine)').matches
);

if (canUseCustomCursor) {
  body.classList.add('custom-cursor-enabled');

  let mx = window.innerWidth * 0.5;
  let my = window.innerHeight * 0.5;
  let rx = mx;
  let ry = my;

  cursor.style.left = mx + 'px';
  cursor.style.top = my + 'px';
  ring.style.left = rx + 'px';
  ring.style.top = ry + 'px';

  document.addEventListener('mousemove', (e) => {
    mx = e.clientX;
    my = e.clientY;
    cursor.style.left = mx + 'px';
    cursor.style.top = my + 'px';
  });

  function animateRing() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    ring.style.left = rx + 'px';
    ring.style.top = ry + 'px';
    requestAnimationFrame(animateRing);
  }

  animateRing();

  document.querySelectorAll('a, button, .product-card, .collection-card').forEach((el) => {
    el.addEventListener('mouseenter', () => {
      cursor.style.width = '16px';
      cursor.style.height = '16px';
      ring.style.width = '56px';
      ring.style.height = '56px';
      ring.style.borderColor = 'var(--volt)';
    });

    el.addEventListener('mouseleave', () => {
      cursor.style.width = '10px';
      cursor.style.height = '10px';
      ring.style.width = '36px';
      ring.style.height = '36px';
      ring.style.borderColor = 'var(--volt)';
    });
  });
} else {
  body.classList.remove('custom-cursor-enabled');
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-up').forEach((el) => observer.observe(el));

function initParallax() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touchLike = window.matchMedia('(hover: none), (pointer: coarse)').matches;

  if (reduceMotion || touchLike) {
    return;
  }

  const roots = Array.from(document.querySelectorAll('[data-parallax-root]'));
  if (!roots.length) {
    return;
  }

  const allLayerItems = [];

  function getParallaxProfile(rootNode) {
    if (rootNode.classList.contains('hero')) {
      return {
        scrollStrength: 1.28,
        pointerStrength: 1.14,
        rotateStrength: 1.25,
        lerp: 0.1,
        scaleBoost: 0.03
      };
    }

    if (rootNode.classList.contains('campaign')) {
      return {
        scrollStrength: 0.92,
        pointerStrength: 0.84,
        rotateStrength: 0.92,
        lerp: 0.09,
        scaleBoost: 0.02
      };
    }

    if (rootNode.classList.contains('collection-card')) {
      return {
        scrollStrength: 0.66,
        pointerStrength: 0.62,
        rotateStrength: 0.7,
        lerp: 0.08,
        scaleBoost: 0.015
      };
    }

    return {
      scrollStrength: 0.86,
      pointerStrength: 0.78,
      rotateStrength: 0.84,
      lerp: 0.09,
      scaleBoost: 0.018
    };
  }

  roots.forEach((rootNode) => {
    const profile = getParallaxProfile(rootNode);
    const localLayers = Array.from(rootNode.querySelectorAll('.parallax-layer'));
    localLayers.forEach((layerNode) => {
      const speed = Number.parseFloat(layerNode.dataset.parallaxSpeed || '0');
      const pointer = Number.parseFloat(layerNode.dataset.parallaxPointer || '0');
      allLayerItems.push({
        root: rootNode,
        node: layerNode,
        speed,
        pointer,
        profile,
        tx: 0,
        ty: 0,
        rz: 0,
        sx: 1,
        sy: 1
      });
    });
  });

  if (!allLayerItems.length) {
    return;
  }

  const state = {
    mx: window.innerWidth * 0.5,
    my: window.innerHeight * 0.5,
    lx: window.innerWidth * 0.5,
    ly: window.innerHeight * 0.5,
    raf: null,
    active: false
  };

  function clamp(value, min, max) {
    return Math.max(min, Math.min(value, max));
  }

  function remap(value, inMin, inMax, outMin, outMax) {
    if (inMin === inMax) {
      return outMin;
    }
    const t = (value - inMin) / (inMax - inMin);
    return outMin + (outMax - outMin) * t;
  }

  function viewportScale() {
    const w = window.innerWidth;
    if (w >= 1440) {
      return 1;
    }
    if (w >= 1100) {
      return 0.88;
    }
    if (w >= 768) {
      return 0.72;
    }
    return 0.6;
  }

  function updateParallax() {
    const vh = window.innerHeight;
    const vw = window.innerWidth;
    const scale = viewportScale();

    state.lx += (state.mx - state.lx) * 0.085;
    state.ly += (state.my - state.ly) * 0.085;

    const px = clamp(remap(state.lx, 0, Math.max(vw, 1), -1, 1), -1, 1);
    const py = clamp(remap(state.ly, 0, Math.max(vh, 1), -1, 1), -1, 1);

    allLayerItems.forEach((item) => {
      const rootRect = item.root.getBoundingClientRect();
      const rootCenter = rootRect.top + (rootRect.height * 0.5);
      const progress = clamp(remap(rootCenter, vh * 1.35, -vh * 0.35, -1, 1), -1, 1);

      const yFromScroll = progress * item.speed * 170 * scale * item.profile.scrollStrength;
      const xFromPointer = px * item.pointer * 22 * scale * item.profile.pointerStrength;
      const yFromPointer = py * item.pointer * 18 * scale * item.profile.pointerStrength;
      const rotateZ = px * item.pointer * 2.2 * item.profile.rotateStrength;

      const targetTx = xFromPointer;
      const targetTy = yFromScroll + yFromPointer;
      const targetRz = rotateZ;
      const targetSx = 1 + (Math.abs(item.speed) * item.profile.scaleBoost);
      const targetSy = 1 + (Math.abs(item.speed) * item.profile.scaleBoost);

      item.tx += (targetTx - item.tx) * item.profile.lerp;
      item.ty += (targetTy - item.ty) * item.profile.lerp;
      item.rz += (targetRz - item.rz) * (item.profile.lerp * 0.9);
      item.sx += (targetSx - item.sx) * 0.08;
      item.sy += (targetSy - item.sy) * 0.08;

      item.node.style.setProperty('--parallax-x', `${item.tx.toFixed(2)}px`);
      item.node.style.setProperty('--parallax-y', `${item.ty.toFixed(2)}px`);
      item.node.style.setProperty('--parallax-rz', `${item.rz.toFixed(2)}deg`);
      item.node.style.setProperty('--parallax-sx', item.sx.toFixed(4));
      item.node.style.setProperty('--parallax-sy', item.sy.toFixed(4));
    });

    state.raf = requestAnimationFrame(updateParallax);
  }

  function onPointerMove(event) {
    state.mx = event.clientX;
    state.my = event.clientY;
    if (!state.active) {
      state.active = true;
    }
  }

  window.addEventListener('mousemove', onPointerMove, { passive: true });
  window.addEventListener('touchmove', (event) => {
    if (event.touches && event.touches[0]) {
      state.mx = event.touches[0].clientX;
      state.my = event.touches[0].clientY;
    }
  }, { passive: true });

  window.addEventListener('scroll', () => {
    if (!state.active) {
      state.active = true;
    }
  }, { passive: true });

  window.addEventListener('resize', () => {
    state.mx = window.innerWidth * 0.5;
    state.my = window.innerHeight * 0.5;
  }, { passive: true });

  state.raf = requestAnimationFrame(updateParallax);
}

initParallax();

function initScrollBlur() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) {
  return;
  }

  const selector = [
    '.hero-eyebrow',
    '.hero-headline',
    '.hero-ctas',
    '.section-header',
    '.product-card',
    '.campaign-eyebrow',
    '.campaign-heading',
    '.campaign-body',
    '.stat-item',
    '.collection-card',
    '.ed-item',
    '.newsletter-heading',
    '.newsletter-sub',
    '.footer-top > div',
    '.footer-bottom'
  ].join(',');

  const targets = Array.from(document.querySelectorAll(selector));
  if (!targets.length) {
    return;
  }

  targets.forEach((node) => node.classList.add('scroll-blur-target'));

  let rafId = null;

  function clamp(value, min, max) {
    return Math.max(min, Math.min(value, max));
  }

  function getBlurProfile(node) {
    if (node.matches('.hero-headline, .campaign-heading, .newsletter-heading, .section-header')) {
      return {
        start: 0.24,
        range: 0.5,
        maxBlur: 10.5,
        fade: 0.58,
        lift: 26,
        scaleDrop: 0.032
      };
    }

    if (node.matches('.product-card, .collection-card, .ed-item')) {
      return {
        start: 0.2,
        range: 0.44,
        maxBlur: 7,
        fade: 0.42,
        lift: 17,
        scaleDrop: 0.02
      };
    }

    if (node.matches('.footer-top > div, .footer-bottom')) {
      return {
        start: 0.24,
        range: 0.5,
        maxBlur: 6.5,
        fade: 0.35,
        lift: 14,
        scaleDrop: 0.016
      };
    }

    return {
      start: 0.22,
      range: 0.48,
      maxBlur: 8.2,
      fade: 0.5,
      lift: 20,
      scaleDrop: 0.024
    };
  }

  function render() {
    const vh = window.innerHeight;
    const widthScale = window.innerWidth >= 1280 ? 1 : window.innerWidth >= 900 ? 0.9 : 0.78;

    targets.forEach((node) => {
      const p = getBlurProfile(node);
      const rect = node.getBoundingClientRect();
      const center = rect.top + (rect.height * 0.5);
      const start = vh * p.start;
      const range = vh * p.range;

      const progress = clamp((start - center) / range, 0, 1);
      const blur = progress * p.maxBlur * widthScale;
      const opacity = 1 - (progress * p.fade);
      const y = progress * (-p.lift * widthScale);
      const scale = 1 - (progress * p.scaleDrop);

      node.style.setProperty('--blur-amount', `${blur.toFixed(2)}px`);
      node.style.setProperty('--blur-opacity', opacity.toFixed(3));
      node.style.setProperty('--blur-y', `${y.toFixed(2)}px`);
      node.style.setProperty('--blur-scale', scale.toFixed(4));
    });

    rafId = null;
  }

  function queueRender() {
    if (rafId !== null) {
      return;
    }
    rafId = requestAnimationFrame(render);
  }

  window.addEventListener('scroll', queueRender, { passive: true });
  window.addEventListener('resize', queueRender, { passive: true });

  queueRender();
}

initScrollBlur();