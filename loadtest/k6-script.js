import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://notes-app';
const JSON_PARAMS = { headers: { 'Content-Type': 'application/json' } };

export const options = {
  stages: [
    { duration: '15s', target: 500 },
    { duration: '60s', target: 500 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
  },
  summaryTrendStats: ['avg', 'min', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

export default function () {
  const health = http.get(`${BASE}/health/`, { tags: { name: 'health' } });
  check(health, { 'health 200': (r) => r.status === 200 });

  const title = `load-${__VU}-${__ITER}`;
  const created = http.post(
    `${BASE}/notes`,
    JSON.stringify({ title: title, content: 'created by k6' }),
    { ...JSON_PARAMS, tags: { name: 'notes_create' } }
  );
  const createdOk = check(created, { 'create 201': (r) => r.status === 201 });
  if (!createdOk) {
    sleep(1);
    return;
  }
  const id = created.json('id');

  const one = http.get(`${BASE}/notes/${id}`, { tags: { name: 'notes_get_one' } });
  check(one, {
    'read one 200': (r) => r.status === 200,
    'title matches': (r) => r.json('title') === title,
  });

  const updated = http.put(
    `${BASE}/notes/${id}`,
    JSON.stringify({ title: title, content: 'updated by k6' }),
    { ...JSON_PARAMS, tags: { name: 'notes_update' } }
  );
  check(updated, {
    'update 200': (r) => r.status === 200,
    'content updated': (r) => r.json('content') === 'updated by k6',
  });

  const list = http.get(`${BASE}/notes`, { tags: { name: 'notes_list' } });
  check(list, { 'list 200': (r) => r.status === 200 });

  const deleted = http.del(`${BASE}/notes/${id}`, null, { tags: { name: 'notes_delete' } });
  check(deleted, { 'delete 200': (r) => r.status === 200 });

  const gone = http.get(`${BASE}/notes/${id}`, {
    tags: { name: 'notes_get_deleted' },
    responseCallback: http.expectedStatuses(404),
  });
  check(gone, { 'deleted note is 404': (r) => r.status === 404 });

  sleep(1);
}