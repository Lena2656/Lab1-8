import http from 'k6/http'
import { check, sleep } from 'k6'

// Настройки теста
export const options = {
	// Этапы нагрузочного теста
	stages: [
		{ duration: '30s', target: 10 }, // 10 VUs на 30 секунд
		{ duration: '10s', target: 50 }, // 50 VUs на 10 секунд
	],

	// Пороговые значения (thresholds)
	thresholds: {
		// 95% запросов должны завершиться за 500мс
		http_req_duration: ['p(95)<500'],
		// Менее 1% ошибок
		http_req_failed: ['rate<0.01'],
	},

	// Исключения
	noConnectionReuse: false,
}

// Инициализация (выполняется один раз)
export function setup() {
	console.log('Начало нагрузочного тестирования')
	return { baseUrl: 'https://jsonplaceholder.typicode.com' }
}

// Основная функция, выполняемая каждым виртуальным пользователем
export default function (data) {
	// GET-запрос к API
	const response = http.get(`${data.baseUrl}/posts/1`)

	// Проверки ответа
	check(response, {
		'Статус код 200': r => r.status === 200,
		'Время ответа < 500ms': r => r.timings.duration < 500,
		'Заголовок Content-Type присутствует': r =>
			r.headers['Content-Type'] !== undefined,
	})

	// Имитация поведения пользователя (пауза между запросами)
	sleep(1)
}

// Завершающая функция (выполняется после теста)
export function teardown(data) {
	console.log('Завершение нагрузочного тестирования')
}
