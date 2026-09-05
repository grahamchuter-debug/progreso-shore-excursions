/**
 * Progreso Shore Excursion — Workers Assets entry.
 * www → apex (one hop); .html → extensionless (one hop); combined in one hop when both apply.
 */
const APEX_HOST = 'progresoshoreexcursion.com';

function stripHtmlPath(pathname) {
  if (!pathname.toLowerCase().endsWith('.html')) return pathname;
  let path = pathname.slice(0, -5);
  if (path.toLowerCase().endsWith('/index')) path = path.slice(0, -6);
  if (path === '' || path === '/index') path = '/';
  return path || '/';
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();
    const isWww = host === `www.${APEX_HOST}`;
    const hasHtml = url.pathname.toLowerCase().endsWith('.html');

    if (isWww || hasHtml) {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = 'https:';
      if (hasHtml) dest.pathname = stripHtmlPath(url.pathname);
      else if (isWww) dest.pathname = url.pathname || '/';
      if (dest.toString() !== url.toString()) {
        return Response.redirect(dest.toString(), 301);
      }
    }

    const assetResponse = await env.ASSETS.fetch(request);

    if (assetResponse.status === 404) {
      const notFound = await env.ASSETS.fetch(new URL('/404.html', url.origin));
      return new Response(notFound.body, {
        status: 404,
        headers: {
          'content-type': 'text/html; charset=utf-8',
          'cache-control': 'no-store',
        },
      });
    }

    return assetResponse;
  },
};
