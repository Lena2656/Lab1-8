// Хранение задач
let tasks = []
let currentFilter = 'all'

// Загрузка задач при старте
window.onload = function () {
	loadTasks()
	updateStats()
}

// Добавление задачи
function addTask() {
	const input = document.getElementById('taskInput')
	const text = input.value.trim()

	if (text === '') {
		alert('Введите текст задачи!')
		return
	}

	const task = {
		id: Date.now(), // уникальный ID
		text: text,
		completed: false,
		createdAt: new Date(),
	}

	tasks.push(task)
	saveTasks()
	renderTasks()
	updateStats()

	// Очищаем поле ввода
	input.value = ''
	input.focus()
}

// Отображение задач
function renderTasks() {
	const taskList = document.getElementById('taskList')

	// Фильтрация задач
	let filteredTasks
	switch (currentFilter) {
		case 'active':
			filteredTasks = tasks.filter(task => !task.completed)
			break
		case 'completed':
			filteredTasks = tasks.filter(task => task.completed)
			break
		default:
			filteredTasks = tasks
	}

	// Если нет задач
	if (filteredTasks.length === 0) {
		let message = 'Пока нет задач. Добавьте первую!'
		if (currentFilter === 'active') message = 'Нет активных задач'
		if (currentFilter === 'completed') message = 'Нет выполненных задач'

		taskList.innerHTML = `<div class="empty">${message}</div>`
		return
	}

	// Создаем HTML для каждой задачи
	taskList.innerHTML = filteredTasks
		.map(
			task => `
        <div class="task ${task.completed ? 'completed' : ''}" data-id="${
				task.id
			}">
            <input 
                type="checkbox" 
                class="task-checkbox" 
                ${task.completed ? 'checked' : ''}
                onclick="toggleTask(${task.id})"
            >
            <span class="task-text">${escapeHtml(task.text)}</span>
            <div class="task-actions">
                <button class="delete-btn" onclick="deleteTask(${task.id})">
                    ✕
                </button>
            </div>
        </div>
    `
		)
		.join('')
}

// Переключение статуса задачи
function toggleTask(id) {
	const task = tasks.find(t => t.id === id)
	if (task) {
		task.completed = !task.completed
		saveTasks()
		renderTasks()
		updateStats()
	}
}

// Удаление задачи
function deleteTask(id) {
	if (confirm('Удалить эту задачу?')) {
		tasks = tasks.filter(task => task.id !== id)
		saveTasks()
		renderTasks()
		updateStats()
	}
}

// Фильтрация задач
function filterTasks(filter) {
	currentFilter = filter

	// Обновляем активную кнопку фильтра
	document.querySelectorAll('.filters button').forEach(btn => {
		btn.classList.remove('active')
	})
	event.target.classList.add('active')

	renderTasks()
}

// Очистка выполненных задач
function clearCompleted() {
	if (confirm('Удалить все выполненные задачи?')) {
		tasks = tasks.filter(task => !task.completed)
		saveTasks()
		renderTasks()
		updateStats()
	}
}

// Обновление статистики
function updateStats() {
	const total = tasks.length
	const completed = tasks.filter(task => task.completed).length
	const active = total - completed

	document.getElementById('totalCount').textContent = total
	document.getElementById('completedCount').textContent = completed
	document.getElementById('activeCount').textContent = active
}

// Сохранение в localStorage
function saveTasks() {
	localStorage.setItem('tasks', JSON.stringify(tasks))
}

// Загрузка из localStorage
function loadTasks() {
	const saved = localStorage.getItem('tasks')
	if (saved) {
		tasks = JSON.parse(saved)
		renderTasks()
	}
}

// Защита от XSS
function escapeHtml(text) {
	const div = document.createElement('div')
	div.textContent = text
	return div.innerHTML
}

// Добавление по Enter
document.getElementById('taskInput').addEventListener('keypress', function (e) {
	if (e.key === 'Enter') {
		addTask()
	}
})
