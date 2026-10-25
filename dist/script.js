const menu = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
const header = document.querySelector('.site-header');
function closeMenu() {
  menu.setAttribute('aria-expanded', 'false');
  menu.textContent = 'Menu';
  navigation.classList.remove('is-open');
  header.classList.remove('menu-open');
}
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? 'Close' : 'Menu';
  navigation.classList.toggle('is-open', open);
  header.classList.toggle('menu-open', open);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
function onScroll() { header.classList.toggle('is-scrolled', window.scrollY > 24); }
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();
const dialog = document.querySelector('#artwork-dialog');
let galleryPhotos = [];
let galleryIndex = 0;
function showGalleryPhoto(index) {
  galleryIndex = (index + galleryPhotos.length) % galleryPhotos.length;
  const photo = galleryPhotos[galleryIndex];
  const image = document.createElement('img');
  image.src = photo.src;
  image.alt = photo.alt;
  image.width = photo.width;
  image.height = photo.height;
  document.querySelector('#dialog-art').replaceChildren(image);
  document.querySelector('.dialog-navigation').hidden = galleryPhotos.length < 2;
  document.querySelector('#photo-count').textContent = `${galleryIndex + 1} / ${galleryPhotos.length}`;
}
document.querySelectorAll('[data-work]').forEach(button => button.addEventListener('click', () => {
  const entry = button.closest('.work-item');
  galleryPhotos = JSON.parse(entry.dataset.photos);
  showGalleryPhoto(Number(button.dataset.photoIndex || 0));
  document.querySelector('#dialog-title').textContent = entry.querySelector('h2').textContent;
  document.querySelector('.dialog-copy>.eyebrow').textContent = 'Becoming, in Layers / 2026';
  document.querySelector('#dialog-description').replaceChildren(entry.querySelector('.artwork-description').cloneNode(true));
  dialog.showModal();
  document.body.classList.add('dialog-open');
}));
document.querySelectorAll('[data-archive]').forEach(button => button.addEventListener('click', () => {
  const entry = button.closest('.archive-card');
  const image = button.querySelector('img');
  galleryPhotos = [{ src: image.getAttribute('src'), alt: image.alt, width: image.width, height: image.height }];
  showGalleryPhoto(0);
  document.querySelector('.dialog-copy>.eyebrow').textContent = 'Archive / Earlier work';
  document.querySelector('#dialog-title').textContent = entry.querySelector('h3').textContent;
  document.querySelector('#dialog-description').replaceChildren(entry.querySelector('.archive-description').cloneNode(true));
  dialog.showModal();
  document.body.classList.add('dialog-open');
}));
document.querySelector('#previous-photo').addEventListener('click', () => showGalleryPhoto(galleryIndex - 1));
document.querySelector('#next-photo').addEventListener('click', () => showGalleryPhoto(galleryIndex + 1));
dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showGalleryPhoto(galleryIndex + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => document.body.classList.remove('dialog-open'));
dialog.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
});
document.querySelector('#year').textContent = new Date().getFullYear();

const contactForm = document.querySelector('#contact-form');
if (contactForm?.elements.namedItem('access_key').value.trim()) {
  document.querySelector('#contact-form-note').textContent = 'Send an enquiry directly from this website.';
}
contactForm?.addEventListener('submit', async event => {
  event.preventDefault();
  if (contactForm.getAttribute('aria-busy') === 'true') return;
  const name = contactForm.elements.namedItem('name');
  const enquiry = contactForm.elements.namedItem('message');
  name.value = name.value.trim();
  enquiry.value = enquiry.value.trim();
  if (!contactForm.reportValidity()) return;
  const status = document.querySelector('#contact-form-status');
  if (!contactForm.elements.namedItem('access_key').value.trim()) {
    status.textContent = 'Online enquiries are not available yet. Please email or call Koketso using the details beside this form.';
    return;
  }
  const button = contactForm.querySelector('button[type="submit"]');
  const values = Object.fromEntries(new FormData(contactForm));
  contactForm.setAttribute('aria-busy', 'true');
  button.disabled = true;
  button.textContent = 'Sending…';
  status.textContent = 'Sending your enquiry…';
  try {
    const response = await fetch(contactForm.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(values),
      signal: AbortSignal.timeout(18000),
    });
    if (!response.headers.get('content-type')?.includes('application/json')) {
      throw new Error('The enquiry form is unavailable here. Please contact Koketso using the email address or phone number beside it.');
    }
    const result = await response.json();
    if (!response.ok || result.success !== true) {
      throw new Error('Your enquiry could not be sent. Please try again or contact Koketso directly.');
    }
    status.textContent = 'Thank you. Your enquiry has been sent to Koketso.';
    contactForm.reset();
  } catch (error) {
    status.textContent = error.name === 'TimeoutError' || error.name === 'TypeError'
      ? 'We could not confirm your submission. Your message is still here; please try again or contact Koketso directly.'
      : error.message;
  } finally {
    contactForm.removeAttribute('aria-busy');
    button.disabled = false;
    button.textContent = 'Submit ↗';
  }
});
