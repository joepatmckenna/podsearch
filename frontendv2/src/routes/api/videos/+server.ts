import { RequestHandler } from '@sveltejs/kit';

const URL = 'https://search-ouy3lqvqqq-uc.a.run.app';

export const GET: RequestHandler = async () => {
  return await fetch(`${URL}/videos`);
};
