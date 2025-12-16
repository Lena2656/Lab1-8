;(function () {
	const display = document.getElementById('display')
	const keys = document.querySelector('.keys')
	const error = document.getElementById('error')

	// Создаем элемент для отображения текущей операции
	const operationDisplay = document.createElement('div')
	operationDisplay.className = 'operation-indicator'
	display.parentNode.insertBefore(operationDisplay, display)

	let firstOperand = null
	let pendingOp = null
	let overwrite = true
	let currentOperation = ''

	function setError(msg) {
		error.textContent = msg || ''
	}

	function setDisplay(value) {
		display.value = value
	}

	function updateOperationDisplay() {
		if (firstOperand !== null && pendingOp) {
			operationDisplay.textContent = `${firstOperand} ${pendingOp}`
		} else {
			operationDisplay.textContent = currentOperation
		}
	}

	function parseDisplay() {
		const v = display.value.replace(',', '.')
		return Number(v)
	}

	function inputDigit(d) {
		setError('')
		if (overwrite || display.value === '0') {
			setDisplay(d)
			overwrite = false
		} else {
			setDisplay(display.value + d)
		}
		updateOperationDisplay()
	}

	function inputDot() {
		setError('')
		if (overwrite) {
			setDisplay('0.')
			overwrite = false
			return
		}
		if (!display.value.includes('.')) {
			setDisplay(display.value + '.')
		}
		updateOperationDisplay()
	}

	function clearAll() {
		firstOperand = null
		pendingOp = null
		overwrite = true
		currentOperation = ''
		setDisplay('0')
		setError('')
		updateOperationDisplay()
		// Снимаем выделение со всех операций
		document.querySelectorAll('.key-op').forEach(btn => {
			btn.classList.remove('active')
		})
	}

	function applyOp(op, a, b) {
		switch (op) {
			case '+':
				return a + b
			case '-':
				return a - b
			case '*':
				return a * b
			case '/':
				if (b === 0) {
					throw new Error('Деление на ноль')
				}
				return a / b
			default:
				return b
		}
	}

	function chooseOp(op) {
		setError('')
		const current = parseDisplay()

		// Снимаем выделение со всех операций
		document.querySelectorAll('.key-op').forEach(btn => {
			btn.classList.remove('active')
		})

		// Выделяем текущую операцию
		const activeOpButton = document.querySelector(`[data-op="${op}"]`)
		if (activeOpButton) {
			activeOpButton.classList.add('active')
		}

		currentOperation = `${display.value} ${op}`

		if (pendingOp === null) {
			firstOperand = current
		} else if (!overwrite) {
			try {
				firstOperand = applyOp(pendingOp, firstOperand, current)
				setDisplay(String(firstOperand))
			} catch (e) {
				setError(e.message)
			}
		}
		pendingOp = op
		overwrite = true
		updateOperationDisplay()
	}

	function equals() {
		if (pendingOp === null) return

		// Снимаем выделение со всех операций
		document.querySelectorAll('.key-op').forEach(btn => {
			btn.classList.remove('active')
		})

		const current = parseDisplay()
		try {
			const result = applyOp(pendingOp, firstOperand, current)
			currentOperation = `${firstOperand} ${pendingOp} ${current} = ${result}`
			setDisplay(String(result))
			firstOperand = result
			pendingOp = null
			overwrite = true
			setError('')
			updateOperationDisplay()

			// Через 2 секунды очищаем отображение операции
			setTimeout(() => {
				if (pendingOp === null) {
					currentOperation = ''
					updateOperationDisplay()
				}
			}, 2000)
		} catch (e) {
			setError(e.message)
			currentOperation = `${firstOperand} ${pendingOp} ${current} = Ошибка`
			updateOperationDisplay()
		}
	}

	function toggleSign() {
		if (display.value === '0') return
		if (display.value.startsWith('-')) {
			setDisplay(display.value.slice(1))
		} else {
			setDisplay('-' + display.value)
		}
		updateOperationDisplay()
	}

	function toPercent() {
		const v = parseDisplay()
		setDisplay(String(v / 100))
		updateOperationDisplay()
	}

	// Добавляем обработчики событий для улучшенной обратной связи
	keys.addEventListener('click', e => {
		const btn = e.target.closest('button')
		if (!btn) return

		// Эффект нажатия
		btn.style.transform = 'scale(0.95)'
		setTimeout(() => {
			btn.style.transform = ''
		}, 100)

		const action = btn.getAttribute('data-action')
		const text = btn.textContent

		if (!action) {
			if (text === '.') inputDot()
			else inputDigit(text)
			return
		}

		switch (action) {
			case 'clear':
				clearAll()
				break
			case 'op':
				chooseOp(btn.getAttribute('data-op'))
				break
			case 'equals':
				equals()
				break
			case 'sign':
				toggleSign()
				break
			case 'percent':
				toPercent()
				break
			default:
				break
		}
	})

	// Добавляем поддержку клавиатуры
	document.addEventListener('keydown', function (event) {
		if (event.key >= '0' && event.key <= '9') {
			inputDigit(event.key)
		} else if (event.key === '.') {
			inputDot()
		} else if (event.key === '+') {
			chooseOp('+')
		} else if (event.key === '-') {
			chooseOp('-')
		} else if (event.key === '*') {
			chooseOp('*')
		} else if (event.key === '/') {
			event.preventDefault()
			chooseOp('/')
		} else if (event.key === 'Enter' || event.key === '=') {
			event.preventDefault()
			equals()
		} else if (event.key === 'Escape') {
			clearAll()
		} else if (event.key === '%') {
			toPercent()
		}
	})

	// Инициализация
	clearAll()

	// Логирование для отладки
	console.log('Калькулятор инициализирован')
	console.log('Используйте мышь или клавиатуру для ввода')
	console.log('Операции: +, -, *, /')
	console.log('Enter или = для вычисления')
	console.log('Escape для очистки')
})()
