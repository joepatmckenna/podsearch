import { RequestHandler } from '@sveltejs/kit';

const URL = 'https://search-ouy3lqvqqq-uc.a.run.app';

export const GET: RequestHandler = async () => {
  return await fetch(URL);
};

export const POST: RequestHandler = async ({ request }) => {
  const { query } = await request.json();
  return await fetch(`${URL}/search?` + new URLSearchParams({ query: query }));
};
