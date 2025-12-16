import http from 'k6/http'
import { check } from 'k6'

// Тест 1: 10 VUs на 30 секунд
export let options = {
	vus: 10,
	duration: '30s',
	thresholds: {
		http_req_duration: ['p(95)<1000'],
		http_req_failed: ['rate<0.05'],
	},
}

export default function () {
	const res = http.get('https://httpbin.test.k6.io/get')

	check(res, {
		'is status 200': r => r.status === 200,
		'response time OK': r => r.timings.duration < 1000,
	})
}
