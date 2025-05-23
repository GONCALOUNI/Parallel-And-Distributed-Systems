import http from 'k6/http';
import { check, sleep } from 'k6';
import { group } from 'k6';

export const options = {
  vus: 100,
  duration: '5m',
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const url = `${BASE_URL}/kv`;
  const key = Math.random().toString(36).substring(7);
  const payload = JSON.stringify({ key: key, value: `val_${key}` });
  const params = { headers: { 'Content-Type': 'application/json' } };

  group('PUT /kv', () => {
    let res = http.put(url, payload, params);
    check(res, { 'PUT status is 200': (r) => r.status === 200 });
  });

  group('GET /kv', () => {
    let res = http.get(url + `?key=${key}`);
    check(res, { 'GET status is 200': (r) => r.status === 200 });
  });

  group('DELETE /kv', () => {
    let res = http.del(url + `?key=${key}`);
    check(res, { 'DELETE status is 200': (r) => r.status === 200 });
  });

  sleep(1);
}